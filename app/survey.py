from app import db


class Survey:
    def __init__(self, json):
        self._json = json
        self._columns = self._get_columns(json)

    def _get_columns(self, json):
        questions = json['questions']
        return {q['name']: self._get_db_type(q) for q in questions}

    @classmethod
    def _get_db_type(cls, item):
        """
        :param item: the survey item
        :return: the db type that corresponds to `item`
        """
        if item['type'] == 'radiogroup':
            return cls._guess_db_type_from_choices(item['choices'])
        else:
            raise ValueError(
                "Failed to get DB type from item : {}".format(item)
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