# Fill the DB with fati and valve

from app import db
from app.models import Fati, Valve

for i in range(12):
    f = Fati()
    db.session.add(f)
    for j in range(8):
        v = Valve(from_fati=f)
        db.session.add(v)
db.session.commit()