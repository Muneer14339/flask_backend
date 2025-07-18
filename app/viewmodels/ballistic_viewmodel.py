# app/viewmodels/ballistic_viewmodel.py
from app.services.ballistic_service import BallisticService
from app.utils.responses import ApiResponse
import logging

class BallisticViewModel:
    """Ballistic ViewModel - Handles business logic for ballistic views"""
    
    def __init__(self):
        self.ballistic_service = BallisticService()
    
    # DOPE Entry operations
    def handle_create_dope_entry(self, request_data, user_id):
        """Handle DOPE entry creation request"""
        try:
            success, message, dope_entry = self.ballistic_service.create_dope_entry(user_id, request_data)
            
            if success:
                return ApiResponse.success(
                    data=dope_entry.to_dict(),
                    message=message
                )
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Create DOPE entry error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to create DOPE entry")
    
    def handle_get_dope_entries(self, user_id, rifle_id=None):
        """Handle get DOPE entries request"""
        try:
            success, message, dope_entries = self.ballistic_service.get_dope_entries(user_id, rifle_id)
            
            if success:
                return ApiResponse.success(
                    data=[entry.to_dict() for entry in dope_entries],
                    message=message
                )
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Get DOPE entries error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to get DOPE entries")
    
    def handle_delete_dope_entry(self, entry_id, user_id):
        """Handle DOPE entry deletion request"""
        try:
            success, message = self.ballistic_service.delete_dope_entry(entry_id, user_id)
            
            if success:
                return ApiResponse.success(message=message)
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Delete DOPE entry error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to delete DOPE entry")
    
    # Zero Entry operations
    def handle_create_zero_entry(self, request_data, user_id):
        """Handle zero entry creation request"""
        try:
            success, message, zero_entry = self.ballistic_service.create_zero_entry(user_id, request_data)
            
            if success:
                return ApiResponse.success(
                    data=zero_entry.to_dict(),
                    message=message
                )
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Create zero entry error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to create zero entry")
    
    def handle_get_zero_entries(self, user_id, rifle_id=None):
        """Handle get zero entries request"""
        try:
            success, message, zero_entries = self.ballistic_service.get_zero_entries(user_id, rifle_id)
            
            if success:
                return ApiResponse.success(
                    data=[entry.to_dict() for entry in zero_entries],
                    message=message
                )
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Get zero entries error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to get zero entries")
    
    def handle_delete_zero_entry(self, entry_id, user_id):
        """Handle zero entry deletion request"""
        try:
            success, message = self.ballistic_service.delete_zero_entry(entry_id, user_id)
            
            if success:
                return ApiResponse.success(message=message)
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Delete zero entry error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to delete zero entry")
    
    # Chronograph Data operations
    def handle_create_chronograph_data(self, request_data, user_id):
        """Handle chronograph data creation request"""
        try:
            success, message, chrono_data = self.ballistic_service.create_chronograph_data(user_id, request_data)
            
            if success:
                return ApiResponse.success(
                    data=chrono_data.to_dict(),
                    message=message
                )
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Create chronograph data error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to create chronograph data")
    
    def handle_get_chronograph_data(self, user_id, rifle_id=None):
        """Handle get chronograph data request"""
        try:
            success, message, chrono_data = self.ballistic_service.get_chronograph_data(user_id, rifle_id)
            
            if success:
                return ApiResponse.success(
                    data=[data.to_dict() for data in chrono_data],
                    message=message
                )
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Get chronograph data error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to get chronograph data")
    
    def handle_delete_chronograph_data(self, data_id, user_id):
        """Handle chronograph data deletion request"""
        try:
            success, message = self.ballistic_service.delete_chronograph_data(data_id, user_id)
            
            if success:
                return ApiResponse.success(message=message)
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Delete chronograph data error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to delete chronograph data")
    
    # Ballistic Calculation operations
    def handle_calculate_ballistics(self, request_data, user_id):
        """Handle ballistic calculation request"""
        try:
            # Validate required calculation parameters
            required_fields = ['rifleId', 'ammunitionId', 'ballisticCoefficient', 'muzzleVelocity', 'targetDistance']
            for field in required_fields:
                if request_data.get(field) is None:
                    return ApiResponse.validation_error(f"{field} is required for ballistic calculation")
            
            success, message, calculation = self.ballistic_service.calculate_ballistics(user_id, request_data)
            
            if success:
                return ApiResponse.success(
                    data=calculation.to_dict(),
                    message=message
                )
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Calculate ballistics error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to calculate ballistics")
    
    def handle_get_ballistic_calculations(self, user_id, rifle_id=None):
        """Handle get ballistic calculations request"""
        try:
            success, message, calculations = self.ballistic_service.get_ballistic_calculations(user_id, rifle_id)
            
            if success:
                return ApiResponse.success(
                    data=[calc.to_dict() for calc in calculations],
                    message=message
                )
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Get ballistic calculations error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to get ballistic calculations")
    
    def handle_delete_ballistic_calculation(self, calculation_id, user_id):
        """Handle ballistic calculation deletion request"""
        try:
            success, message = self.ballistic_service.delete_ballistic_calculation(calculation_id, user_id)
            
            if success:
                return ApiResponse.success(message=message)
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Delete ballistic calculation error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to delete ballistic calculation")
    
    # Summary operations
    def handle_get_ballistic_summary(self, rifle_id, user_id):
        """Handle get ballistic data summary request"""
        try:
            if not rifle_id:
                return ApiResponse.validation_error("Rifle ID is required")
            
            success, message, summary = self.ballistic_service.get_ballistic_data_summary(user_id, rifle_id)
            
            if success:
                return ApiResponse.success(
                    data=summary,
                    message=message
                )
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Get ballistic summary error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to get ballistic summary")
    
    def handle_get_all_ballistic_data(self, user_id, rifle_id=None):
        """Handle get all ballistic data request"""
        try:
            # Get all types of ballistic data
            dope_success, dope_message, dope_entries = self.ballistic_service.get_dope_entries(user_id, rifle_id)
            zero_success, zero_message, zero_entries = self.ballistic_service.get_zero_entries(user_id, rifle_id)
            chrono_success, chrono_message, chrono_data = self.ballistic_service.get_chronograph_data(user_id, rifle_id)
            calc_success, calc_message, calculations = self.ballistic_service.get_ballistic_calculations(user_id, rifle_id)
            
            if not all([dope_success, zero_success, chrono_success, calc_success]):
                return ApiResponse.error("Failed to retrieve complete ballistic data")
            
            # Combine all data
            ballistic_data = {
                'dopeEntries': [entry.to_dict() for entry in dope_entries],
                'zeroEntries': [entry.to_dict() for entry in zero_entries],
                'chronographData': [data.to_dict() for data in chrono_data],
                'ballisticCalculations': [calc.to_dict() for calc in calculations],
                'summary': {
                    'totalDopeEntries': len(dope_entries),
                    'totalZeroEntries': len(zero_entries),
                    'totalChronographSessions': len(chrono_data),
                    'totalCalculations': len(calculations),
                    'rifleId': rifle_id
                }
            }
            
            return ApiResponse.success(
                data=ballistic_data,
                message="All ballistic data retrieved successfully"
            )
            
        except Exception as e:
            logging.error(f"Get all ballistic data error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to get ballistic data")