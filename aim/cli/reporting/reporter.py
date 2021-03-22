import json
import os
from typing import Any, Dict, Optional
import uuid

from humbug.consent import HumbugConsent
from humbug.report import Reporter

from aim.__version__ import __version__ as aim_version
from aim.engine.configs import (
    AIM_REPORT_CONFIG_FILE_NAME,
    AIM_CONFIG_FILE_NAME,
    AIM_REPO_NAME,
    HUMBUG_TOKEN,
    HUMBUG_KB_ID,
)


aim_version_tag = "version:{}".format(aim_version)
aim_tags = [aim_version_tag]


def get_aim_repo_dir(initialized_only: bool = False) -> Optional[str]:
    # Get working directory path
    working_dir = os.getcwd()

    # Try to find closest .aim repository
    repo_found = False
    while True:
        if len(working_dir) <= 1:
            break

        repo_path = os.path.join(working_dir, AIM_REPO_NAME)
        config_file_path = os.path.join(repo_path, AIM_CONFIG_FILE_NAME)

        if (not initialized_only and os.path.exists(repo_path)) or (
            initialized_only and os.path.isfile(config_file_path)
        ):
            repo_found = True
            break
        else:
            working_dir = os.path.split(working_dir)[0]

    if not repo_found:
        return None

    return os.path.join(working_dir, AIM_REPO_NAME)


def get_reporting_config_path() -> Optional[str]:
    repo_dir = get_aim_repo_dir(initialized_only=True)
    if repo_dir is None:
        return None
    return os.path.join(repo_dir, AIM_REPORT_CONFIG_FILE_NAME)


def save_reporting_config(consent: bool, client_id: Optional[str] = None):
    """
    Allow or disallow Aim reporting.
    """
    config_report_path = get_reporting_config_path()
    if config_report_path is None:
        raise Exception(
            'Config report file not found, use "aim init" to initialize a new repository'
        )

    reporting_config = {}
    if os.path.isfile(config_report_path):
        try:
            with open(config_report_path, "r") as ifp:
                reporting_config = json.load(ifp)
        except Exception:
            pass

    if client_id is not None and reporting_config.get("client_id") is None:
        reporting_config["client_id"] = client_id

    if reporting_config.get("client_id") is None:
        reporting_config["client_id"] = str(uuid.uuid4())

    reporting_config["consent"] = consent

    try:
        with open(config_report_path, "w") as ofp:
            json.dump(reporting_config, ofp)
    except Exception:
        pass


def get_reporting_config() -> Dict[str, Any]:
    reporting_config = {}
    config_report_path = get_reporting_config_path()
    if config_report_path is not None:
        try:
            if not os.path.exists(config_report_path):
                client_id = str(uuid.uuid4())
                reporting_config["client_id"] = client_id
                save_reporting_config(True, client_id)
            else:
                with open(config_report_path, "r") as ifp:
                    reporting_config = json.load(ifp)
        except Exception:
            pass
    return reporting_config


session_id = str(uuid.uuid4())


def aim_consent_from_reporting_config_file() -> bool:
    reporting_config = get_reporting_config()
    return reporting_config.get("consent", False)


client_id = get_reporting_config().get("client_id")

aim_consent = HumbugConsent(aim_consent_from_reporting_config_file)
aim_reporter = Reporter(
    name="aim",
    consent=aim_consent,
    client_id=client_id,
    session_id=session_id,
    bugout_token=HUMBUG_TOKEN,
    bugout_journal_id=HUMBUG_KB_ID,
)
