import attrs


@attrs.frozen
class ServiceAccountProfile:
    id: str
    name: str
    description: str
    created_by: str
    is_active: bool
    obscured_key: str


def set_credentials(tecton_api_key: str) -> None:
    """
    Explicitly override tecton credentials settings.

    Typically, Tecton credentials are set in environment variables, but if your
    Tecton SDK setup requires another type of setup, you can use this function
    to set the Tecton API Key secret during an interactive Python session.

    :param tecton_api_key: Tecton API Key
    """
    # Import this lazily so we don't trigger initialization that happens on importing conf module.
    from tecton import conf

    conf.set("TECTON_API_KEY", tecton_api_key)


def who_am_i():
    """Introspect the current User or API Key used to authenticate with Tecton"""
    from tecton import conf
    from tecton import okta
    from tecton_core.id_helper import IdHelper
    from tecton.identities import api_keys

    user_profile = okta.get_user_profile()
    if user_profile:
        return user_profile
    else:
        token = conf.get_or_none("TECTON_API_KEY")
        if token:
            try:
                introspect_result = api_keys.introspect(token)
            except PermissionError as e:
                print("Permissions error when introspecting the tecton api key")
                return None
            if introspect_result is not None:
                return ServiceAccountProfile(
                    id=IdHelper.to_string(introspect_result.id),
                    name=introspect_result.name,
                    description=introspect_result.description,
                    created_by=introspect_result.created_by,
                    is_active=introspect_result.active,
                    obscured_key=f"****{token[-4:]}",
                )
    return None
