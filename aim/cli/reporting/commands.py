import click

from humbug.report import Report

from aim.engine.repo import AimRepo
from aim.cli.reporting.reporter import aim_reporter, get_reporting_config, save_reporting_config
from aim.cli.de.utils import repo_init_alert


@click.command()
@click.option("--on/--off", help="Turn crash report on/off")
def reporting(on):
    """
    Enable or disable sending crash reports to Aim.
    """
    report = Report(
        title="Consent change",
        tags=aim_reporter.system_tags(),
        content="Consent? `{}`".format(on),
    )
    aim_reporter.publish(report)
    save_reporting_config(on)
