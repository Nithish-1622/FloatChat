"""
Simplified FloatChat API for Windows deployment with Supabase integration
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging
import json
from datetime import datetime
import uuid
import os

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    logger = logging.getLogger(__name__)
    logger.info("Environment variables loaded from .env file")
except ImportError:
    logger = logging.getLogger(__name__)
    logger.warning("python-dotenv not available, using system environment variables")

# Supabase integration
try:
    from supabase_data_storage import supabase_storage_service
    from supabase_config import test_supabase_connection
    SUPABASE_AVAILABLE = True
except ImportError as e:
    supabase_storage_service = None
    test_supabase_connection = None
    SUPABASE_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.error(f"Supabase import error: {str(e)}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FloatChat ARGO API",
    description="AI-powered oceanographic data processing system with Supabase backend",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: datetime

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    services: Dict[str, Any]

class ProfileSearchRequest(BaseModel):
    query_params: Optional[Dict[str, Any]] = None
    limit: Optional[int] = 100

# Enhanced data service with Supabase integration
class SupabaseDataService:
    def __init__(self):
        self.storage = supabase_storage_service if SUPABASE_AVAILABLE else None
        
        # Fallback mock data
        self.mock_data = {
            "floats": ["1234567", "2345678", "3456789"],
            "profiles": [
                {
                    "id": "profile_001",
                    "float_id": "1234567",
                    "latitude": 25.5,
                    "longitude": -80.3,
                    "date": "2024-09-24",
                    "temperature": [22.1, 21.8, 21.5],
                    "salinity": [36.1, 36.2, 36.3],
                    "pressure": [0, 10, 20]
                }
            ]
        }
    
    async def search_profiles(self, query_params: Dict[str, Any] = None, limit: int = 100) -> Dict[str, Any]:
        """Search profiles using Supabase or fallback to mock data"""
        if self.storage and self.storage.is_available:
            try:
                return await self.storage.search_profiles(query_params, limit)
            except Exception as e:
                logger.error(f"Supabase search error: {str(e)}")
                return self._fallback_search_profiles()
        else:
            return self._fallback_search_profiles()
    
    def _fallback_search_profiles(self) -> Dict[str, Any]:
        """Fallback search using mock data"""
        return {
            "success": True,
            "data": self.mock_data["profiles"],
            "count": len(self.mock_data["profiles"]),
            "message": "Using mock data (Supabase not available)"
        }
    
    async def get_float_info(self, float_id: str) -> Dict[str, Any]:
        """Get float information from Supabase or mock data"""
        if self.storage and self.storage.is_available:
            try:
                from supabase_models import argo_floats_db
                return await argo_floats_db.get_float(float_id)
            except Exception as e:
                logger.error(f"Error getting float info: {str(e)}")
                return self._fallback_float_info(float_id)
        else:
            return self._fallback_float_info(float_id)
    
    def _fallback_float_info(self, float_id: str) -> Dict[str, Any]:
        """Fallback float info using mock data"""
        return {
            "success": True,
            "data": {
                "float_id": float_id,
                "status": "active",
                "deployment_latitude": 25.5,
                "deployment_longitude": -80.3,
                "last_update": "2024-09-24T12:00:00Z"
            },
            "message": "Using mock data (Supabase not available)"
        }
    
    async def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        if self.storage and self.storage.is_available:
            try:
                return await self.storage.get_storage_stats()
            except Exception as e:
                logger.error(f"Error getting storage stats: {str(e)}")
                return self._fallback_storage_stats()
        else:
            return self._fallback_storage_stats()
    
    def _fallback_storage_stats(self) -> Dict[str, Any]:
        """Fallback storage statistics"""
        return {
            "success": True,
            "stats": {
                "storage_type": "mock_data",
                "total_floats": len(self.mock_data["floats"]),
                "total_profiles": len(self.mock_data["profiles"]),
                "last_update": datetime.utcnow().isoformat()
            },
            "message": "Using mock data statistics"
        }

# Enhanced AI service
class SupabaseAIService:
    def __init__(self):
        self.data_service = None  # Will be set after initialization
        self.responses = {
            "temperature": "Based on the ARGO data, the current temperature profile shows warm surface waters at 22°C decreasing with depth.",
            "salinity": "The salinity measurements indicate typical oceanic values around 36 PSU, characteristic of this region.",
            "float": "ARGO floats are autonomous instruments that collect oceanographic data including temperature and salinity profiles.",
            "search": "I can help you search through the ARGO database for specific locations, time periods, or measurement criteria.",
            "default": "I can help you analyze ARGO oceanographic data. Ask me about temperature, salinity, floats, specific locations, or data searches."
        }
    
    async def process_message(self, message: str, session_id: str = None) -> str:
        """Process chat message with enhanced responses"""
        message_lower = message.lower()
        
        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Enhanced response logic
        if "temperature" in message_lower:
            response = self.responses["temperature"]
            
            # Try to get actual data if available
            if self.data_service:
                try:
                    profiles_result = await self.data_service.search_profiles(limit=5)
                    if profiles_result.get("success") and profiles_result.get("data"):
                        profile_count = profiles_result.get("count", 0)
                        response += f" I found {profile_count} recent profiles in the database."
                except Exception as e:
                    logger.error(f"Error getting temperature data: {str(e)}")
            
            return response
        
        elif "salinity" in message_lower:
            return self.responses["salinity"]
        
        elif any(word in message_lower for word in ["float", "floats"]):
            response = self.responses["float"]
            
            # Add storage stats if available
            if self.data_service:
                try:
                    stats_result = await self.data_service.get_storage_stats()
                    if stats_result.get("success"):
                        stats = stats_result.get("stats", {})
                        float_count = stats.get("total_floats", 0)
                        response += f" Currently tracking {float_count} floats in our database."
                except Exception as e:
                    logger.error(f"Error getting float stats: {str(e)}")
            
            return response
        
        elif any(word in message_lower for word in ["search", "find", "data"]):
            return self.responses["search"]
        
        else:
            return self.responses["default"]

# Initialize services
data_service = SupabaseDataService()
ai_service = SupabaseAIService()
ai_service.data_service = data_service  # Set reference for AI service

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "FloatChat ARGO API", "version": "1.0.0"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint with service status"""
    supabase_status = "available" if SUPABASE_AVAILABLE else "unavailable"
    
    # Test Supabase connection if available
    supabase_connection = "unknown"
    if SUPABASE_AVAILABLE and test_supabase_connection:
        try:
            connection_test = test_supabase_connection()
            supabase_connection = "connected" if connection_test else "disconnected"
        except Exception as e:
            supabase_connection = f"error: {str(e)}"
    
    services = {
        "supabase": {
            "status": supabase_status,
            "connection": supabase_connection
        },
        "storage": {
            "status": "available" if data_service.storage and data_service.storage.is_available else "fallback"
        },
        "ai_service": {
            "status": "available"
        }
    }
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        services=services
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint for conversational AI"""
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        response = await ai_service.process_message(
            message=request.message,
            session_id=session_id
        )
        
        return ChatResponse(
            response=response,
            session_id=session_id,
            timestamp=datetime.now()
        )
    
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")

@app.post("/data/search_profiles")
async def search_profiles(request: ProfileSearchRequest):
    """Search ARGO profiles with filters"""
    try:
        result = await data_service.search_profiles(
            query_params=request.query_params,
            limit=request.limit or 100
        )
        return result
    
    except Exception as e:
        logger.error(f"Profile search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Profile search failed: {str(e)}")

@app.get("/data/float/{float_id}")
async def get_float(float_id: str):
    """Get specific ARGO float information"""
    try:
        result = await data_service.get_float_info(float_id)
        return result
    
    except Exception as e:
        logger.error(f"Float info error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Float info retrieval failed: {str(e)}")

@app.get("/data/stats")
async def get_storage_stats():
    """Get database storage statistics"""
    try:
        result = await data_service.get_storage_stats()
        return result
    
    except Exception as e:
        logger.error(f"Stats error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Statistics retrieval failed: {str(e)}")

@app.get("/admin/supabase_test")
async def test_supabase():
    """Test Supabase connection (admin endpoint)"""
    if not SUPABASE_AVAILABLE:
        return {
            "success": False,
            "message": "Supabase not available (check installation)",
            "available_services": ["mock_data"]
        }
    
    try:
        if test_supabase_connection:
            connection_result = test_supabase_connection()
            
            # Also test storage service
            storage_stats = await data_service.get_storage_stats()
            
            return {
                "success": connection_result,
                "message": "Supabase connection successful" if connection_result else "Supabase connection failed",
                "storage_service_available": data_service.storage and data_service.storage.is_available,
                "storage_stats": storage_stats
            }
        else:
            return {
                "success": False,
                "message": "Supabase test function not available"
            }
    
    except Exception as e:
        logger.error(f"Supabase test error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Supabase test failed"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
async def root():
    """Root endpoint"""
    return {
        "message": "FloatChat ARGO API is running!",
        "status": "active",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        services={
            "api": {"status": "active"},
            "data_service": {"status": "active"},
            "ai_service": {"status": "active"}
        }
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process chat messages"""
    try:
        session_id = request.session_id or f"session_{int(datetime.now().timestamp())}"
        
        # Process the message with AI service
        response = ai_service.process_message(request.message, session_id)
        
        return ChatResponse(
            response=response,
            session_id=session_id,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)