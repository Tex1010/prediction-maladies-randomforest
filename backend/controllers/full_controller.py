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
       
        scores = {
            "la fièvre" : round(probas[0][0][1] * 100, 2),
            "la paludisme" : round(probas[1][0][1] * 100, 2),
            "la grippe" : round(probas[2][0][1] * 100, 2),
            "l'anemie" : round(probas[3][0][1] * 100, 2)
        }

        # D. GÉNÉRATION DU MESSAGE DE DIAGNOSTIC UNIQUE
        # On ne liste que les maladies ayant un risque significatif (> 25%)
        risques_detectes = [f"{m} ({s}%)" for m, s in scores.items() if s > 25]

        if not risques_detectes:
            message_unique = "Analyse terminée : Aucun risque majeur détecté. Les paramètres cliniques sont stables."
        else:
            liste_maladies = ", ".join(risques_detectes)
            message_unique = f"Analyse terminée : Le patient présente des risques significatifs pour {liste_maladies}. Une consultation médicale est recommandée."
        

       

        new_result = Resultat(
            id_patient=new_patient.id_patient,
            risque_fievre=scores["la fièvre"],
            risque_paludisme=scores["la paludisme"],
            risque_grippe=scores["la grippe"],
            risque_anemie=scores["l'anemie"],
            niveau_risque_global=message_unique
        )
        db.session.add(new_result)

        # TOUT VALIDER
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": message_unique,
            "id_patient": new_patient.id_patient,
            "id_resultat": new_result.id_resultat
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

def update_consultation_data(patient_id):
    data = request.json
    try:
        patient = Patient.query.get(patient_id)
        if not patient: 
            return jsonify({'error': "Patient non trouvé"}), 404
        
        last_params = Parametre.query.filter_by(id_patient=patient_id).order_by(Parametre.id_parametre.desc()).first()

        if 'nom' in data: patient.nom = data['nom']
        if 'prenom' in data: patient.prenom = data['prenom']
        if 'sexe' in data: patient.sexe = data['sexe']
        if 'date_naissance' in data: patient.date_naissance = data['date_naissance']
        if 'adresse' in data: patient.adresse = data['adresse']
        if 'telephone' in data: patient.telephone = data['telephone']

        if last_params:
            if 'age' in data: last_params.age = int(data['age'])
            if 'tension_arterielle' in data: last_params.tension_arterielle = int(data['tension_arterielle'])
            if 'temperature' in data: last_params.temperature = int(data['temperature'])
            if 'poids' in data: last_params.poids = int(data['poids'])
            if 'taille' in data: last_params.taille = int(data['taille'])
            if 'fatigue' in data: last_params.fatigue = bool(data['fatigue'])
            if 'frissons' in data: last_params.frissons = bool(data['frissons'])
            if 'toux' in data: last_params.toux = bool(data['toux'])
            if 'maux_tete' in data: last_params.maux_tete = bool(data['maux_tete'])
            if 'vomissement' in data: last_params.vomissement = bool(data['vomissement'])
        
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Informations du patient et paramètre mis à jour"
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
def get_all_consultations():
    try:
        results = Resultat.query.order_by(Resultat.date_resultat.desc()).all()
        output = []

        for r in results:
            p = Parametre.query.filter_by(id_patient=r.id_patient).order_by(Parametre.id_parametre.desc()).first()

            output.append({
                "id_resultat": r.id_resultat,
                "date": r.date_resultat.strftime("%d/%m/%Y %H:%M") if r.date_resultat else None,
                "risque_fievre": r.risque_fievre,
                "risque_paludisme": r.risque_paludisme,
                "risque_grippe": r.risque_grippe,
                "risque_anemie": r.risque_anemie,
                # On ne ferme pas l'accolade ici !

                "patient": {
                    "id": r.patient.id_patient,
                    "nom": r.patient.nom,
                    "prenom": r.patient.prenom,
                    "sexe": r.patient.sexe,
                    "telephone": r.patient.telephone,
                    "adresse": r.patient.adresse
                },

                "parametres": {
                    "age": p.age if p else None,
                    "tension_arterielle": p.tension_arterielle if p else None,
                    "temperature": p.temperature if p else None,
                    "poids": p.poids if p else None,
                    "taille": p.taille if p else None,
                    "fatigue": p.fatigue if p else None,
                    "frissons": p.frissons if p else None,
                    "toux": p.toux if p else None,
                    "maux_tete": p.maux_tete if p else None,
                    "vomissement": p.vomissement if p else None,
                },
                "diagnostic": r.niveau_risque_global
            }) # On ferme l'accolade ici, à la fin de l'objet
            
        return jsonify(output), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_consultation(id_resultat):
    try:
        resultat = Resultat.query.get(id_resultat)

        if not resultat:
            return jsonify({"error": "Résultat non trouvé"}), 404
        
        db.session.delete(resultat)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": f"La consultation {id_resultat} a été supprimée avec succès"
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500