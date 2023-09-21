from datetime import datetime

from settings import MAX_USER_SHORT

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text)
    short = db.Column(db.String(MAX_USER_SHORT), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def from_dict(self, data):
        for field in ['url', 'custom_id']:
            if field in data:
                setattr(self, field, data[field])