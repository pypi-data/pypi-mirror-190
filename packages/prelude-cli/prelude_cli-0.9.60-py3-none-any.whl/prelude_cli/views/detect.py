import click

from datetime import datetime, timedelta, timezone
from rich import print_json
from rich.console import Console
from rich.table import Table
from collections import defaultdict

from prelude_cli.views.shared import handle_api_error
from prelude_sdk.controllers.build_controller import BuildController
from prelude_sdk.controllers.detect_controller import DetectController
from prelude_sdk.models.codes import RunCode, ExitCodeGroup


@click.group()
@click.pass_context
def detect(ctx):
    """ Continuously test your endpoints """
    ctx.obj = DetectController(account=ctx.obj)


@detect.command('create-endpoint')
@click.option('--tags', help='a comma-separated list of tags for this endpoint', type=str, default='')
@click.argument('name')
@click.pass_obj
@handle_api_error
def register_endpoint(controller, name, tags):
    """ Register a new endpoint """
    endpoint_token = controller.register_endpoint(name=name, tags=tags)
    click.secho(f'Endpoint token: {endpoint_token}', fg='green')


@detect.command('enable-test')
@click.argument('test')
@click.option('--tags', help='only enable for these tags (comma-separated list)', type=str, default='')
@click.option('--run_code',
              help='provide a run_code',
              default='daily', show_default=True,
              type=click.Choice(['daily', 'weekly', 'monthly', 'once', 'debug'], case_sensitive=False))
@click.pass_obj
@handle_api_error
def activate_test(controller, test, run_code, tags):
    """ Add TEST to your queue """
    controller.enable_test(ident=test, run_code=RunCode[run_code.upper()].value, tags=tags)


@detect.command('disable-test')
@click.argument('test')
@click.confirmation_option(prompt='Are you sure?')
@click.pass_obj
@handle_api_error
def deactivate_test(controller, test):
    """ Remove TEST from your queue """
    controller.disable_test(ident=test)
    click.secho(f'Disabled {test}', fg='green')


@detect.command('delete-endpoint')
@click.argument('endpoint_id')
@click.confirmation_option(prompt='Are you sure?')
@click.pass_obj
@handle_api_error
def delete_endpoint(controller, endpoint_id):
    """Delete a probe/endpoint"""
    controller.delete_endpoint(ident=endpoint_id)
    click.secho(f'Deleted {endpoint_id}', fg='green')


@detect.command('queue')
@click.pass_obj
@handle_api_error
def queue(controller):
    """ List all tests in your active queue """
    build = BuildController(account=controller.account)
    tests = {row['id']: row['name'] for row in build.list_tests()}
    active = controller.print_queue()
    for q in active:
        q['run_code'] = RunCode(q['run_code']).name
        q['name'] = tests[q['test']]
    print_json(data=active)


@detect.command('observe')
@click.argument('result')
@click.option('--value', help='Mark 1 for observed', default=1, type=int)
@click.pass_obj
@handle_api_error
def observe(controller, result, value):
    """ Mark a result as observed """
    controller.observe(row_id=result, value=value)


@detect.command('search')
@click.argument('cve')
@click.pass_obj
@handle_api_error
def search(controller, cve):
    """ Search the NVD for a specific CVE identifier """
    print("This product uses the NVD API but is not endorsed or certified by the NVD.\n")
    print_json(data=controller.search(identifier=cve))


@detect.command('rules')
@click.pass_obj
@handle_api_error
def rules(controller):
    """ Print all Verified Security Rules """
    print_json(data=controller.list_rules())


@detect.command('probes')
@click.option('--days', help='days to look back', default=7, type=int)
@click.pass_obj
@handle_api_error
def list_probes(controller, days):
    """ List all endpoint probes """
    print_json(data=controller.list_probes(days=days))


@detect.command('social-stats')
@click.argument('test')
@click.option('--days', help='days to look back', default=30, type=int)
@click.pass_obj
@handle_api_error
def social_statistics(controller, test, days):
    """ Pull social statistics for a specific test """
    stats = defaultdict(lambda: defaultdict(int))
    for dos, values in controller.social_stats(ident=test, days=days).items():
        for state, count in values.items():
            stats[dos][state] = count
    print_json(data=stats)


@detect.command('activity')
@click.option('--days', help='days to look back', default=7, type=int)
@click.option('--view',
              help='retrieve a specific result view',
              default='logs', show_default=True,
              type=click.Choice(['logs', 'days', 'insights'], case_sensitive=False))
@click.option('--tests', help='comma-separated list of test IDs', type=str)
@click.option('--endpoints', help='comma-separated list of endpoint IDs', type=str)
@click.option('--statuses', help='comma-separated list of statuses', type=str)
@click.pass_obj
@handle_api_error
def describe_activity(controller, days, view, tests, endpoints, statuses):
    """ View my Detect results """
    filters = dict(
        start=datetime.now(timezone.utc) - timedelta(days=days),
        finish=datetime.now(timezone.utc)
    )
    if tests:
        filters['tests'] = tests
    if endpoints:
        filters['endpoints'] = endpoints
    if statuses:
        filters['statuses'] = statuses

    raw = controller.describe_activity(view=view, filters=filters)
    report = Table()

    if view == 'logs':
        build = BuildController(account=controller.account)
        tests = {row['id']: row['name'] for row in build.list_tests()}

        report.add_column('timestamp')
        report.add_column('result ID')
        report.add_column('name')
        report.add_column('test')
        report.add_column('endpoint')
        report.add_column('status')
        report.add_column('observed')

        for record in raw:
            report.add_row(
                record['date'], 
                record['id'], 
                tests.get(record['test'], 'DELETED'),
                record['test'],
                record['endpoint_id'], 
                record['status'],
                'yes' if record.get('observed') else '-'
            )

    elif view == 'insights':
        report.add_column('test')
        report.add_column('dos')
        report.add_column('failed (%)', style='red')
        
        for insight in raw:
            report.add_row(insight['test'], insight['dos'], str(insight["rate"]))

    elif view == 'days':
        report.add_column('date')
        report.add_column('protected', style='green')
        report.add_column('unprotected',  style='red')
        report.add_column('error', style='yellow')

        for date, states in raw.items():
            report.add_row(
                date, 
                str(states.get(ExitCodeGroup.PROTECTED.name, 0)), 
                str(states.get(ExitCodeGroup.UNPROTECTED.name, 0)), 
                str(states.get(ExitCodeGroup.ERROR.name, 0)), 
            )

    console = Console()
    console.print(report)
