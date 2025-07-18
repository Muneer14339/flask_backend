# app/viewmodels/loadout_viewmodel.py
from app.services.loadout_service import LoadoutService
from app.utils.responses import ApiResponse
from app.utils.jwt_utils import JWTUtils
import logging

class LoadoutViewModel:
    """Loadout ViewModel - Handles business logic for loadout views"""
    
    def __init__(self):
        self.loadout_service = LoadoutService()
    
    # Rifle operations
    def handle_create_rifle(self, request_data, user_id):
        """Handle rifle creation request"""
        try:
            success, message, rifle = self.loadout_service.create_rifle(user_id, request_data)
            
            if success:
                return ApiResponse.success(
                    data=rifle.to_dict(),
                    message=message
                )
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Create rifle error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to create rifle")
    
    def handle_get_rifles(self, user_id):
        """Handle get rifles request"""
        try:
            success, message, rifles = self.loadout_service.get_rifles(user_id)
            
            if success:
                return ApiResponse.success(
                    data=[rifle.to_dict() for rifle in rifles],
                    message=message
                )
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Get rifles error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to get rifles")
    
    def handle_get_rifle(self, rifle_id, user_id):
        """Handle get single rifle request"""
        try:
            success, message, rifle = self.loadout_service.get_rifle(rifle_id, user_id)
            
            if success:
                return ApiResponse.success(
                    data=rifle.to_dict(),
                    message=message
                )
            else:
                return ApiResponse.not_found(message)
                
        except Exception as e:
            logging.error(f"Get rifle error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to get rifle")
    
    def handle_update_rifle(self, rifle_id, request_data, user_id):
        """Handle rifle update request"""
        try:
            success, message, rifle = self.loadout_service.update_rifle(rifle_id, user_id, request_data)
            
            if success:
                return ApiResponse.success(
                    data=rifle.to_dict(),
                    message=message
                )
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Update rifle error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to update rifle")
    
    def handle_delete_rifle(self, rifle_id, user_id):
        """Handle rifle deletion request"""
        try:
            success, message = self.loadout_service.delete_rifle(rifle_id, user_id)
            
            if success:
                return ApiResponse.success(message=message)
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Delete rifle error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to delete rifle")
    
    def handle_set_active_rifle(self, request_data, user_id):
        """Handle set active rifle request"""
        try:
            rifle_id = request_data.get('rifleId')
            if not rifle_id:
                return ApiResponse.validation_error("Rifle ID is required")
            
            success, message = self.loadout_service.set_active_rifle(rifle_id, user_id)
            
            if success:
                return ApiResponse.success(message=message)
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Set active rifle error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to set active rifle")
    
    # Ammunition operations
    def handle_create_ammunition(self, request_data, user_id):
        """Handle ammunition creation request"""
        try:
            success, message, ammunition = self.loadout_service.create_ammunition(user_id, request_data)
            
            if success:
                return ApiResponse.success(
                    data=ammunition.to_dict(),
                    message=message
                )
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Create ammunition error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to create ammunition")
    
    def handle_get_ammunition(self, user_id):
        """Handle get ammunition request"""
        try:
            success, message, ammunition = self.loadout_service.get_ammunition(user_id)
            
            if success:
                return ApiResponse.success(
                    data=[ammo.to_dict() for ammo in ammunition],
                    message=message
                )
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Get ammunition error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to get ammunition")
    
    def handle_update_ammunition(self, ammo_id, request_data, user_id):
        """Handle ammunition update request"""
        try:
            success, message, ammunition = self.loadout_service.update_ammunition(ammo_id, user_id, request_data)
            
            if success:
                return ApiResponse.success(
                    data=ammunition.to_dict(),
                    message=message
                )
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Update ammunition error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to update ammunition")
    
    def handle_delete_ammunition(self, ammo_id, user_id):
        """Handle ammunition deletion request"""
        try:
            success, message = self.loadout_service.delete_ammunition(ammo_id, user_id)
            
            if success:
                return ApiResponse.success(message=message)
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Delete ammunition error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to delete ammunition")
    
    # Scope operations
    def handle_create_scope(self, request_data, user_id):
        """Handle scope creation request"""
        try:
            success, message, scope = self.loadout_service.create_scope(user_id, request_data)
            
            if success:
                return ApiResponse.success(
                    data=scope.to_dict(),
                    message=message
                )
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Create scope error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to create scope")
    
    def handle_get_scopes(self, user_id):
        """Handle get scopes request"""
        try:
            success, message, scopes = self.loadout_service.get_scopes(user_id)
            
            if success:
                return ApiResponse.success(
                    data=[scope.to_dict() for scope in scopes],
                    message=message
                )
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Get scopes error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to get scopes")
    
    def handle_update_scope(self, scope_id, request_data, user_id):
        """Handle scope update request"""
        try:
            success, message, scope = self.loadout_service.update_scope(scope_id, user_id, request_data)
            
            if success:
                return ApiResponse.success(
                    data=scope.to_dict(),
                    message=message
                )
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Update scope error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to update scope")
    
    def handle_delete_scope(self, scope_id, user_id):
        """Handle scope deletion request"""
        try:
            success, message = self.loadout_service.delete_scope(scope_id, user_id)
            
            if success:
                return ApiResponse.success(message=message)
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Delete scope error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to delete scope")
    
    # Maintenance operations
    def handle_create_maintenance(self, request_data, user_id):
        """Handle maintenance creation request"""
        try:
            success, message, maintenance = self.loadout_service.create_maintenance(user_id, request_data)
            
            if success:
                return ApiResponse.success(
                    data=maintenance.to_dict(),
                    message=message
                )
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Create maintenance error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to create maintenance task")
    
    def handle_get_maintenance(self, user_id):
        """Handle get maintenance request"""
        try:
            success, message, maintenance = self.loadout_service.get_maintenance(user_id)
            
            if success:
                return ApiResponse.success(
                    data=[task.to_dict() for task in maintenance],
                    message=message
                )
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Get maintenance error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to get maintenance tasks")
    
    def handle_complete_maintenance(self, maintenance_id, user_id):
        """Handle maintenance completion request"""
        try:
            success, message = self.loadout_service.complete_maintenance(maintenance_id, user_id)
            
            if success:
                return ApiResponse.success(message=message)
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Complete maintenance error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to complete maintenance task")
    
    def handle_delete_maintenance(self, maintenance_id, user_id):
        """Handle maintenance deletion request"""
        try:
            success, message = self.loadout_service.delete_maintenance(maintenance_id, user_id)
            
            if success:
                return ApiResponse.success(message=message)
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Delete maintenance error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to delete maintenance task")
    
    # Association operations
    def handle_update_rifle_scope(self, rifle_id, request_data, user_id):
        """Handle rifle scope association update"""
        try:
            scope_id = request_data.get('scopeId')
            success, message = self.loadout_service.update_rifle_scope(rifle_id, user_id, scope_id)
            
            if success:
                return ApiResponse.success(message=message)
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Update rifle scope error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to update rifle scope")
    
    def handle_update_rifle_ammunition(self, rifle_id, request_data, user_id):
        """Handle rifle ammunition association update"""
        try:
            ammunition_id = request_data.get('ammunitionId')
            success, message = self.loadout_service.update_rifle_ammunition(rifle_id, user_id, ammunition_id)
            
            if success:
                return ApiResponse.success(message=message)
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Update rifle ammunition error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to update rifle ammunition")
    
    # Summary operations
    def handle_get_loadout_summary(self, user_id):
        """Handle get loadout summary request"""
        try:
            # Get all loadout data
            rifles_success, rifles_message, rifles = self.loadout_service.get_rifles(user_id)
            ammo_success, ammo_message, ammunition = self.loadout_service.get_ammunition(user_id)
            scopes_success, scopes_message, scopes = self.loadout_service.get_scopes(user_id)
            maintenance_success, maintenance_message, maintenance = self.loadout_service.get_maintenance(user_id)
            
            if not all([rifles_success, ammo_success, scopes_success, maintenance_success]):
                return ApiResponse.error("Failed to retrieve complete loadout data")
            
            # Calculate summary statistics
            total_rifles = len(rifles)
            total_ammunition = len(ammunition)
            total_scopes = len(scopes)
            total_maintenance = len(maintenance)
            
            # Count maintenance due/overdue
            maintenance_due = 0
            for task in maintenance:
                # This would need more complex logic based on your maintenance scheduling
                # For now, just count tasks without completion date
                if not task.last_completed:
                    maintenance_due += 1
            
            # Get active rifle
            active_rifle = None
            for rifle in rifles:
                if rifle.is_active:
                    active_rifle = rifle
                    break
            
            summary = {
                'rifles': [rifle.to_dict() for rifle in rifles],
                'ammunition': [ammo.to_dict() for ammo in ammunition],
                'scopes': [scope.to_dict() for scope in scopes],
                'maintenance': [task.to_dict() for task in maintenance],
                'summary': {
                    'totalRifles': total_rifles,
                    'totalAmmunition': total_ammunition,
                    'totalScopes': total_scopes,
                    'totalMaintenance': total_maintenance,
                    'maintenanceDue': maintenance_due,
                    'activeRifle': active_rifle.to_dict() if active_rifle else None
                }
            }
            
            return ApiResponse.success(
                data=summary,
                message="Loadout summary retrieved successfully"
            )
            
        except Exception as e:
            logging.error(f"Get loadout summary error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to get loadout summary")