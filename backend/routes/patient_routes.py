from flask import Blueprint, request, jsonify
from controllers.patient_controller import create_patient, get_all_patients

patient_bp = Blueprint('patient_bp', __name__)

@patient_bp.route('/api/patients', methods=['POST'])
def add_patient():
    data = request.get_json()

    if not data or not data.get('nom'):
        return jsonify({"error": "Le nom est obligatoire"}), 400
    
    try:
        patient = create_patient(data)
        return jsonify({
            "message": "Patient créé",
            "id_patient": patient.id_patient
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@patient_bp.route('/api/patients', methods=['GET'])
def get_patients():
    try:
        patients = get_all_patients()
        return jsonify(patients), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500