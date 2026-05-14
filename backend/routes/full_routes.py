from flask import Blueprint
from controllers.full_controller import create_full_consultation, get_consultation, update_consultation_data, get_all_consultations, delete_consultation

full_bp = Blueprint('full_bp', __name__)

full_bp.route('/api/consultation', methods=['POST'])(create_full_consultation)

@full_bp.route('/api/consultation/<int:patient_id>', methods=['GET'])
def get_consultations(patient_id):
    return get_consultation(patient_id)

@full_bp.route('/api/consultation/<int:patient_id>', methods=['PUT'])
def update_consultation(patient_id):
    return update_consultation_data(patient_id)

@full_bp.route('/api/consultations', methods=['GET'])
def list_consultations():
    return get_all_consultations()

@full_bp.route('/api/consultation/<int:id_resultat>', methods=['DELETE'])
def delete_cons(id_resultat):
    return delete_consultation(id_resultat)