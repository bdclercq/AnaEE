from app import db
from sqlalchemy.sql import func


class ValveConfiguration(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=func.now(), nullable=False)
    status = db.Column(db.String(96), nullable=False)
    configtype = db.Column(db.Integer, default=1, nullable=False)

    def __repr__(self):
        return 'Configuration at {0}: {1}'.format(self.timestamp, self.status)
