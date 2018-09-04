from flask import request, session, abort
from app import app, db
from app.models import Result


@app.route('/results', methods=['POST', 'OPTIONS'])
def results_post():
    headers = {

    }
    if request.method == 'POST':
        if session.get('token', None) != 'pouet':
            abort(403)
        json = request.get_json()

        result = Result(**json)
        db.session.add(result)
        db.session.commit()

        return str(result.id), headers
    else:
        return '', headers


@app.route('/results', methods=['GET'])
def results_get():
    return str(Result.query.all())
