# app/views/loadout.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.viewmodels.loadout_viewmodel import LoadoutViewModel
from app.utils.responses import ApiResponse
import logging

# Create loadout blueprint
loadout_bp = Blueprint('loadout', __name__)

# Initialize ViewModel
loadout_viewmodel = LoadoutViewModel()

# Rifle endpoints
@loadout_bp.route('/rifles', methods=['GET'])
@jwt_required()
def get_rifles():
    """Get all rifles for authenticated user"""
    try:
        user_id = get_jwt_identity()
        return loadout_viewmodel.handle_get_rifles(user_id)
        
    except Exception as e:
        logging.error(f"Get rifles endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to get rifles")

@loadout_bp.route('/rifles', methods=['POST'])
@jwt_required()
def create_rifle():
    """Create a new rifle"""
    try:
        if not request.is_json:
            return ApiResponse.validation_error("Request must be JSON")
        
        user_id = get_jwt_identity()
        request_data = request.get_json()
        return loadout_viewmodel.handle_create_rifle(request_data, user_id)
        
    except Exception as e:
        logging.error(f"Create rifle endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to create rifle")

@loadout_bp.route('/rifles/<rifle_id>', methods=['GET'])
@jwt_required()
def get_rifle(rifle_id):
    """Get a specific rifle"""
    try:
        user_id = get_jwt_identity()
        return loadout_viewmodel.handle_get_rifle(rifle_id, user_id)
        
    except Exception as e:
        logging.error(f"Get rifle endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to get rifle")

@loadout_bp.route('/rifles/<rifle_id>', methods=['PUT'])
@jwt_required()
def update_rifle(rifle_id):
    """Update a rifle"""
    try:
        if not request.is_json:
            return ApiResponse.validation_error("Request must be JSON")
        
        user_id = get_jwt_identity()
        request_data = request.get_json()
        return loadout_viewmodel.handle_update_rifle(rifle_id, request_data, user_id)
        
    except Exception as e:
        logging.error(f"Update rifle endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to update rifle")

@loadout_bp.route('/rifles/<rifle_id>', methods=['DELETE'])
@jwt_required()
def delete_rifle(rifle_id):
    """Delete a rifle"""
    try:
        user_id = get_jwt_identity()
        return loadout_viewmodel.handle_delete_rifle(rifle_id, user_id)
        
    except Exception as e:
        logging.error(f"Delete rifle endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to delete rifle")

@loadout_bp.route('/rifles/set-active', methods=['POST'])
@jwt_required()
def set_active_rifle():
    """Set active rifle"""
    try:
        if not request.is_json:
            return ApiResponse.validation_error("Request must be JSON")
        
        user_id = get_jwt_identity()
        request_data = request.get_json()
        return loadout_viewmodel.handle_set_active_rifle(request_data, user_id)
        
    except Exception as e:
        logging.error(f"Set active rifle endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to set active rifle")

# Rifle association endpoints
@loadout_bp.route('/rifles/<rifle_id>/scope', methods=['PUT'])
@jwt_required()
def update_rifle_scope(rifle_id):
    """Update rifle's associated scope"""
    try:
        if not request.is_json:
            return ApiResponse.validation_error("Request must be JSON")
        
        user_id = get_jwt_identity()
        request_data = request.get_json()
        return loadout_viewmodel.handle_update_rifle_scope(rifle_id, request_data, user_id)
        
    except Exception as e:
        logging.error(f"Update rifle scope endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to update rifle scope")

@loadout_bp.route('/rifles/<rifle_id>/ammunition', methods=['PUT'])
@jwt_required()
def update_rifle_ammunition(rifle_id):
    """Update rifle's associated ammunition"""
    try:
        if not request.is_json:
            return ApiResponse.validation_error("Request must be JSON")
        
        user_id = get_jwt_identity()
        request_data = request.get_json()
        return loadout_viewmodel.handle_update_rifle_ammunition(rifle_id, request_data, user_id)
        
    except Exception as e:
        logging.error(f"Update rifle ammunition endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to update rifle ammunition")

# Ammunition endpoints
@loadout_bp.route('/ammunition', methods=['GET'])
@jwt_required()
def get_ammunition():
    """Get all ammunition for authenticated user"""
    try:
        user_id = get_jwt_identity()
        return loadout_viewmodel.handle_get_ammunition(user_id)
        
    except Exception as e:
        logging.error(f"Get ammunition endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to get ammunition")

@loadout_bp.route('/ammunition', methods=['POST'])
@jwt_required()
def create_ammunition():
    """Create new ammunition"""
    try:
        if not request.is_json:
            return ApiResponse.validation_error("Request must be JSON")
        
        user_id = get_jwt_identity()
        request_data = request.get_json()
        return loadout_viewmodel.handle_create_ammunition(request_data, user_id)
        
    except Exception as e:
        logging.error(f"Create ammunition endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to create ammunition")

@loadout_bp.route('/ammunition/<ammo_id>', methods=['PUT'])
@jwt_required()
def update_ammunition(ammo_id):
    """Update ammunition"""
    try:
        if not request.is_json:
            return ApiResponse.validation_error("Request must be JSON")
        
        user_id = get_jwt_identity()
        request_data = request.get_json()
        return loadout_viewmodel.handle_update_ammunition(ammo_id, request_data, user_id)
        
    except Exception as e:
        logging.error(f"Update ammunition endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to update ammunition")

@loadout_bp.route('/ammunition/<ammo_id>', methods=['DELETE'])
@jwt_required()
def delete_ammunition(ammo_id):
    """Delete ammunition"""
    try:
        user_id = get_jwt_identity()
        return loadout_viewmodel.handle_delete_ammunition(ammo_id, user_id)
        
    except Exception as e:
        logging.error(f"Delete ammunition endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to delete ammunition")

# Scope endpoints
@loadout_bp.route('/scopes', methods=['GET'])
@jwt_required()
def get_scopes():
    """Get all scopes for authenticated user"""
    try:
        user_id = get_jwt_identity()
        return loadout_viewmodel.handle_get_scopes(user_id)
        
    except Exception as e:
        logging.error(f"Get scopes endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to get scopes")

@loadout_bp.route('/scopes', methods=['POST'])
@jwt_required()
def create_scope():
    """Create new scope"""
    try:
        if not request.is_json:
            return ApiResponse.validation_error("Request must be JSON")
        
        user_id = get_jwt_identity()
        request_data = request.get_json()
        return loadout_viewmodel.handle_create_scope(request_data, user_id)
        
    except Exception as e:
        logging.error(f"Create scope endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to create scope")

@loadout_bp.route('/scopes/<scope_id>', methods=['PUT'])
@jwt_required()
def update_scope(scope_id):
    """Update scope"""
    try:
        if not request.is_json:
            return ApiResponse.validation_error("Request must be JSON")
        
        user_id = get_jwt_identity()
        request_data = request.get_json()
        return loadout_viewmodel.handle_update_scope(scope_id, request_data, user_id)
        
    except Exception as e:
        logging.error(f"Update scope endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to update scope")

@loadout_bp.route('/scopes/<scope_id>', methods=['DELETE'])
@jwt_required()
def delete_scope(scope_id):
    """Delete scope"""
    try:
        user_id = get_jwt_identity()
        return loadout_viewmodel.handle_delete_scope(scope_id, user_id)
        
    except Exception as e:
        logging.error(f"Delete scope endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to delete scope")

# Maintenance endpoints
@loadout_bp.route('/maintenance', methods=['GET'])
@jwt_required()
def get_maintenance():
    """Get all maintenance tasks for authenticated user"""
    try:
        user_id = get_jwt_identity()
        return loadout_viewmodel.handle_get_maintenance(user_id)
        
    except Exception as e:
        logging.error(f"Get maintenance endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to get maintenance tasks")

@loadout_bp.route('/maintenance', methods=['POST'])
@jwt_required()
def create_maintenance():
    """Create new maintenance task"""
    try:
        if not request.is_json:
            return ApiResponse.validation_error("Request must be JSON")
        
        user_id = get_jwt_identity()
        request_data = request.get_json()
        return loadout_viewmodel.handle_create_maintenance(request_data, user_id)
        
    except Exception as e:
        logging.error(f"Create maintenance endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to create maintenance task")

@loadout_bp.route('/maintenance/<maintenance_id>/complete', methods=['POST'])
@jwt_required()
def complete_maintenance(maintenance_id):
    """Complete maintenance task"""
    try:
        user_id = get_jwt_identity()
        return loadout_viewmodel.handle_complete_maintenance(maintenance_id, user_id)
        
    except Exception as e:
        logging.error(f"Complete maintenance endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to complete maintenance task")

@loadout_bp.route('/maintenance/<maintenance_id>', methods=['DELETE'])
@jwt_required()
def delete_maintenance(maintenance_id):
    """Delete maintenance task"""
    try:
        user_id = get_jwt_identity()
        return loadout_viewmodel.handle_delete_maintenance(maintenance_id, user_id)
        
    except Exception as e:
        logging.error(f"Delete maintenance endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to delete maintenance task")

# Summary endpoints
@loadout_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_loadout_summary():
    """Get complete loadout summary"""
    try:
        user_id = get_jwt_identity()
        return loadout_viewmodel.handle_get_loadout_summary(user_id)
        
    except Exception as e:
        logging.error(f"Get loadout summary endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to get loadout summary")

# Health check for loadout service
@loadout_bp.route('/health', methods=['GET'])
def loadout_health():
    """Loadout service health check"""
    return ApiResponse.success(
        data={'service': 'loadout', 'status': 'healthy'},
        message="Loadout service is running"
    )