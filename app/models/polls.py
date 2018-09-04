import json
from datetime import datetime

from slugify import slugify

from app import db


class Poll(db.Model):
    __tablename__ = 'polls'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String, unique=True)
    name = db.Column(db.String)

    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    json_dict = db.Column(db.PickleType)

    @staticmethod
    def import_from_local(long_name, json_path):
        with open(json_path, 'r') as f:
            content = json.load(f)

        p = Poll(
            slug=slugify(long_name),
            name=long_name,
            json_dict=content
        )

        db.session.add(p)
        db.session.commit()
        return p

    def __repr__(self):
        return '<Poll (slug="{}">'.format(self.slug)
