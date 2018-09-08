from flask import request, session, abort

from app import app, db
from app.models import results

from .signature import check_signature


@app.route('/polls/<poll_name>/results', methods=['POST'])
def results_post(poll_name):
    if request.method == 'POST':
        signature = session.get('signature', None)
        if not check_signature(signature):
            abort(403)

        json = request.get_json()

        result = results[poll_name](signature=signature, **json)
        db.session.add(result)
        db.session.commit()

        return str(result.id)


@app.route('/polls/<poll_name>/results', methods=['GET'])
def results_get(poll_name):
    return str(results[poll_name].query.all())
