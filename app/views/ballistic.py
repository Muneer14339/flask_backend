# app/views/ballistic.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.viewmodels.ballistic_viewmodel import BallisticViewModel
from app.utils.responses import ApiResponse
import logging

# Create ballistic blueprint
ballistic_bp = Blueprint('ballistic', __name__)

# Initialize ViewModel
ballistic_viewmodel = BallisticViewModel()

# DOPE Entry endpoints
@ballistic_bp.route('/dope', methods=['GET'])
@jwt_required()
def get_dope_entries():
    """Get DOPE entries for authenticated user"""
    try:
        user_id = get_jwt_identity()
        rifle_id = request.args.get('rifleId')
        return ballistic_viewmodel.handle_get_dope_entries(user_id, rifle_id)
        
    except Exception as e:
        logging.error(f"Get DOPE entries endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to get DOPE entries")

@ballistic_bp.route('/dope', methods=['POST'])
@jwt_required()
def create_dope_entry():
    """Create new DOPE entry"""
    try:
        if not request.is_json:
            return ApiResponse.validation_error("Request must be JSON")
        
        user_id = get_jwt_identity()
        request_data = request.get_json()
        return ballistic_viewmodel.handle_create_dope_entry(request_data, user_id)
        
    except Exception as e:
        logging.error(f"Create DOPE entry endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to create DOPE entry")

@ballistic_bp.route('/dope/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_dope_entry(entry_id):
    """Delete DOPE entry"""
    try:
        user_id = get_jwt_identity()
        return ballistic_viewmodel.handle_delete_dope_entry(entry_id, user_id)
        
    except Exception as e:
        logging.error(f"Delete DOPE entry endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to delete DOPE entry")

# Zero Entry endpoints
@ballistic_bp.route('/zero', methods=['GET'])
@jwt_required()
def get_zero_entries():
    """Get zero entries for authenticated user"""
    try:
        user_id = get_jwt_identity()
        rifle_id = request.args.get('rifleId')
        return ballistic_viewmodel.handle_get_zero_entries(user_id, rifle_id)
        
    except Exception as e:
        logging.error(f"Get zero entries endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to get zero entries")

@ballistic_bp.route('/zero', methods=['POST'])
@jwt_required()
def create_zero_entry():
    """Create new zero entry"""
    try:
        if not request.is_json:
            return ApiResponse.validation_error("Request must be JSON")
        
        user_id = get_jwt_identity()
        request_data = request.get_json()
        return ballistic_viewmodel.handle_create_zero_entry(request_data, user_id)
        
    except Exception as e:
        logging.error(f"Create zero entry endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to create zero entry")

@ballistic_bp.route('/zero/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_zero_entry(entry_id):
    """Delete zero entry"""
    try:
        user_id = get_jwt_identity()
        return ballistic_viewmodel.handle_delete_zero_entry(entry_id, user_id)
        
    except Exception as e:
        logging.error(f"Delete zero entry endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to delete zero entry")

# Chronograph Data endpoints
@ballistic_bp.route('/chronograph', methods=['GET'])
@jwt_required()
def get_chronograph_data():
    """Get chronograph data for authenticated user"""
    try:
        user_id = get_jwt_identity()
        rifle_id = request.args.get('rifleId')
        return ballistic_viewmodel.handle_get_chronograph_data(user_id, rifle_id)
        
    except Exception as e:
        logging.error(f"Get chronograph data endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to get chronograph data")

@ballistic_bp.route('/chronograph', methods=['POST'])
@jwt_required()
def create_chronograph_data():
    """Create new chronograph data"""
    try:
        if not request.is_json:
            return ApiResponse.validation_error("Request must be JSON")
        
        user_id = get_jwt_identity()
        request_data = request.get_json()
        return ballistic_viewmodel.handle_create_chronograph_data(request_data, user_id)
        
    except Exception as e:
        logging.error(f"Create chronograph data endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to create chronograph data")

@ballistic_bp.route('/chronograph/<data_id>', methods=['DELETE'])
@jwt_required()
def delete_chronograph_data(data_id):
    """Delete chronograph data"""
    try:
        user_id = get_jwt_identity()
        return ballistic_viewmodel.handle_delete_chronograph_data(data_id, user_id)
        
    except Exception as e:
        logging.error(f"Delete chronograph data endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to delete chronograph data")

# Ballistic Calculation endpoints
@ballistic_bp.route('/calculations', methods=['GET'])
@jwt_required()
def get_ballistic_calculations():
    """Get ballistic calculations for authenticated user"""
    try:
        user_id = get_jwt_identity()
        rifle_id = request.args.get('rifleId')
        return ballistic_viewmodel.handle_get_ballistic_calculations(user_id, rifle_id)
        
    except Exception as e:
        logging.error(f"Get ballistic calculations endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to get ballistic calculations")

@ballistic_bp.route('/calculations', methods=['POST'])
@jwt_required()
def calculate_ballistics():
    """Calculate ballistic trajectory"""
    try:
        if not request.is_json:
            return ApiResponse.validation_error("Request must be JSON")
        
        user_id = get_jwt_identity()
        request_data = request.get_json()
        return ballistic_viewmodel.handle_calculate_ballistics(request_data, user_id)
        
    except Exception as e:
        logging.error(f"Calculate ballistics endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to calculate ballistics")

@ballistic_bp.route('/calculations/<calculation_id>', methods=['DELETE'])
@jwt_required()
def delete_ballistic_calculation(calculation_id):
    """Delete ballistic calculation"""
    try:
        user_id = get_jwt_identity()
        return ballistic_viewmodel.handle_delete_ballistic_calculation(calculation_id, user_id)
        
    except Exception as e:
        logging.error(f"Delete ballistic calculation endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to delete ballistic calculation")

# Summary endpoints
@ballistic_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_ballistic_summary():
    """Get ballistic data summary for a rifle"""
    try:
        user_id = get_jwt_identity()
        rifle_id = request.args.get('rifleId')
        
        if not rifle_id:
            return ApiResponse.validation_error("Rifle ID is required")
        
        return ballistic_viewmodel.handle_get_ballistic_summary(rifle_id, user_id)
        
    except Exception as e:
        logging.error(f"Get ballistic summary endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to get ballistic summary")

@ballistic_bp.route('/all-data', methods=['GET'])
@jwt_required()
def get_all_ballistic_data():
    """Get all ballistic data for authenticated user"""
    try:
        user_id = get_jwt_identity()
        rifle_id = request.args.get('rifleId')
        return ballistic_viewmodel.handle_get_all_ballistic_data(user_id, rifle_id)
        
    except Exception as e:
        logging.error(f"Get all ballistic data endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to get ballistic data")

# Health check for ballistic service
@ballistic_bp.route('/health', methods=['GET'])
def ballistic_health():
    """Ballistic service health check"""
    return ApiResponse.success(
        data={'service': 'ballistic', 'status': 'healthy'},
        message="Ballistic service is running"
    )