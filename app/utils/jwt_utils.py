from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from datetime import timedelta
from flask import current_app

class JWTUtils:
    """JWT utility functions"""
    
    @staticmethod
    def generate_tokens(user_id):
        """Generate access and refresh tokens for user"""
        additional_claims = {
            "user_id": user_id,
            "type": "access"
        }
        
        access_token = create_access_token(
            identity=user_id,
            expires_delta=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
            additional_claims=additional_claims
        )
        
        refresh_token = create_refresh_token(
            identity=user_id,
            expires_delta=current_app.config['JWT_REFRESH_TOKEN_EXPIRES']
        )
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': int(current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds())
        }
    
    @staticmethod
    def get_current_user_id():
        """Get current user ID from JWT token"""
        return get_jwt_identity()
    
    @staticmethod
    def refresh_access_token(user_id):
        """Generate new access token using refresh token"""
        additional_claims = {
            "user_id": user_id,
            "type": "access"
        }
        
        new_token = create_access_token(
            identity=user_id,
            expires_delta=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
            additional_claims=additional_claims
        )
        
        return {
            'access_token': new_token,
            'expires_in': int(current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds())
        }