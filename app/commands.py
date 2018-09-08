import click
import os

from flask.cli import AppGroup
from flask_migrate.cli import migrate, upgrade

from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

from app import app, db


poll_cli = AppGroup('poll')


def _get_table_states(results):
    """
    :param results: A dictionary mapping poll names to Result models
    :return: A dictionary mapping poll names to a boolean value that indicates
    whether the database table for the corresponding Result model has been
    created
    """
    table_states = {}
    for k, r in results.items():
        i = inspect(r)
        table_states[k] = all([db.engine.has_table(t.name) for t in i.tables])
    return table_states


@poll_cli.command('import')
@click.argument(
    'json_file_path',
    type=click.Path(exists=True, dir_okay=False)
)
def import_poll(json_file_path):
    """Import poll contained in file at JSON_FILE_PATH."""
    from app.models import Poll

    dir, file = os.path.split(json_file_path)
    file_name, ext_name = os.path.splitext(file)
    if ext_name != '.json':
        raise TypeError('Expect json file, got {}'.format(ext_name))

    try:
        p = Poll.import_from_local(file_name, json_file_path)
    except IntegrityError as e:
        if 'UNIQUE' in e.args[0]:
            click.echo('Error : poll "{}" already exists !'.format(e.params[0]))
            return

        raise e

    click.echo('Successfully imported {}'.format(p))
    click.echo('Call "flask poll upgrade" to complete the operation')


@poll_cli.command('upgrade')
@click.pass_context
def db_poll(ctx):
    """Upgrade database to handle newly-imported polls."""
    from app.models import results

    missing_polls = [p for p, r in _get_table_states(results).items() if not r]

    ctx.invoke(
        migrate,
        message="Add polls '{}'".format(', '.join(missing_polls))
    )
    ctx.invoke(upgrade)

    click.echo("DB upgraded to add polls '{}'".format(', '.join(missing_polls)))


@poll_cli.command('list')
def list_polls():
    """List all current polls."""
    from app.models import results

    result_states = _get_table_states(results)
    click.echo(
        '\n'.join([
            '  * "{}": <{}>'.format(k, 'ready' if r else 'pending')
            for k, r in result_states.items()
        ])
    )

app.cli.add_command(poll_cli)
