from app import db
from sqlalchemy.sql import func


class ValveConfiguration(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=func.now(), nullable=False)
    status = db.Column(db.String(96), nullable=False)
    configtype = db.Column(db.Integer, default=1, nullable=False) # 1 for start, 0 for end

    def __repr__(self):
        return 'Configuration at {0}: {1}'.format(self.timestamp, self.status)
