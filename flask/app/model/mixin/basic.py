from ... import db
from datetime import datetime


class BasicModelMixin:
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)

    def save(self):
        db.session.add(self)
        db.session.commit()
