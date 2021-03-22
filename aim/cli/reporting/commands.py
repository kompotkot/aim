import click

from humbug.report import Report

from aim.engine.repo import AimRepo
from aim.cli.reporting.reporter import configure_reporter
from aim.cli.de.utils import repo_init_alert


@click.command()
@click.option("--on/--off", help="Turn crash report on/off")
def reporting(on):
    """
    Enable or disable sending crash reports to Aim.
    """
    repo_inst = AimRepo.get_working_repo()
    if repo_inst is None or not repo_inst.exists():
        repo_init_alert()
        return

    reporting_config = repo_inst.get_reporting_config()
    aim_reporter = configure_reporter(
        client_id=reporting_config.get('client_id'), 
        aim_consent=reporting_config.get('consent')
    )
    report = Report(
        title="Consent change",
        tags=aim_reporter.system_tags(),
        content="Consent? `{}`".format(on),
    )
    aim_reporter.publish(report)
    repo_inst.save_reporting_config(on)
