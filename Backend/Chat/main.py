"""
FloatChat ARGO System Startup Script
===================================

This script starts the complete FloatChat system including:
- FastAPI server with all endpoints
- Background scheduler for automated tasks
- All integrated services (data storage, AI, vector DB)
- System monitoring and health checks

Usage:
    python main.py [--port 8000] [--host 0.0.0.0] [--dev]
"""

import asyncio
import sys
import logging
import argparse
from pathlib import Path
from contextlib import asynccontextmanager

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import system components
from api.main import app as fastapi_app
from services.scheduler import init_scheduler_service, shutdown_scheduler
from supabase_data_storage import ArgoDataStorage
from services.vector_database import ArgoVectorDatabase
from services.conversational_ai import ArgoConversationalAI
from services.comprehensive_data_ingestion import ComprehensiveArgoDataIngestion

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global service instances
global_services = {
    'data_storage': None,
    'vector_database': None,
    'conversational_ai': None,
    'data_ingestion': None,
    'scheduler_service': None
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("🚀 Starting FloatChat ARGO System...")
    
    try:
        # Initialize all services
        logger.info("📡 Initializing services...")
        
        # Initialize core services
        global_services['data_storage'] = ArgoDataStorage()
        global_services['vector_database'] = ArgoVectorDatabase()
        global_services['conversational_ai'] = ArgoConversationalAI()
        global_services['data_ingestion'] = ComprehensiveArgoDataIngestion()
        
        # Initialize scheduler with all services
        logger.info("⏰ Starting background scheduler...")
        global_services['scheduler_service'] = await init_scheduler_service(
            data_storage=global_services['data_storage'],
            vector_database=global_services['vector_database'],
            conversational_ai=global_services['conversational_ai'],
            data_ingestion=global_services['data_ingestion']
        )
        
        # Start the scheduler
        if global_services['scheduler_service']:
            success = await global_services['scheduler_service'].start_scheduler()
            if success:
                logger.info("✅ Background scheduler started successfully")
            else:
                logger.warning("⚠️ Background scheduler failed to start")
        
        logger.info("🌊 FloatChat ARGO System is now operational!")
        logger.info("📚 API Documentation available at: http://localhost:8000/docs")
        logger.info("🔍 Health Check endpoint: http://localhost:8000/health")
        
        yield
        
    finally:
        # Cleanup on shutdown
        logger.info("🛑 Shutting down FloatChat ARGO System...")
        
        try:
            # Stop scheduler
            if global_services['scheduler_service']:
                await shutdown_scheduler()
                logger.info("✅ Scheduler stopped")
            
            # Close other services if needed
            # (Most services will be garbage collected automatically)
            
            logger.info("✅ FloatChat ARGO System shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {str(e)}")

def create_app() -> FastAPI:
    """Create the FastAPI application with all configurations"""
    
    # Use the existing FastAPI app from api/main.py
    app = fastapi_app
    
    # Update lifespan
    app.router.lifespan_context = lifespan
    
    # Add additional middleware if needed
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure this for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add startup message to root endpoint
    @app.get("/")
    async def root():
        return {
            "system": "FloatChat ARGO System",
            "status": "operational",
            "version": "1.0.0",
            "description": "AI-powered ARGO oceanographic data analysis system",
            "services": {
                "data_storage": "ArgoDataStorage with Supabase",
                "vector_database": "ChromaDB with SentenceTransformers",
                "ai_service": "Groq LLM with RAG",
                "data_ingestion": "Multi-source ARGO data ingestion",
                "scheduler": "Background task automation"
            },
            "endpoints": {
                "docs": "/docs",
                "health": "/health", 
                "chat": "/chat",
                "search": "/search",
                "ingest": "/ingest",
                "admin": "/admin"
            }
        }
    
    return app

def main():
    """Main function to start the system"""
    parser = argparse.ArgumentParser(description="FloatChat ARGO System")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind the server to")
    parser.add_argument("--dev", action="store_true", help="Run in development mode with auto-reload")
    parser.add_argument("--log-level", type=str, default="info", choices=["debug", "info", "warning", "error"], help="Log level")
    
    args = parser.parse_args()
    
    # Create the application
    app = create_app()
    
    # Configure uvicorn
    uvicorn_config = {
        "app": app,
        "host": args.host,
        "port": args.port,
        "log_level": args.log_level,
        "access_log": True,
        "loop": "asyncio"
    }
    
    if args.dev:
        uvicorn_config.update({
            "reload": True,
            "reload_dirs": [str(project_root)],
            "reload_excludes": ["logs/*", "cache/*", "data/*"]
        })
    
    # Print startup banner
    print("="*60)
    print("🌊 FLOATCHAT ARGO SYSTEM")
    print("="*60)
    print(f"🌐 Server: http://{args.host}:{args.port}")
    print(f"📚 API Docs: http://{args.host}:{args.port}/docs")
    print(f"🔍 Health Check: http://{args.host}:{args.port}/health")
    print(f"💬 Chat Endpoint: http://{args.host}:{args.port}/chat")
    print("="*60)
    print("🚀 Starting server...")
    
    # Start the server
    try:
        uvicorn.run(**uvicorn_config)
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
            
            # Initialize data ingestion service
            logger.info("Initializing data ingestion service...")
            self.services['data_ingestion'] = ArgoDataIngestion()
            
            # Initialize data storage service
            logger.info("Initializing data storage service...")
            self.services['data_storage'] = ArgoDataStorage()
            
            # Initialize vector database
            logger.info("Initializing vector database...")
            self.services['vector_db'] = ArgoVectorDatabase()
            
            # Initialize RAG system
            logger.info("Initializing RAG system...")
            self.services['rag_system'] = ArgoRAGSystem(self.services['vector_db'])
            
            # Initialize conversational AI
            logger.info("Initializing conversational AI...")
            self.services['conversational_ai'] = ArgoConversationalAI(
                self.services['rag_system']
            )
            
            # Initialize scheduler
            logger.info("Initializing scheduler...")
            self.scheduler = ArgoScheduler(
                self.services['data_ingestion'],
                self.services['data_storage'],
                self.services['vector_db']
            )
            
            logger.info("All services initialized successfully!")
            
        except Exception as e:
            logger.error(f"Error initializing services: {str(e)}")
            raise
    
    async def start_scheduler(self):
        """Start the background scheduler"""
        if self.scheduler:
            try:
                await self.scheduler.start()
                logger.info("Background scheduler started successfully!")
            except Exception as e:
                logger.error(f"Error starting scheduler: {str(e)}")
                raise
    
    async def stop_scheduler(self):
        """Stop the background scheduler"""
        if self.scheduler:
            try:
                await self.scheduler.stop()
                logger.info("Background scheduler stopped successfully!")
            except Exception as e:
                logger.error(f"Error stopping scheduler: {str(e)}")
    
    async def shutdown_services(self):
        """Shutdown all application services"""
        logger.info("Shutting down FloatChat ARGO system...")
        
        try:
            # Stop scheduler
            await self.stop_scheduler()
            
            # Close database connection
            await close_database()
            
            # Clear services
            self.services.clear()
            
            logger.info("All services shut down successfully!")
            
        except Exception as e:
            logger.error(f"Error shutting down services: {str(e)}")
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform system health check"""
        health_status = {
            'status': 'healthy',
            'timestamp': asyncio.get_event_loop().time(),
            'services': {}
        }
        
        # Check each service
        for service_name, service in self.services.items():
            try:
                if hasattr(service, 'health_check'):
                    service_health = await service.health_check()
                    health_status['services'][service_name] = service_health
                else:
                    health_status['services'][service_name] = {'status': 'unknown'}
            except Exception as e:
                health_status['services'][service_name] = {
                    'status': 'error',
                    'error': str(e)
                }
                health_status['status'] = 'degraded'
        
        # Check scheduler
        if self.scheduler:
            try:
                scheduler_health = await self.scheduler.get_system_health()
                health_status['services']['scheduler'] = scheduler_health
            except Exception as e:
                health_status['services']['scheduler'] = {
                    'status': 'error',
                    'error': str(e)
                }
                health_status['status'] = 'degraded'
        
        return health_status
    
    async def process_chat_message(self, message: str, session_id: str = None) -> Dict[str, Any]:
        """Process a chat message through the system"""
        try:
            if 'conversational_ai' not in self.services:
                raise ValueError("Conversational AI service not initialized")
            
            response = await self.services['conversational_ai'].process_message(
                message, session_id
            )
            
            return {
                'status': 'success',
                'response': response
            }
            
        except Exception as e:
            logger.error(f"Error processing chat message: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    async def get_service_stats(self) -> Dict[str, Any]:
        """Get statistics from all services"""
        stats = {}
        
        for service_name, service in self.services.items():
            try:
                if hasattr(service, 'get_stats'):
                    service_stats = await service.get_stats()
                    stats[service_name] = service_stats
                else:
                    stats[service_name] = {'message': 'Stats not available'}
            except Exception as e:
                stats[service_name] = {'error': str(e)}
        
        return stats

# Global application instance
app_instance = None

@asynccontextmanager
async def lifespan():
    """Application lifespan context manager"""
    global app_instance
    
    # Startup
    app_instance = FloatChatApp()
    await app_instance.initialize_services()
    await app_instance.start_scheduler()
    
    yield app_instance
    
    # Shutdown
    await app_instance.shutdown_services()

async def main():
    """Main entry point for standalone execution"""
    logger.info("Starting FloatChat ARGO system in standalone mode...")
    
    async with lifespan() as app:
        logger.info("System is running. Press Ctrl+C to stop.")
        
        try:
            # Keep the application running
            while True:
                await asyncio.sleep(60)  # Sleep for 1 minute
                
                # Perform periodic health check
                health = await app.health_check()
                if health['status'] != 'healthy':
                    logger.warning(f"System health check: {health['status']}")
                
        except KeyboardInterrupt:
            logger.info("Received shutdown signal...")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
    
    logger.info("FloatChat ARGO system stopped.")

def create_directories():
    """Create necessary directories"""
    directories = [
        'cache',
        'data',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

if __name__ == "__main__":
    # Create necessary directories
    create_directories()
    
    # Run the application
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application failed: {str(e)}")
        sys.exit(1)