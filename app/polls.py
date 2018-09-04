from flask import session, render_template, Markup, abort
from sqlalchemy.orm.exc import NoResultFound

from app import app
from app.models import Poll, RawResult

from .signature import get_signature


@app.route('/polls/<poll_name>', methods=['GET'])
def polls_get(poll_name):
    try:
        poll = Poll.query.filter(Poll.slug == poll_name).one()
    except NoResultFound as e:
        abort(404)

    signature = get_signature()
    session['signature'] = signature

    q = RawResult.query.filter(
        RawResult.poll == poll,
        RawResult.signature == signature
    )
    already = RawResult.query.filter(q.exists()).scalar()

    return render_template(
        'index.html',
        poll_name=Markup(poll_name),
        already=already
    )
