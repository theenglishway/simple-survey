import json

from app import db
from app.survey import Survey


class ResultBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<SurveyResult {}>'.format(self.id)

    @staticmethod
    def get_complete_model(json_path):
        """
        :param json_path: the path to the JSON-file containing the survey
        questions
        :return: a model that derives from `ResultBase` with a database column
        for each survey question
        """
        with open(json_path, 'r') as f:
            content = json.load(f)

        survey = Survey(content)

        return type(
            'Result',
            (ResultBase,),
            {k: db.Column(c) for k, c in survey.columns.items()}
        )

Result = ResultBase.get_complete_model('app/static/survey.json')
