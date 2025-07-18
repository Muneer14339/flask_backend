from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.viewmodels.auth_viewmodel import AuthViewModel
from app.utils.responses import ApiResponse
import logging

# Create auth blueprint
auth_bp = Blueprint('auth', __name__)

# Initialize ViewModel
auth_viewmodel = AuthViewModel()

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    User registration endpoint
    Expected JSON: {
        "fullName": "string",
        "email": "string", 
        "password": "string"
    }
    """
    try:
        if not request.is_json:
            return ApiResponse.validation_error("Request must be JSON")
        
        request_data = request.get_json()
        return auth_viewmodel.handle_user_registration(request_data)
        
    except Exception as e:
        logging.error(f"Signup endpoint error: {str(e)}")
        return ApiResponse.server_error("Signup failed")

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login endpoint
    Expected JSON: {
        "email": "string",
        "password": "string"
    }
    """
    try:
        if not request.is_json:
            return ApiResponse.validation_error("Request must be JSON")
        
        request_data = request.get_json()
        return auth_viewmodel.handle_user_login(request_data)
        
    except Exception as e:
        logging.error(f"Login endpoint error: {str(e)}")
        return ApiResponse.server_error("Login failed")

@auth_bp.route('/google-signin', methods=['POST'])
def google_signin():
    """
    Google sign-in endpoint
    Expected JSON: {
        "googleToken": "string"
    }
    """
    try:
        if not request.is_json:
            return ApiResponse.validation_error("Request must be JSON")
        
        request_data = request.get_json()
        return auth_viewmodel.handle_google_signin(request_data)
        
    except Exception as e:
        logging.error(f"Google sign-in endpoint error: {str(e)}")
        return ApiResponse.server_error("Google sign-in failed")

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Forgot password endpoint
    Expected JSON: {
        "email": "string"
    }
    """
    try:
        if not request.is_json:
            return ApiResponse.validation_error("Request must be JSON")
        
        request_data = request.get_json()
        return auth_viewmodel.handle_forgot_password(request_data)
        
    except Exception as e:
        logging.error(f"Forgot password endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to process password reset request")

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """
    OTP verification endpoint
    Expected JSON: {
        "email": "string",
        "otp": "string"
    }
    """
    try:
        if not request.is_json:
            return ApiResponse.validation_error("Request must be JSON")
        
        request_data = request.get_json()
        return auth_viewmodel.handle_verify_otp(request_data)
        
    except Exception as e:
        logging.error(f"Verify OTP endpoint error: {str(e)}")
        return ApiResponse.server_error("OTP verification failed")

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """
    Reset password endpoint
    Expected JSON: {
        "email": "string",
        "resetToken": "string",
        "newPassword": "string"
    }
    """
    try:
        if not request.is_json:
            return ApiResponse.validation_error("Request must be JSON")
        
        request_data = request.get_json()
        return auth_viewmodel.handle_reset_password(request_data)
        
    except Exception as e:
        logging.error(f"Reset password endpoint error: {str(e)}")
        return ApiResponse.server_error("Password reset failed")

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current user endpoint (protected)
    Requires JWT token in Authorization header
    """
    try:
        user_id = get_jwt_identity()
        return auth_viewmodel.handle_get_current_user(user_id)
        
    except Exception as e:
        logging.error(f"Get current user endpoint error: {str(e)}")
        return ApiResponse.server_error("Failed to get user information")

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh token endpoint
    Requires refresh token in Authorization header
    """
    try:
        user_id = get_jwt_identity()
        return auth_viewmodel.handle_refresh_token(user_id)
        
    except Exception as e:
        logging.error(f"Refresh token endpoint error: {str(e)}")
        return ApiResponse.server_error("Token refresh failed")

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout endpoint (protected)
    Note: JWT tokens are stateless, so logout is handled client-side
    This endpoint is for future token blacklisting if needed
    """
    try:
        # For now, just return success
        # In future, can add token blacklisting logic here
        return ApiResponse.success(message="Logged out successfully")
        
    except Exception as e:
        logging.error(f"Logout endpoint error: {str(e)}")
        return ApiResponse.server_error("Logout failed")

# Health check for auth service
@auth_bp.route('/health', methods=['GET'])
def auth_health():
    """Auth service health check"""
    return ApiResponse.success(
        data={'service': 'auth', 'status': 'healthy'},
        message="Auth service is running"
    )