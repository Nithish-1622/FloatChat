#!/usr/bin/env python3
"""
FloatChat ARGO LLM API Service
Interactive API for querying Indian Ocean ARGO data with LLM responses
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import logging
from datetime import datetime
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add current directory to path
sys.path.append('.')

# Import our data services
from supabase_data_storage import SupabaseDataStorageService
from groq import Groq

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="FloatChat ARGO API",
    description="Interactive API for Indian Ocean ARGO float data with LLM responses",
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

# Initialize services
data_service = SupabaseDataStorageService()

# Initialize Groq LLM (using LLM_API_KEY from .env file)
try:
    groq_api_key = os.environ.get("GROQ_API_KEY") or os.environ.get("LLM_API_KEY")
    if groq_api_key:
        groq_client = Groq(api_key=groq_api_key)
        logger.info("Groq LLM client initialized successfully")
    else:
        groq_client = None
        logger.warning("No Groq API key found in GROQ_API_KEY or LLM_API_KEY environment variables")
except Exception as e:
    groq_client = None
    logger.warning(f"Groq LLM not available: {e}")

# Pydantic models for API
class ChatRequest(BaseModel):
    message: str
    include_data: bool = True
    max_profiles: int = 5

class ChatResponse(BaseModel):
    response: str
    argo_data_summary: Optional[Dict[str, Any]] = None
    query_timestamp: str

class ArgoDataQuery(BaseModel):
    region: Optional[str] = None
    max_results: int = 10
    date_range_days: Optional[int] = 30

class ArgoDataResponse(BaseModel):
    profiles: List[Dict[str, Any]]
    floats: List[Dict[str, Any]]
    summary: Dict[str, Any]

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "FloatChat ARGO API - Indian Ocean Data Service",
        "version": "1.0.0",
        "endpoints": [
            "/chat - Interactive LLM chat with ARGO data",
            "/argo/data - Query ARGO float and profile data",
            "/argo/summary - Get data summary",
            "/health - Health check"
        ],
        "data_status": "Connected to Indian Ocean ARGO database" if data_service.is_available else "Database unavailable"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected" if data_service.is_available else "disconnected",
        "llm": "available" if groq_client else "unavailable",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/argo/summary")
async def get_argo_summary():
    """Get summary of ARGO data in database"""
    if not data_service.is_available:
        raise HTTPException(status_code=503, detail="Database service unavailable")
    
    try:
        # Get counts
        floats = data_service.supabase_client.table('argo_floats').select('*').execute()
        profiles = data_service.supabase_client.table('argo_profiles').select('*').execute()
        
        # Regional breakdown
        regions = {}
        temp_ranges = {}
        depth_ranges = {}
        
        for profile in profiles.data:
            # Count by region
            region = profile.get('ocean_basin', 'Unknown')
            regions[region] = regions.get(region, 0) + 1
            
            # Temperature and depth analysis
            measurements = profile.get('measurements', [])
            if measurements:
                temps = [m.get('temperature') for m in measurements if m.get('temperature')]
                depths = [m.get('depth', m.get('pressure', 0)) for m in measurements]
                
                if temps:
                    temp_ranges[region] = {
                        'min': min(temps),
                        'max': max(temps),
                        'avg': sum(temps) / len(temps)
                    }
                
                if depths:
                    depth_ranges[region] = {
                        'min': min(depths),
                        'max': max(depths)
                    }
        
        return {
            "total_floats": len(floats.data),
            "total_profiles": len(profiles.data),
            "regional_distribution": regions,
            "temperature_ranges": temp_ranges,
            "depth_ranges": depth_ranges,
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting ARGO summary: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {str(e)}")

@app.post("/argo/data")
async def query_argo_data(query: ArgoDataQuery):
    """Query ARGO float and profile data"""
    if not data_service.is_available:
        raise HTTPException(status_code=503, detail="Database service unavailable")
    
    try:
        # Build query filters
        profile_query = data_service.supabase_client.table('argo_profiles').select('*')
        float_query = data_service.supabase_client.table('argo_floats').select('*')
        
        # Filter by region if specified
        if query.region:
            profile_query = profile_query.eq('ocean_basin', query.region)
        
        # Limit results
        profiles = profile_query.limit(query.max_results).execute()
        floats = float_query.limit(query.max_results).execute()
        
        return ArgoDataResponse(
            profiles=profiles.data,
            floats=floats.data,
            summary={
                "profiles_returned": len(profiles.data),
                "floats_returned": len(floats.data),
                "query_region": query.region,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Error querying ARGO data: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {str(e)}")

def get_relevant_argo_context(user_message: str, max_profiles: int = 5) -> Dict[str, Any]:
    """Get relevant ARGO data context based on user message"""
    if not data_service.is_available:
        return {"error": "Database not available"}
    
    try:
        # Simple keyword matching for regions
        user_lower = user_message.lower()
        region_keywords = {
            'arabian sea': 'Arabian_Sea',
            'arabian': 'Arabian_Sea',
            'bay of bengal': 'Bay_of_Bengal',
            'bengal': 'Bay_of_Bengal',
            'bay': 'Bay_of_Bengal',
            'central indian': 'Central_Indian',
            'equatorial': 'Central_Indian',
            'southern indian': 'Southern_Indian',
            'subtropical': 'Southern_Indian'
        }
        
        # Determine region
        target_region = None
        for keyword, region in region_keywords.items():
            if keyword in user_lower:
                target_region = region
                break
        
        # Query profiles
        profile_query = data_service.supabase_client.table('argo_profiles').select('*')
        if target_region:
            profile_query = profile_query.eq('ocean_basin', target_region)
        
        profiles = profile_query.limit(max_profiles).execute()
        
        # Get some floats too
        floats = data_service.supabase_client.table('argo_floats').select('*').limit(3).execute()
        
        # Prepare context summary
        context = {
            "profiles_count": len(profiles.data),
            "target_region": target_region,
            "sample_profiles": []
        }
        
        # Add sample profile data
        for profile in profiles.data[:3]:
            measurements = profile.get('measurements', [])
            if measurements:
                surface_temp = next((m.get('temperature') for m in measurements if m.get('depth', 0) < 10), None)
                max_depth = max(m.get('depth', m.get('pressure', 0)) for m in measurements)
                
                context["sample_profiles"].append({
                    "id": profile.get('profile_id'),
                    "location": f"{profile.get('latitude', 0):.2f}N, {profile.get('longitude', 0):.2f}E",
                    "region": profile.get('ocean_basin'),
                    "date": profile.get('date_time'),
                    "surface_temperature": surface_temp,
                    "max_depth": max_depth,
                    "measurement_count": len(measurements)
                })
        
        return context
        
    except Exception as e:
        logger.error(f"Error getting ARGO context: {e}")
        return {"error": str(e)}

def generate_llm_response(user_message: str, argo_context: Dict[str, Any]) -> str:
    """Generate LLM response using ARGO data context"""
    if not groq_client:
        return "LLM service is not available. Please check your GROQ_API_KEY configuration."
    
    try:
        # Create system prompt with ARGO context
        system_prompt = f"""You are FloatChat, an expert marine oceanographer specializing in Indian Ocean ARGO float data.

Instructions:
- Only answer questions strictly related to oceanography, marine science, or ARGO float data.
- If the question is not related to these topics, respond with: "Sorry, I can only answer questions about oceanography, marine science, or ARGO float data."
- Keep your answers concise, crisp, and easy to understand for all users.

Current ARGO Data Context:
- Available profiles: {argo_context.get('profiles_count', 0)}
- Target region: {argo_context.get('target_region', 'All Indian Ocean regions')}

Sample Recent Data:
{json.dumps(argo_context.get('sample_profiles', []), indent=2)}

You have access to real Indian Ocean ARGO float data covering:
- Arabian Sea: High salinity waters (35.5-36.5 psu), warm temperatures (25-30°C)
- Bay of Bengal: Lower salinity due to river discharge (32-35 psu), warm temperatures (26-30°C)
- Central Indian Ocean: Equatorial waters (34.5-35.5 psu), temperatures (26-29°C)
- Southern Indian Ocean: Subtropical waters (34-35 psu), cooler temperatures (15-20°C)

Respond as an expert oceanographer with specific insights about Indian Ocean conditions, temperature profiles, salinity patterns, and marine phenomena. Use the provided data context to give accurate, scientific responses."""

        # Generate response using model from environment
        llm_model = os.environ.get("LLM_MODEL", "llama-3.1-8b-instant")
        response = groq_client.chat.completions.create(
            model=llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Error generating LLM response: {e}")
        return f"I apologize, but I encountered an error generating a response: {str(e)}"

@app.post("/chat")
async def chat_with_argo_data(request: ChatRequest):
    """Interactive chat with ARGO data context"""
    try:
        # Get relevant ARGO context
        argo_context = None
        if request.include_data and data_service.is_available:
            argo_context = get_relevant_argo_context(request.message, request.max_profiles)
        
        # Generate LLM response
        llm_response = generate_llm_response(request.message, argo_context or {})
        
        return ChatResponse(
            response=llm_response,
            argo_data_summary=argo_context,
            query_timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# Additional endpoint for testing
@app.get("/test/sample-queries")
async def get_sample_queries():
    """Get sample queries for testing the API"""
    return {
        "sample_queries": [
            "What are the temperature conditions in the Arabian Sea?",
            "How does salinity vary in the Bay of Bengal?",
            "Show me recent ARGO profile data from the Indian Ocean",
            "What's the difference between Arabian Sea and Bay of Bengal water properties?",
            "Explain the thermocline structure in Central Indian Ocean",
            "How deep do ARGO floats sample in Southern Indian Ocean?"
        ],
        "test_regions": [
            "Arabian_Sea",
            "Bay_of_Bengal", 
            "Central_Indian",
            "Southern_Indian"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    
    # Check if API key is set
    api_key = os.environ.get("GROQ_API_KEY") or os.environ.get("LLM_API_KEY")
    if not api_key:
        print("⚠️ Warning: No API key found in GROQ_API_KEY or LLM_API_KEY environment variables!")
        print("Check your .env file or set manually with: $env:GROQ_API_KEY='your-api-key-here' (PowerShell)")
    else:
        print("✅ LLM API key loaded successfully")
    
    print("🌊 Starting FloatChat ARGO API Server...")
    print("🇮🇳 Ready to serve Indian Ocean ARGO data!")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)