from flask import request, session, abort, Response

from app import app, db
from app.models import Poll, RawResult

from .signature import check_signature


@app.route('/polls/<poll_name>/results', methods=['POST'])
def results_post(poll_name):
    if request.method == 'POST':
        signature = session.get('signature', None)
        if not check_signature(signature):
            abort(403)

        poll = Poll.query.filter(Poll.slug == poll_name).one()
        poll.raw_results.append(
            RawResult(signature=signature, raw=request.get_json())
        )
        db.session.add(poll)
        db.session.commit()

        return "", 201, {}


@app.route('/polls/<poll_name>/results', methods=['GET'])
def results_get(poll_name):
    return '\n'.join([str(r) for r in RawResult.query.all()])
