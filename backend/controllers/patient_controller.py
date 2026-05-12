from models import db
from models.patient import Patient

def create_patient(data):
    nouveau_patient = Patient(
        nom=data.get('nom'),
        prenom=data.get('prenom'),
        sexe=data.get('sexe'),
        date_naissance=data.get('date_naissance'),
        adresse=data.get('adresse'),
        telephone=data.get('telephone')
    )

    db.session.add(nouveau_patient)
    db.session.commit()
    return nouveau_patient

def get_all_patients():
    patients = Patient.query.all()

    return [
        {
            "id_patient": p.id_patient,
            "nom": p.nom,
            "prenom":p.prenom,
            "sexe": p.sexe,
            "date_naissance": p.date_naissance,
            "adresse":p.adresse,
            "telephone":p.telephone
        } for p in patients
    ]