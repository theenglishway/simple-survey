import json

from app import app
from app.models import Poll


@app.route('/surveys/<survey_slug>', methods=['GET'])
def get_survey(survey_slug):
    poll = Poll.query.filter(Poll.slug == survey_slug).first()
    return json.dumps(poll.json_dict)
