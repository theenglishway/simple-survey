import json

from app import app
from app.models import Poll


@app.route('/surveys/<survey_name>', methods=['GET'])
def get_survey(survey_name):
    poll = Poll.query.filter(Poll.name == survey_name).first()
    return json.dumps(poll.json_dict)
