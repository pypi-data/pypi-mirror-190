from enum import Enum
from typing import List
from typing import Tuple

from colorama import Fore
from typeguard import typechecked

from tecton import version as tecton_version
from tecton._internals import metadata_service
from tecton.unified import common as unified_common
from tecton_core import errors
from tecton_core import id_helper
from tecton_proto.args import fco_args_pb2
from tecton_proto.args import repo_metadata_pb2
from tecton_proto.data import state_update_pb2
from tecton_proto.metadataservice import metadata_service_pb2
from tecton_proto.validation import validator_pb2


class ValidationMode(str, Enum):
    EXPLICIT = "explicit"
    AUTOMATIC = "auto"


def print_validation_success(obj: unified_common.BaseTectonObject) -> None:
    print(f"{obj.__class__.__name__} '{obj.name}' has been successfully validated.")


def print_validating_dependencies(obj: unified_common.BaseTectonObject, dependency_count: int) -> None:
    if dependency_count == 1:
        print(f"Validating 1 dependency for {obj.__class__.__name__} '{obj.name}'.")
    elif dependency_count > 1:
        print(f"Validating {dependency_count} dependencies for {obj.__class__.__name__} '{obj.name}'.")


# Copy of logic in engine.py - but using unified objects for notebook development.
def _get_declared_fco_args(
    objects: List[unified_common.BaseTectonObject],
) -> Tuple[List[fco_args_pb2.FcoArgs], repo_metadata_pb2.FeatureRepoSourceInfo]:
    all_args = []
    repo_source_info = repo_metadata_pb2.FeatureRepoSourceInfo()

    for fco_obj in objects:
        source_info = fco_obj._source_info
        source_info.fco_id.CopyFrom(id_helper.IdHelper.from_string(fco_obj.info.id))

        repo_source_info.source_info.append(source_info)
        all_args.append(fco_obj._build_args())

    return all_args, repo_source_info


# Copy of logic in error_utils.py - but using unified objects for notebook development.
def _format_server_errors(
    messages: List[state_update_pb2.ValidationMessage], objects: List[unified_common.BaseTectonObject]
):
    obj_by_id = {}
    for fco_obj in objects:
        obj_by_id[fco_obj.info.id] = fco_obj

    for m in messages:
        obj_id = id_helper.IdHelper.to_string(m.fco_refs[0].fco_id)
        obj = obj_by_id[obj_id]
        print(f"================ Error found in {obj.__class__.__name__} {obj.info.name} ================")
        print(Fore.RED + m.message + Fore.RESET)


@typechecked
def run_backend_validation_for_local_fco(
    validation_request: validator_pb2.ValidationRequest,
) -> bool:
    try:
        validation_request = metadata_service_pb2.ValidateLocalFcoRequest(
            sdk_version=tecton_version.get_semantic_version() or "",
            validation_request=validation_request,
        )
        response = metadata_service.instance().ValidateLocalFco(validation_request).response_proto
        if not response.success:
            # TODO: Need a better way to print errors
            for error in response.validation_result.errors:
                print(error.message)
            return False
    except (
        errors.TectonInternalError,
        errors.TectonAPIValidationError,
    ) as e:
        print(e)
        return False
    return True
