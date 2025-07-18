from flask import jsonify

class ApiResponse:
    """Standardized API response utility"""
    
    @staticmethod
    def success(data=None, message="Success", status_code=200):
        """Return success response"""
        response = {
            "success": True,
            "message": message
        }
        
        if data is not None:
            response["data"] = data
        
        return jsonify(response), status_code
    
    @staticmethod
    def error(message="An error occurred", status_code=400, error_code=None):
        """Return error response"""
        response = {
            "success": False,
            "message": message
        }
        
        if error_code:
            response["error_code"] = error_code
        
        return jsonify(response), status_code
    
    @staticmethod
    def validation_error(message="Validation failed", errors=None, status_code=422):
        """Return validation error response"""
        response = {
            "success": False,
            "message": message
        }
        
        if errors:
            response["errors"] = errors
        
        return jsonify(response), status_code
    
    @staticmethod
    def unauthorized(message="Unauthorized access"):
        """Return unauthorized response"""
        return ApiResponse.error(message, 401, "UNAUTHORIZED")
    
    @staticmethod
    def forbidden(message="Access forbidden"):
        """Return forbidden response"""
        return ApiResponse.error(message, 403, "FORBIDDEN")
    
    @staticmethod
    def not_found(message="Resource not found"):
        """Return not found response"""
        return ApiResponse.error(message, 404, "NOT_FOUND")
    
    @staticmethod
    def server_error(message="Internal server error"):
        """Return server error response"""
        return ApiResponse.error(message, 500, "INTERNAL_SERVER_ERROR")
    
    @staticmethod
    def auth_success(user, tokens, message="Authentication successful"):
        """Return authentication success response"""
        return ApiResponse.success(
            data={
                "user": user.to_flutter_dict(),
                "tokens": tokens
            },
            message=message
        )
    
    @staticmethod
    def user_response(user, message="User retrieved successfully"):
        """Return user data response"""
        return ApiResponse.success(
            data=user.to_flutter_dict(),
            message=message
        )