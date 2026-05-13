from flask import request, jsonify
from models import db, Patient, Parametre, Resultat
import joblib
import numpy as np

# Charge le modèle au démarrage
model = joblib.load('model_data/random_forest_model.pkl')

def create_full_consultation():
    data = request.json
    try:
        # 1. Insertion PATIENT
        new_patient = Patient(
            nom=data['nom'],
            prenom=data.get('prenom'),
            sexe=data.get('sexe'),
            date_naissance=data.get('date_naissance'),
            adresse=data.get('adresse'),
            telephone=data.get('telephone')
        )
        db.session.add(new_patient)
        db.session.flush() #Récuperer l'ID sans commit

        # 2. Insertion PARAMETRE
        new_params = Parametre(
            id_patient=new_patient.id_patient,
            age=int(data['age']),
            temperature=float(data['temperature']),
            tension_arterielle=int(data['tension_arterielle']),
            poids=int(data['poids']),
            taille=int(data['taille']),
            fatigue=bool(data.get('fatigue')),
            frissons=bool(data.get('frissons')),
            toux=bool(data.get('toux')),
            maux_tete=bool(data.get('maux_tete')),
            vomissement=bool(data.get('vomissement'))
        )
        db.session.add(new_params)

        # 3. CALCUL AUTOMATIQUE (IA)
        # Préparer les données pour le Random Forest
        input_data = [[
            new_params.age, new_params.temperature, new_params.tension_arterielle,
            int(new_params.fatigue), int(new_params.frissons), 
            int(new_params.toux), int(new_params.maux_tete), 
            int(new_params.vomissement)
        ]]
        
        # Obtenir les probabilités (pourcentages)
        # predict_proba renvoie une liste de tableaux (un par maladie)
        probas = model.predict_proba(input_data)
        
        # Extraction des probabilités du "classe 1" (Malade)
        # L'index [0][0][1] dépend de la structure de sortie de scikit-learn
        res_fievre = round(probas[0][0][1] * 100, 2)
        res_palu = round(probas[1][0][1] * 100, 2)
        res_grippe = round(probas[2][0][1] * 100, 2)
        res_anemie = round(probas[3][0][1] * 100, 2)

        # 4. Insertion RESULTAT
        score_global = (res_fievre + res_palu + res_grippe + res_anemie) / 4
        niveau = "Élevé" if score_global > 50 else "Moyen" if score_global > 20 else "Faible"

        new_result = Resultat(
            id_patient=new_patient.id_patient,
            risque_fievre=res_fievre,
            risque_paludisme=res_palu,
            risque_grippe=res_grippe,
            risque_anemie=res_anemie,
            niveau_risque_global=niveau
        )
        db.session.add(new_result)

        # TOUT VALIDER
        db.session.commit()

        return jsonify({
            "status": "success",
            "patient_id": new_patient.id_patient,
            "predictions": {
                "fievre": res_fievre,
                "paludisme": res_palu,
                "grippe": res_grippe,
                "anemie": res_anemie,
                "niveau": niveau
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

def get_consultation(patient_id):
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({"error": "Patient non trouvé"}), 404
        
        last_params = Parametre.query.filter_by(id_patient=patient_id).order_by(Parametre.id_parametre.desc()).first()

        last_result = Resultat.query.filter_by(id_patient=patient_id).order_by(Resultat.id_resultat.desc()).first()

        return jsonify({
            "patient": {
                "nom" : patient.nom,
                "prenom": patient.prenom,
                "sexe": patient.sexe,
                "adresse": patient.adresse,
                "telephone": patient.telephone
            },
            "parametre": {
                "age": last_params.age if last_params else None,
                "temperature": last_params.temperature if last_params else None,
                "tension_arterielle": last_params.tension_arterielle if last_params else None,
                "poids": last_params.poids if last_params else None
            },
            "resultat": {
                "risque_fievre": last_result.risque_fievre if last_result else None,
                "risque_paludisme": last_result.risque_paludisme if last_result else None,
                "risque_grippe": last_result.risque_grippe if last_result else None,
                "risque_anemie": last_result.risque_anemie if last_result else None,
                "niveau_risque_global": last_result.niveau_risque_global if last_result else None,
                "date_resultat": last_result.date_resultat if last_result else None
            }
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500