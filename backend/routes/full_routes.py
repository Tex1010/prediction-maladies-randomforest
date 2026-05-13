from flask import Blueprint
from controllers.full_controller import create_full_consultation, get_consultation

full_bp = Blueprint('full_bp', __name__)

full_bp.route('/api/consultation', methods=['POST'])(create_full_consultation)

@full_bp.route('/api/consultation/<int:patient_id>', methods=['GET'])
def get_consultations(patient_id):
    return get_consultation(patient_id)