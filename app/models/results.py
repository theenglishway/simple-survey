from sqlalchemy.ext.declarative import declared_attr

from app import db


class JSONSurvey:
    def __init__(self, json):
        self._json = json
        self._columns = self._get_columns(json)

    def _get_columns(self, json):
        try:
            cols = self._columns_from_questions(json['questions'])
        except KeyError as e:
            cols = self._columns_from_pages(json['pages'])

        return cols

    def _columns_from_questions(self, d):
        return {q['name']: self._get_db_type(q) for q in d}

    def _columns_from_pages(self, d):
        return {q['name']: self._get_db_type(q) for p in d for q in p['elements']}

    @classmethod
    def _get_db_type(cls, item):
        """
        :param item: the survey item
        :return: the db type that corresponds to `item`
        """
        t = item['type']
        if t == 'radiogroup' or t == 'dropdown':
            return cls._guess_db_type_from_choices(item['choices'])
        elif t == 'text' or t == 'comment':
            return db.Text
        elif t == 'rating':
            return db.Integer
        elif t == 'boolean':
            return db.Boolean
        elif t == 'matrix':
            return db.PickleType
        elif t == 'checkbox' or t == 'html':
            return db.String
        elif t == 'file':
            raise ValueError(
                "Item type '{}' is not supported".format(t)
            )
        else:
            raise ValueError(
                "Failed to get DB type from unknown item type '{}'".format(t)
            )

    @staticmethod
    def _guess_db_type_from_choices(choices):
        """
        :param choices: the list of choices of a survey question
        :return: the db type that was guessed from the list of choices
        """
        converters = (
            (db.Float, float),
            (db.Integer, int),
            (db.String, str)
        )

        for db_type, conv_fn in converters:
            try:
                for c in choices:
                    value = c['value'] if isinstance(c, dict) else c
                    conv_fn(value)
                return db_type
            except ValueError:
                continue

        raise TypeError(
            "Failed to guess type from choices : {}".format(choices)
        )

    @property
    def columns(self):
        return self._columns


class ResultMixin:
    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def raw_id(cls):
        return db.Column(
            db.Integer,
            db.ForeignKey('raw_results.id'),
            nullable=False,
            unique=True
        )

    @declared_attr
    def raw(cls):
        return db.relationship("RawResult")

    @classmethod
    def from_raw(cls, raw_result):
        return cls(raw=raw_result, **raw_result.raw)

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.id)


def get_result_model(poll):
    """
    :param poll: the poll instance for which results should be stored
    :return: a SQLAlchemy model with a database column per survey question
    """
    survey = JSONSurvey(poll.json_dict)
    snake_name = poll.slug.replace('-', '_')

    attrs = {k: db.Column(c) for k, c in survey.columns.items()}
    attrs.update({
        '__tablename__': 'results_{}'.format(snake_name),
    })

    return type(
        'Result{}'.format(snake_name.capitalize()),
        (db.Model, ResultMixin),
        attrs
    )
