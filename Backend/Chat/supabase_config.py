"""
Supabase configuration and connection setup for FloatChat ARGO system
"""
import os
from supabase import create_client, Client
from typing import Dict, Any, Optional
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class SupabaseConfig:
    """Supabase configuration and client management"""
    
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.anon_key = os.getenv("SUPABASE_ANON_KEY")
        self.service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not self.url or not self.anon_key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment variables")
        
        # Create clients
        self.client: Client = create_client(self.url, self.anon_key)
        self.admin_client: Client = create_client(self.url, self.service_role_key) if self.service_role_key else None
        
        logger.info("Supabase client initialized successfully")
    
    def get_client(self, admin: bool = False) -> Client:
        """Get Supabase client"""
        if admin and self.admin_client:
            return self.admin_client
        return self.client
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test Supabase connection"""
        try:
            # Try to access a simple table or perform a basic query
            response = self.client.table('argo_floats').select("count", count="exact").execute()
            
            return {
                "status": "connected",
                "message": "Supabase connection successful",
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Supabase connection test failed: {str(e)}")
            return {
                "status": "error",
                "message": f"Connection failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }

# Global Supabase configuration instance
try:
    supabase_config = SupabaseConfig()
except Exception as e:
    logger.warning(f"Failed to initialize Supabase config: {str(e)}")
    supabase_config = None

def get_supabase_client(admin: bool = False) -> Optional[Client]:
    """Get Supabase client instance"""
    if supabase_config:
        return supabase_config.get_client(admin=admin)
    return None

def test_supabase_connection() -> bool:
    """Test Supabase connection - simple function for testing"""
    if not supabase_config:
        print("❌ Supabase config not initialized")
        return False
    
    try:
        # Simple connection test
        client = supabase_config.get_client()
        if client:
            print("✅ Supabase client created successfully")
            print(f"📡 Connected to: {supabase_config.url}")
            return True
        else:
            print("❌ Failed to create Supabase client")
            return False
    except Exception as e:
        print(f"❌ Connection test failed: {str(e)}")
        return False