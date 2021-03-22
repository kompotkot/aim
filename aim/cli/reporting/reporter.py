import json
import os
from typing import Any, Dict, Optional
import uuid

from humbug.consent import HumbugConsent
from humbug.report import Reporter

from aim.__version__ import __version__ as aim_version
from aim.engine.configs import AIM_REPORT_CONFIG_FILE_NAME, HUMBUG_TOKEN, HUMBUG_KB_ID
from aim.engine.repo import AimRepo


aim_version_tag = "version:{}".format(aim_version)
aim_tags = [aim_version_tag]

def get_reporting_config_path() -> Optional[str]:
    repo_dir = AimRepo.get_aim_repo_dir(initialized_only=True)
    if repo_dir is None:
        return None
    return os.path.join(repo_dir, AIM_REPORT_CONFIG_FILE_NAME)

def save_reporting_config(consent: bool, client_id: Optional[str] = None):
    """
    Allow or disallow Aim reporting.
    """
    config_report_path = get_reporting_config_path()
    if config_report_path is not None:
        # TODO: Raise error
        return

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


def configure_reporter(
    client_id: uuid.UUID, aim_consent: bool, reporter: Reporter = aim_reporter
) -> Reporter:
    """
    Prepare Humbug Consent mechanism and create reporter.
    """
    aim_reporter.consent = aim_consent
    aim_reporter.client_id = client_id
    # return aim_reporter


def init_reporter(reporting_config: Dict[str, Any]):
    aim_reporter = configure_reporter(
        client_id=reporting_config.get("client_id"),
        aim_consent=reporting_config.get("consent"),
    )
    aim_reporter.setup_excepthook(publish=True, tags=aim_tags)
