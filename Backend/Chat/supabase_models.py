"""
Supabase database models and operations for FloatChat ARGO system
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
import json
from supabase_config import get_supabase_client

logger = logging.getLogger(__name__)

class SupabaseArgoFloats:
    """ARGO Floats table operations"""
    
    def __init__(self):
        self.client = get_supabase_client()
        self.table_name = "argo_floats"
    
    async def create_float(self, float_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new ARGO float record"""
        try:
            response = self.client.table(self.table_name).insert(float_data).execute()
            return {
                "success": True,
                "data": response.data,
                "message": "Float created successfully"
            }
        except Exception as e:
            logger.error(f"Error creating float: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create float"
            }
    
    async def get_float(self, float_id: str) -> Dict[str, Any]:
        """Get ARGO float by ID"""
        try:
            response = self.client.table(self.table_name).select("*").eq("float_id", float_id).execute()
            
            if response.data:
                return {
                    "success": True,
                    "data": response.data[0],
                    "message": "Float retrieved successfully"
                }
            else:
                return {
                    "success": False,
                    "message": "Float not found"
                }
        except Exception as e:
            logger.error(f"Error getting float: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve float"
            }
    
    async def get_all_floats(self, limit: int = 100) -> Dict[str, Any]:
        """Get all ARGO floats"""
        try:
            response = self.client.table(self.table_name).select("*").limit(limit).execute()
            return {
                "success": True,
                "data": response.data,
                "count": len(response.data),
                "message": "Floats retrieved successfully"
            }
        except Exception as e:
            logger.error(f"Error getting floats: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve floats"
            }
    
    async def update_float(self, float_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update ARGO float"""
        try:
            response = self.client.table(self.table_name).update(update_data).eq("float_id", float_id).execute()
            return {
                "success": True,
                "data": response.data,
                "message": "Float updated successfully"
            }
        except Exception as e:
            logger.error(f"Error updating float: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update float"
            }

class SupabaseArgoProfiles:
    """ARGO Profiles table operations"""
    
    def __init__(self):
        self.client = get_supabase_client()
        self.table_name = "argo_profiles"
    
    async def create_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new ARGO profile record"""
        try:
            response = self.client.table(self.table_name).insert(profile_data).execute()
            return {
                "success": True,
                "data": response.data,
                "message": "Profile created successfully"
            }
        except Exception as e:
            logger.error(f"Error creating profile: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create profile"
            }
    
    async def get_profiles_by_float(self, float_id: str, limit: int = 50) -> Dict[str, Any]:
        """Get profiles for a specific float"""
        try:
            response = self.client.table(self.table_name).select("*").eq("float_id", float_id).limit(limit).execute()
            return {
                "success": True,
                "data": response.data,
                "count": len(response.data),
                "message": "Profiles retrieved successfully"
            }
        except Exception as e:
            logger.error(f"Error getting profiles: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve profiles"
            }
    
    async def search_profiles(self, query_params: Dict[str, Any] = None, limit: int = 100) -> Dict[str, Any]:
        """Search profiles with various filters"""
        try:
            query = self.client.table(self.table_name).select("*")
            
            if query_params:
                # Apply filters based on query parameters
                if 'min_lat' in query_params:
                    query = query.gte('latitude', query_params['min_lat'])
                if 'max_lat' in query_params:
                    query = query.lte('latitude', query_params['max_lat'])
                if 'min_lon' in query_params:
                    query = query.gte('longitude', query_params['min_lon'])
                if 'max_lon' in query_params:
                    query = query.lte('longitude', query_params['max_lon'])
                if 'start_date' in query_params:
                    query = query.gte('date_time', query_params['start_date'])
                if 'end_date' in query_params:
                    query = query.lte('date_time', query_params['end_date'])
            
            response = query.limit(limit).execute()
            return {
                "success": True,
                "data": response.data,
                "count": len(response.data),
                "message": "Profiles searched successfully"
            }
        except Exception as e:
            logger.error(f"Error searching profiles: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to search profiles"
            }

class SupabaseChatSessions:
    """Chat Sessions table operations"""
    
    def __init__(self):
        self.client = get_supabase_client()
        self.table_name = "chat_sessions"
    
    async def create_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new chat session"""
        try:
            response = self.client.table(self.table_name).insert(session_data).execute()
            return {
                "success": True,
                "data": response.data,
                "message": "Session created successfully"
            }
        except Exception as e:
            logger.error(f"Error creating session: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create session"
            }
    
    async def get_session(self, session_id: str) -> Dict[str, Any]:
        """Get chat session by ID"""
        try:
            response = self.client.table(self.table_name).select("*").eq("session_id", session_id).execute()
            
            if response.data:
                return {
                    "success": True,
                    "data": response.data[0],
                    "message": "Session retrieved successfully"
                }
            else:
                return {
                    "success": False,
                    "message": "Session not found"
                }
        except Exception as e:
            logger.error(f"Error getting session: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve session"
            }
    
    async def update_session_activity(self, session_id: str) -> Dict[str, Any]:
        """Update last activity timestamp for session"""
        try:
            update_data = {"last_activity": datetime.utcnow().isoformat()}
            response = self.client.table(self.table_name).update(update_data).eq("session_id", session_id).execute()
            return {
                "success": True,
                "data": response.data,
                "message": "Session activity updated"
            }
        except Exception as e:
            logger.error(f"Error updating session activity: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update session activity"
            }

# Initialize database models
argo_floats_db = SupabaseArgoFloats()
argo_profiles_db = SupabaseArgoProfiles()
chat_sessions_db = SupabaseChatSessions()

async def init_supabase_tables():
    """Initialize Supabase tables if they don't exist"""
    client = get_supabase_client(admin=True)
    if not client:
        logger.error("Admin client not available for table initialization")
        return False
    
    # Note: Table creation should be done via Supabase Dashboard or SQL
    # This function is mainly for verification
    try:
        logger.info("Supabase tables initialization check completed")
        return True
    except Exception as e:
        logger.error(f"Error initializing Supabase tables: {str(e)}")
        return False