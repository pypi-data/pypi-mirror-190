import io
import os
import sys
import tarfile
import time
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple

import requests
from google.protobuf.json_format import MessageToJson
from yaspin.spinners import Spinners

import tecton
from .error_utils import format_server_errors
from tecton._internals import metadata_service
from tecton._internals.analytics import TectonStateUpdateMetrics
from tecton._internals.utils import is_live_workspace
from tecton.cli import printer
from tecton.cli.engine_renderer import ThickPlanRenderingClient
from tecton.cli.engine_renderer import ThinPlanRenderingClient
from tecton.unified import common as unified_common
from tecton_core.errors import TectonAPIValidationError
from tecton_core.errors import TectonInternalError
from tecton_core.feature_definition_wrapper import FrameworkVersion
from tecton_core.id_helper import IdHelper
from tecton_proto.args.entity_pb2 import EntityArgs
from tecton_proto.args.fco_args_pb2 import FcoArgs
from tecton_proto.args.feature_service_pb2 import FeatureServiceArgs
from tecton_proto.args.feature_view_pb2 import FeatureViewArgs
from tecton_proto.args.repo_metadata_pb2 import FeatureRepoSourceInfo
from tecton_proto.args.transformation_pb2 import TransformationArgs
from tecton_proto.args.virtual_data_source_pb2 import VirtualDataSourceArgs
from tecton_proto.metadataservice.metadata_service_pb2 import ApplyStateUpdateRequest
from tecton_proto.metadataservice.metadata_service_pb2 import NewStateUpdateRequest
from tecton_proto.metadataservice.metadata_service_pb2 import QueryStateUpdateRequest


def get_declared_fco_args(objects) -> Tuple[List[FcoArgs], FeatureRepoSourceInfo]:
    all_args = []
    repo_source_info = FeatureRepoSourceInfo()

    for fco_obj in objects:
        # TODO(TEC-12828): Clean this logic up and improve type annotations.
        if isinstance(fco_obj, unified_common.BaseTectonObject):
            all_args.append(fco_obj._build_args())
            repo_source_info.source_info.append(fco_obj._source_info)
        else:
            fco_args = FcoArgs()
            args = fco_obj._args
            source_info = fco_obj._source_info
            if isinstance(args, VirtualDataSourceArgs):
                source_info.fco_id.CopyFrom(args.virtual_data_source_id)
                fco_args.virtual_data_source.CopyFrom(args)
            elif isinstance(args, EntityArgs):
                source_info.fco_id.CopyFrom(args.entity_id)
                fco_args.entity.CopyFrom(args)
            elif isinstance(args, TransformationArgs):
                source_info.fco_id.CopyFrom(args.transformation_id)
                fco_args.transformation.CopyFrom(args)
            elif isinstance(args, FeatureViewArgs):
                source_info.fco_id.CopyFrom(args.feature_view_id)
                fco_args.feature_view.CopyFrom(args)
            elif isinstance(args, FeatureServiceArgs):
                source_info.fco_id.CopyFrom(args.feature_service_id)
                fco_args.feature_service.CopyFrom(args)
            else:
                raise RuntimeError(f"Unknown object {fco_obj}")

            all_args.append(fco_args)

            source_info.CopyFrom(source_info)
            repo_source_info.source_info.append(source_info)

    return all_args, repo_source_info


def dump_local_state(objects):
    with printer.safe_yaspin(Spinners.earth, text="Collecting local feature declarations") as sp:
        fco_args, repo_source_info = get_declared_fco_args(objects)
        sp.ok(printer.safe_string("✅"))

    request_plan = NewStateUpdateRequest()
    request_plan.request.fco_args.extend(fco_args)
    request_plan.request.repo_source_info.CopyFrom(repo_source_info)
    printer.safe_print(MessageToJson(request_plan, including_default_value_fields=True))


# upload tar.gz of python files to url via PUT request
def upload_files(repo_files: List[Path], repo_root, url: str):
    tar_bytes = io.BytesIO()
    with tarfile.open(fileobj=tar_bytes, mode="w|gz") as targz:
        for f in repo_files:
            targz.add(f, arcname=os.path.relpath(f, repo_root))
    for _ in range(3):
        try:
            r = requests.put(url, data=tar_bytes.getbuffer())
            if r.status_code != 200:
                # We will get 403 (forbidden) when the signed url expires.
                if r.status_code == 403:
                    printer.safe_print(
                        f"\nUploading feature repo failed due to expired session. Please retry the command."
                    )
                else:
                    printer.safe_print(f"\nUploading feature repo failed with reason: {r.reason}")
                sys.exit(1)
            return
        except requests.RequestException as e:
            last_error = e
    else:
        raise SystemExit(last_error)


def update_tecton_state(
    objects,
    repo_files: List[Path],
    repo_root: str,
    apply,
    debug,
    interactive,
    upgrade_all: bool,
    workspace_name: str,
    suppress_warnings: bool = False,
    suppress_recreates: bool = False,
    json_out_path: Optional[Path] = None,
    timeout_seconds=90 * 60,
    plan_id: Optional[str] = None,
) -> TectonStateUpdateMetrics:
    # In debug mode we compute the plan synchronously, do not save it in the database, and do not allow to apply it.
    # Primary goal is allowing local development/debugging plans against remote clusters in read-only mode.
    assert not (debug and apply), "Cannot apply in debug mode"

    if apply and plan_id:
        # Applying an existing plan, so skip preparing args.
        state_id = IdHelper.from_string(plan_id)
        request_query = QueryStateUpdateRequest()
        request_query.state_id.CopyFrom(state_id)
        request_query.workspace = workspace_name

        try:
            response_query = metadata_service.instance().QueryStateUpdate(request_query)
        except (
            TectonInternalError,
            TectonAPIValidationError,
        ) as e:
            printer.safe_print(e)
            return TectonStateUpdateMetrics.from_error_message(str(e), suppress_recreates)

        if response_query.error:
            printer.safe_print(response_query.error)
            return TectonStateUpdateMetrics.from_error_message(response_query.error, suppress_recreates)
        if response_query.validation_result.errors:
            # Cannot pretty-print validation result using format_server_errors(), because collected local objects
            # might have changed since this plan was generated, so can't accurately match with this plan's FCOs.
            message = f"Cannot apply plan because it had errors."
            printer.safe_print(message)
            return TectonStateUpdateMetrics.from_error_message(message, suppress_recreates)
    else:
        with printer.safe_yaspin(Spinners.earth, text="Collecting local feature declarations") as sp:
            fco_args, repo_source_info = get_declared_fco_args(objects)
            sp.ok(printer.safe_string("✅"))

        request_plan = NewStateUpdateRequest()
        request_plan.request.workspace = workspace_name

        request_plan.request.upgrade_all = upgrade_all
        request_plan.request.sdk_version = tecton.version.get_semantic_version() or ""

        request_plan.request.fco_args.extend(fco_args)
        request_plan.request.repo_source_info.CopyFrom(repo_source_info)
        request_plan.request.suppress_recreates = suppress_recreates

        if debug:
            request_plan.blocking_dry_run_mode = True
        else:
            request_plan.enable_eager_response = True

        server_side_msg_prefix = "Performing server-side feature validation: "
        with printer.safe_yaspin(Spinners.earth, text=f"{server_side_msg_prefix}: Initializing.") as sp:
            try:
                response_submit = metadata_service.instance().NewStateUpdate(request_plan)
                if response_submit.HasField("signed_url_for_repo_upload"):
                    upload_files(repo_files, repo_root, response_submit.signed_url_for_repo_upload)
                if response_submit.HasField("eager_response"):
                    response_query = response_submit.eager_response
                else:
                    seconds_slept = 0
                    request_query = QueryStateUpdateRequest()
                    request_query.workspace = workspace_name
                    request_query.state_id.CopyFrom(response_submit.state_id)
                    while True:
                        response_query = metadata_service.instance().QueryStateUpdate(request_query)
                        if response_query.latest_status_message:
                            sp.text = server_side_msg_prefix + response_query.latest_status_message
                        if response_query.ready:
                            break
                        seconds_to_sleep = 5
                        time.sleep(seconds_to_sleep)
                        seconds_slept += seconds_to_sleep
                        if seconds_slept > timeout_seconds:
                            sp.fail(printer.safe_string("⛔"))
                            printer.safe_print("Validation timed out.")
                            return TectonStateUpdateMetrics.from_error_message(
                                "Validation timed out.", suppress_recreates
                            )

                if response_query.error:
                    sp.fail(printer.safe_string("⛔"))
                    printer.safe_print(response_query.error)
                    return TectonStateUpdateMetrics.from_error_message(response_query.error, suppress_recreates)
                if response_query.validation_result.errors:
                    sp.fail(printer.safe_string("⛔"))
                    format_server_errors(response_query.validation_result.errors, objects, repo_root)
                    return TectonStateUpdateMetrics.from_error_message(
                        str(response_query.validation_result.errors), suppress_recreates
                    )
                sp.ok(printer.safe_string("✅"))
            except (
                TectonInternalError,
                TectonAPIValidationError,
            ) as e:
                sp.fail(printer.safe_string("⛔"))
                printer.safe_print(e)
                return TectonStateUpdateMetrics.from_error_message(str(e), suppress_recreates)

        state_id = response_submit.state_id

    enable_server_side_rendering = False  # TODO: get value from a flag
    if enable_server_side_rendering:
        plan_rendering_client = ThinPlanRenderingClient()
    else:
        plan_rendering_client = ThickPlanRenderingClient(
            response_query.diff_items,
            response_query.validation_result.warnings,
            state_id,
            suppress_warnings,
            workspace_name,
            is_live_workspace(workspace_name),
            debug,
            response_query.recreates_suppressed,
        )

    plan_rendering_client.print_plan()

    if apply and plan_rendering_client.has_diffs():
        # Use the workspace from the update request because the current workspace may have changed.
        plan_rendering_client.confirm_apply_or_exit(interactive)

        request_apply = ApplyStateUpdateRequest()
        request_apply.state_id.CopyFrom(state_id)
        metadata_service.instance().ApplyStateUpdate(request_apply)

        printer.safe_print("🎉 all done!")

    if json_out_path:
        repo_diff_summary = plan_rendering_client.to_diff_summary_proto()
        json_out_path.parent.mkdir(parents=True, exist_ok=True)
        json_out_path.write_text(MessageToJson(repo_diff_summary))

    num_v3_fcos = sum(
        obj._args.version in (FrameworkVersion.UNSPECIFIED.value, FrameworkVersion.FWV3.value) for obj in objects
    )
    num_v5_fcos = sum(obj._args.version is FrameworkVersion.FWV5.value for obj in objects)

    return TectonStateUpdateMetrics(
        num_total_fcos=len(objects),
        num_fcos_changed=plan_rendering_client.num_fcos_changed,
        num_v3_fcos=num_v3_fcos,
        num_v5_fcos=num_v5_fcos,
        # return full warnings for tests but only send the number of warnings to amplitude
        warnings=plan_rendering_client.warnings,
        suppress_recreates=suppress_recreates,
        json_out=(json_out_path is not None),
    )
