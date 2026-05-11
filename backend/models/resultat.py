from . import db
from datetime import datetime

class Resultat(db.Model):
    __tablename__ = 'resultat'
    id_resultat = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_patient = db.Column(db.Integer, db.ForeignKey('patient.id_patient'), nullable=False)
    
    # Probabilités (Sortie du modèle)
    risque_fievre = db.Column(db.Float)
    risque_paludisme = db.Column(db.Float)
    risque_grippe = db.Column(db.Float)
    risque_anemie = db.Column(db.Float)
    
    niveau_risque_global = db.Column(db.String(50))
    date_resultat = db.Column(db.DateTime, default=datetime.utcnow)