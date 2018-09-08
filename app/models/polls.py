import json

from app import db



class Poll(db.Model):
    __tablename__ = 'polls'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    json_dict = db.Column(db.PickleType)

    @staticmethod
    def import_from_local(name, json_path):
        with open(json_path, 'r') as f:
            content = json.load(f)

        p = Poll(name=name, json_dict=content)
        db.session.add(p)
        db.session.commit()
        return p

    def __repr__(self):
        return '<Poll {}>'.format(self.name)
