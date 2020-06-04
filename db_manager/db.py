from pony.orm import *
from db_manager import db, Patient, Session, Data
from datetime import datetime

class DB:
    def __init__(self):
        db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
        db.generate_mapping(create_tables=True)
    
    def get_patient(self, name):
        uid = name.split("_")
        if len(uid) == 1:
            with db_session:
                patient_number = Patient.select().count()
                uid = patient_number + 1000
                Patient(name=name, uid=uid)
                return uid
        else:
            try:
                return self.find_patient(uid[1])
            except:
                with db_session:
                    patient_number = Patient.select().count()
                    uid = patient_number + 1000
                    Patient(name=name, uid=uid)
                    return uid

    def find_patient(self, uid):
        with db_session:
            uid = select(p.uid for p in Patient if p.uid == uid[1])[:]
            return uid
    
    def create_session(self, patient_uid):
        #sess = None
        with db_session:
            session_number = Session.select().count()
            uid = session_number + 1000
            Session(expr_date=datetime.today(), uid=uid, patient=Patient.get(uid=patient_uid))
            return uid
    
    def write_meas(self, session_uid, meas, time, stress):
        #data = None
        with db_session:
            Data(rr=meas["rr"], hr=meas["hr"], stress=stress, time=datetime.utcfromtimestamp(time), session=Session.get(uid=session_uid))

    def expr_duration(self, duration, session_uid):
        with db_session:
            sess = Session.get(uid=session_uid)
            sess.duration = datetime.utcfromtimestamp(duration)
