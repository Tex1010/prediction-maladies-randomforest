from . import db
from datetime import datetime

class Parametre(db.Model):
    __tablename__ = 'parametre'
    id_parametre = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_patient = db.Column(db.Integer, db.ForeignKey('patient.id_patient'), nullable=False)

    age = db.Column(db.Integer)
    tension_arterielle = db.Column(db.Integer)
    temperature = db.Column(db.Integer)
    poids = db.Column(db.Integer)
    taille = db.Column(db.Integer)
    
    # Symptômes (Boolean pour le Random Forest)
    fatigue = db.Column(db.Boolean, default=False)
    frissons = db.Column(db.Boolean, default=False)
    toux = db.Column(db.Boolean, default=False)
    maux_tete = db.Column(db.Boolean, default=False)
    vomissement = db.Column(db.Boolean, default=False)
    
    date_enregistrement = db.Column(db.DateTime, default=datetime.utcnow)