import click

from humbug.report import Report

from aim.cli.reporting.reporter import aim_reporter, save_reporting_config


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
