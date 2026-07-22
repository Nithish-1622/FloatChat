"""
FloatChat ARGO System - FastAPI REST API
Clean, working API server with essential endpoints
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
import uuid
import json
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# FastAPI imports
try:
    from fastapi import FastAPI, HTTPException, Query, BackgroundTasks, Depends, File, UploadFile, Form
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
    from pydantic import BaseModel, Field
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    print("FastAPI not available. Please install fastapi and uvicorn.")

# Local imports
try:
    from config import API_CONFIG, LOGGING_CONFIG
    from services.conversational_ai import ArgoConversationalAI
    from services.comprehensive_data_ingestion import ComprehensiveArgoDataIngestion  
    from services.vector_database import ArgoVectorDatabase, initialize_vector_database
    from supabase_data_storage import SupabaseDataStorageService
except ImportError as e:
    print(f"Import warning: {e}")
    # Define minimal fallbacks
    API_CONFIG = {"host": "0.0.0.0", "port": 8000}
    LOGGING_CONFIG = {"level": "INFO"}

# Setup logging
logging.basicConfig(level=getattr(logging, LOGGING_CONFIG.get("level", "INFO")))
logger = logging.getLogger(__name__)

# Pydantic models for API requests/responses
class ChatRequest(BaseModel):
    message: str = Field(..., description="User message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    conversation_type: Optional[str] = Field("general", description="Type of conversation")

class ChatResponse(BaseModel):
    success: bool
    session_id: str
    response: str
    conversation_type: str
    relevant_profiles_count: int
    metadata: Dict[str, Any]
    suggested_followup: Optional[List[str]] = None

class DataIngestionRequest(BaseModel):
    sources: List[str] = Field(..., description="List of data sources to ingest")
    start_date: Optional[str] = Field(None, description="Start date for data ingestion")
    end_date: Optional[str] = Field(None, description="End date for data ingestion")
    force_refresh: bool = Field(False, description="Force refresh of existing data")

class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    filters: Optional[Dict[str, Any]] = Field(None, description="Search filters")
    max_results: int = Field(10, description="Maximum number of results")
    search_type: str = Field("semantic", description="Type of search (semantic, hybrid, metadata)")

# Global service instances
ai_system: Optional[ArgoConversationalAI] = None
data_ingestion: Optional[ComprehensiveArgoDataIngestion] = None  
data_storage: Optional[SupabaseDataStorageService] = None
vector_db: Optional[ArgoVectorDatabase] = None

# Application startup
startup_time = datetime.utcnow()

def create_app():
    """Create and configure FastAPI application"""
    if not FASTAPI_AVAILABLE:
        raise ImportError("FastAPI not available. Please install fastapi and uvicorn.")
    
    app = FastAPI(
        title="FloatChat ARGO API",
        description="Comprehensive API for ARGO oceanographic data analysis with AI capabilities",
        version="2.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app

# Create app instance
if FASTAPI_AVAILABLE:
    app = create_app()
    
    @app.on_event("startup")
    async def startup_event():
        """Initialize services on startup"""
        global ai_system, data_ingestion, data_storage, vector_db
        
        logger.info("🚀 Starting FloatChat ARGO API...")
        
        try:
            # Initialize data storage
            logger.info("Initializing Supabase data storage...")
            data_storage = SupabaseDataStorageService()
            
            # Initialize vector database
            logger.info("Initializing vector database...")
            vector_db = await initialize_vector_database()
            
            # Initialize data ingestion system
            logger.info("Initializing data ingestion system...")
            data_ingestion = ComprehensiveArgoDataIngestion()
            
            # Initialize AI system
            logger.info("Initializing AI conversational system...")
            ai_system = ArgoConversationalAI(vector_db=vector_db)
            
            logger.info("✅ All services initialized successfully!")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize services: {e}")
            # Don't raise in startup to allow partial functionality

    @app.on_event("shutdown")
    async def shutdown_event():
        """Cleanup on shutdown"""
        logger.info("🛑 Shutting down FloatChat ARGO API...")

    # Health and Status Endpoints
    @app.get("/")
    async def root():
        """Root endpoint with basic API information"""
        return {
            "name": "FloatChat ARGO API", 
            "version": "2.0.0",
            "description": "Comprehensive ARGO oceanographic data analysis with AI",
            "docs": "/docs",
            "status": "/health"
        }

    @app.get("/health")
    async def health_check():
        """Comprehensive health check endpoint"""
        try:
            uptime = (datetime.utcnow() - startup_time).total_seconds()
            
            # Check service health
            services_status = {
                "ai_system": ai_system is not None,
                "data_ingestion": data_ingestion is not None,
                "data_storage": data_storage is not None,
                "vector_db": vector_db is not None
            }
            
            return {
                "status": "healthy" if all(services_status.values()) else "degraded",
                "version": "2.0.0",
                "uptime_seconds": uptime,
                "services": services_status,
                "data_sources": {"available": 11, "active": 5}  # Placeholder
            }
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

    # Chat and AI Endpoints
    @app.post("/chat", response_model=ChatResponse)
    async def chat_with_ai(request: ChatRequest):
        """Main chat endpoint for conversational AI interaction"""
        try:
            if not ai_system:
                raise HTTPException(status_code=503, detail="AI system not available")
            
            # Process user query
            result = await ai_system.process_user_query(
                user_query=request.message,
                session_id=request.session_id,
                context=request.context
            )
            
            if not result.get('success'):
                raise HTTPException(status_code=500, detail=result.get('error', 'AI processing failed'))
            
            return ChatResponse(**result)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Chat endpoint error: {e}")
            raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")

    @app.get("/chat/sessions/{session_id}")
    async def get_chat_session(session_id: str):
        """Get chat session history"""
        try:
            if not ai_system or session_id not in ai_system.active_sessions:
                raise HTTPException(status_code=404, detail="Session not found")
            
            session = ai_system.active_sessions[session_id]
            return {
                "session_id": session_id,
                "created_at": session['created_at'].isoformat(),
                "last_activity": session['last_activity'].isoformat(),
                "message_count": len(session['history']),
                "history": session['history'][-10:]  # Last 10 messages
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Session retrieval error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # Data Ingestion Endpoints
    @app.post("/data/ingest")
    async def ingest_argo_data(request: DataIngestionRequest, background_tasks: BackgroundTasks):
        """Trigger ARGO data ingestion from multiple sources"""
        try:
            if not data_ingestion:
                raise HTTPException(status_code=503, detail="Data ingestion service not available")
            
            # Start ingestion as background task
            task_id = str(uuid.uuid4())
            
            async def _background_ingestion():
                try:
                    logger.info(f"Starting ingestion task {task_id} for sources: {request.sources}")
                    
                    result = await data_ingestion.ingest_from_multiple_sources(
                        source_names=request.sources,
                        max_profiles_per_source=1000,
                        concurrent_limit=5
                    )
                    
                    logger.info(f"Ingestion task {task_id} completed: {result}")
                    
                except Exception as e:
                    logger.error(f"Background ingestion task {task_id} failed: {e}")
            
            background_tasks.add_task(_background_ingestion)
            
            return {
                "success": True,
                "task_id": task_id,
                "message": f"Data ingestion started for {len(request.sources)} sources",
                "sources": request.sources,
                "estimated_duration_minutes": len(request.sources) * 2
            }
            
        except Exception as e:
            logger.error(f"Data ingestion error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/data/sources")
    async def get_available_sources():
        """Get list of available ARGO data sources"""
        try:
            if not data_ingestion:
                return {"sources": [], "error": "Data ingestion service not available"}
            
            sources = data_ingestion.get_available_sources()
            
            return {
                "success": True,
                "sources": sources,
                "total_sources": len(sources),
                "source_types": ["api", "ftp", "demo"]
            }
            
        except Exception as e:
            logger.error(f"Error getting sources: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # Search and Query Endpoints  
    @app.post("/search/profiles")
    async def search_profiles(request: SearchRequest):
        """Search ARGO profiles using semantic or hybrid search"""
        try:
            if not vector_db:
                raise HTTPException(status_code=503, detail="Vector database not available")
            
            # Perform search based on type
            if request.search_type == "semantic":
                results = await vector_db.semantic_search(
                    query=request.query,
                    n_results=request.max_results,
                    filters=request.filters
                )
            elif request.search_type == "hybrid":
                results = await vector_db.hybrid_search(
                    query=request.query,
                    filters=request.filters or {},
                    n_results=request.max_results
                )
            else:
                # Metadata-only search would go here
                results = {"success": False, "error": "Metadata search not implemented"}
            
            if not results.get('success'):
                raise HTTPException(status_code=500, detail=results.get('error', 'Search failed'))
            
            return results
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Search error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/profiles/{profile_id}")
    async def get_profile_details(profile_id: str):
        """Get detailed information about a specific ARGO profile"""
        try:
            if not data_storage:
                raise HTTPException(status_code=503, detail="Data storage not available")
            
            # This would retrieve from Supabase
            profile_data = {
                "profile_id": profile_id,
                "message": "Profile retrieval not yet implemented",
                "placeholder": True
            }
            
            return profile_data
            
        except Exception as e:
            logger.error(f"Profile retrieval error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/profiles")
    async def list_profiles(
        limit: int = Query(50, description="Maximum number of profiles to return"),
        offset: int = Query(0, description="Number of profiles to skip"),
        ocean_basin: Optional[str] = Query(None, description="Filter by ocean basin"),
        date_from: Optional[str] = Query(None, description="Filter profiles from this date"),
        date_to: Optional[str] = Query(None, description="Filter profiles to this date")
    ):
        """List ARGO profiles with optional filtering"""
        try:
            # This would implement proper pagination and filtering
            profiles = {
                "profiles": [],
                "total_count": 0,
                "limit": limit,
                "offset": offset,
                "filters_applied": {
                    "ocean_basin": ocean_basin,
                    "date_from": date_from,
                    "date_to": date_to
                },
                "message": "Profile listing not yet fully implemented"
            }
            
            return profiles
            
        except Exception as e:
            logger.error(f"Profile listing error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # Admin and Testing Endpoints
    @app.get("/admin/stats")
    async def get_system_statistics():
        """Get comprehensive system statistics"""
        try:
            # AI system statistics
            ai_stats = {
                "active_sessions": len(ai_system.active_sessions) if ai_system else 0,
                "total_queries_processed": 0,  # Would track this
                "average_response_time": 0.0
            }
            
            return {
                "success": True,
                "timestamp": datetime.utcnow().isoformat(),
                "ai_system": ai_stats,
                "uptime_seconds": (datetime.utcnow() - startup_time).total_seconds()
            }
            
        except Exception as e:
            logger.error(f"Statistics error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/dev/test-ingestion")
    async def test_data_ingestion():
        """Test data ingestion with demo data"""
        try:
            if not data_ingestion:
                raise HTTPException(status_code=503, detail="Data ingestion not available")
            
            # Generate demo data
            demo_result = await data_ingestion.generate_demo_profiles(
                num_profiles=10,
                save_to_storage=True
            )
            
            return {
                "success": True,
                "demo_profiles_generated": demo_result.get('profiles_generated', 0),
                "message": "Demo data ingestion completed",
                "profiles_summary": demo_result.get('profiles_summary', [])
            }
            
        except Exception as e:
            logger.error(f"Test ingestion error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

else:
    app = None

if __name__ == "__main__":
    # Run the application
    if FASTAPI_AVAILABLE and app:
        uvicorn.run(
            "main:app",
            host=API_CONFIG.get("host", "0.0.0.0"), 
            port=API_CONFIG.get("port", 8000),
            reload=True,
            log_level="info"
        )
    else:
        print("FastAPI not available or app not created. Please install required dependencies.")