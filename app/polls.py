from flask import session, render_template, Markup

from app import app, db
from app.models import results

from .signature import get_signature


@app.route('/polls/<poll_name>', methods=['GET'])
def polls_get(poll_name):
    poll_class = results[poll_name]
    signature = get_signature()

    session['signature'] = signature
    q = poll_class.query.filter(poll_class.signature == signature)
    already = poll_class.query.filter(q.exists()).scalar()

    return render_template(
        'index.html',
        poll_name=Markup(poll_name),
        already=already
    )
