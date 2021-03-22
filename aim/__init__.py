from aim.sdk import *
from aim.cli.reporting.reporter import aim_reporter, aim_tags

aim_reporter.system_report(publish=True, tags=aim_tags)
aim_reporter.setup_excepthook(publish=True, tags=aim_tags)
