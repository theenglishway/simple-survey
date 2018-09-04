from datetime import datetime

from app import db


class RawResult(db.Model):
    __tablename__ = 'raw_results'
    __table_args__ = (
        db.UniqueConstraint(
            'poll_id', 'signature'
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'), nullable=False)

    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    signature = db.Column(db.String, unique=True)

    raw = db.Column(db.PickleType)
    converted = db.Column(db.Boolean, default=False)

    poll = db.relationship('Poll', backref=db.backref('raw_results', lazy=True))

    def __repr__(self):
        return "<RawResult (poll='{}', id={}, {}converted)>".format(
            self.poll.slug, self.id, '' if self.converted else 'not '
        )
