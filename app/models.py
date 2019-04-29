from app import db
from sqlalchemy.sql import func


class ValveConfiguration(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=func.now(), nullable=False)
    status = db.Column(db.BLOB, nullable=False)

    def __repr__(self):
        return 'Valve {0} has status {1} at {2}'.format(self.id, self.status, self.timestamp)

# Voor parsen: statussen moeten per timestamp komen
# BLOB == bytearray(16)