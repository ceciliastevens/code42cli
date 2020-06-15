import os
import py42.sdk
import py42.settings.debug as debug
import py42.settings

from code42cli.logger import get_main_cli_logger

py42.settings.items_per_page = 500
PY42_PASSWORD_KEY = u"PY42_PASS"


def create_sdk(profile, is_debug_mode):
    if is_debug_mode:
        py42.settings.debug.level = debug.DEBUG
    try:
        password = os.environ[PY42_PASSWORD_KEY] if PY42_PASSWORD_KEY in os.environ.keys() \
            else profile.get_password()
        return py42.sdk.from_local_account(profile.authority_url, profile.username, password)
    except Exception:
        logger = get_main_cli_logger()
        logger.print_and_log_error(
            u"Invalid credentials or host address. "
            u"Verify your profile is set up correctly and that you are supplying the correct password."
        )
        exit(1)


def validate_connection(authority_url, username, password):
    try:
        py42.sdk.from_local_account(authority_url, username, password)
        return True
    except:
        return False
