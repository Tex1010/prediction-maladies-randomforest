from . import db

class Patient(db.Model):
    __tablename__='patient'
    id_patient = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100))
    sexe = db.Column(db.String(10))
    date_naissance = db.Column(db.String(20))
    adresse = db.Column(db.String(200))
    telephone = db.Column(db.String(20))

    parametres = db.relationship('Parametre', backref='patient', lazy=True)
    resultats = db.relationship('Resultat', backref='patient', lazy=True) 