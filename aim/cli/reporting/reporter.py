from typing import Any, Dict
import uuid

from humbug.consent import HumbugConsent
from humbug.report import Reporter

from aim.__version__ import __version__ as aim_version
from aim.engine.configs import HUMBUG_TOKEN, HUMBUG_KB_ID

aim_version_tag = "version:{}".format(aim_version)
aim_tags = [aim_version_tag]


def configure_reporter(client_id: uuid.UUID, aim_consent: bool) -> Reporter:
    """
    Prepare Humbug Consent mechanism and create reporter.
    """
    session_id = str(uuid.uuid4())

    aim_consent = HumbugConsent(aim_consent)
    aim_reporter = Reporter(
        name="aim",
        consent=aim_consent,
        client_id=client_id,
        session_id=session_id,
        bugout_token=HUMBUG_TOKEN,
        bugout_journal_id=HUMBUG_KB_ID,
    )

    return aim_reporter


def init_reporter(reporting_config: Dict[str, Any]):
    aim_reporter = configure_reporter(
        client_id=reporting_config.get("client_id"),
        aim_consent=reporting_config.get("consent"),
    )
    aim_reporter.setup_excepthook(publish=True, tags=aim_tags)
