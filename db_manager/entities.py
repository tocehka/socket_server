from pony.orm import *
from datetime import datetime

db = Database()

class Patient(db.Entity):
    name = Required(str)
    uid = Required(int, unique=True)
    sessions = Set(lambda: Session)

class Session(db.Entity):
    expr_date = Required(datetime)
    uid = Required(int, unique=True)
    duration = Optional(datetime)
    patient = Required(Patient)
    data = Set(lambda: Data)

class Data(db.Entity):
    rr = Required(float)
    hr = Required(int)
    stress = Required(bool)
    time = Required(datetime)
    session = Required(Session)
