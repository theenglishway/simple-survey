import click
import os

from flask.cli import AppGroup
from flask_migrate.cli import migrate, upgrade

from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError, InvalidRequestError

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
@click.argument('name', type=click.STRING, required=False)
def import_poll(json_file_path, name):
    """
    Import poll contained in file at JSON_FILE_PATH under the name NAME
    (if present) or the file name.
    """
    from app.models import Poll

    dir, file = os.path.split(json_file_path)
    file_name, ext_name = os.path.splitext(file)
    if ext_name != '.json':
        raise TypeError('Expected json file, got {}'.format(ext_name))

    name = name or file_name
    try:
        p = Poll.import_from_local(name, json_file_path)
    except IntegrityError as e:
        if 'UNIQUE' in e.args[0]:
            click.echo('Error : poll "{}" already exists !'.format(e.params[0]))
            return

        raise e
    except InvalidRequestError as e:
        if 'Table' in e.args[0]:
            click.echo('Error : poll "{}" already exists !'.format(name))
            return

        raise e

    click.echo(
        "Successfully imported poll '{}', available at url : polls/{}".format(
            p.name, p.slug
        )
    )


@poll_cli.command('upgrade')
@click.pass_context
def db_poll(ctx):
    """Upgrade database to store conversion of raw poll results."""
    from app.models import results

    missing_poll_names = [
        p for p, r in _get_table_states(results).items() if not r
    ]

    ctx.invoke(
        migrate,
        message="Add result model for '{}'".format(', '.join(missing_poll_names))
    )
    ctx.invoke(upgrade)

    click.echo(
        "New poll(s) are now analyzable : {}".format(
            ', '.join(missing_poll_names)
        )
    )


@poll_cli.command('convert')
def convert_results():
    """
    Convert all raw results that have not been converted to their respective
    result model yet.
    """
    from app.models import Poll, RawResult, results

    stats = {}
    # For all types of results ...
    for slug, model in results.items():
        # Query the list of raw results for the corresponding poll that have
        # not been converted yet
        non_converted_raws = (RawResult.query.join(Poll, Poll.slug==slug)
                                            .filter(RawResult.converted == False)
                                            .all())

        if non_converted_raws:
            stats[slug] = len(non_converted_raws)

            # Add all the results converted into their respective models
            db.session.add_all([model.from_raw(r) for r in non_converted_raws])
            # On each raw result instance, set the flag signaling that is has
            # been updated
            db.session.bulk_update_mappings(RawResult, [{
                'id': r.id,
                'converted': True
            } for r in non_converted_raws])

    db.session.commit()

    if stats:
        click.echo(
            "Successfully converted raw results for {} poll(s) : ".format(len(stats))
        )
        click.echo(
            '\n'.join([
                '"{}" : {} result(s)'.format(slug, count)
                for slug, count in stats.items()
            ])
        )
    else:
        click.echo("Nothing to do")


@poll_cli.command('list')
def list_polls():
    """List all current polls."""
    from app.models import results

    result_states = _get_table_states(results)
    click.echo(
        '\n'.join([
            '  * {}: <{}>'.format(k, 'analyzable' if r else 'accessible')
            for k, r in result_states.items()
        ])
    )

app.cli.add_command(poll_cli)
