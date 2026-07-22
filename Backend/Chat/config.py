# FloatChat ARGO Data Configuration
import os
from pathlib import Path
from typing import List, Dict, Any

# Base Configuration
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "cache"
LOGS_DIR = BASE_DIR / "logs"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Database Configuration
DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "floatchat_argo"),
    "username": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password")
}

DATABASE_URL = f"postgresql://{DATABASE_CONFIG['username']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"

# Vector Database Configuration
VECTOR_DB_CONFIG = {
    "collection_name": "argo_profiles",
    "persist_directory": str(CACHE_DIR / "chroma_db"),
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2"
}

# LLM Configuration
LLM_CONFIG = {
    "provider": os.getenv("LLM_PROVIDER", "groq"),  # groq, openai, local
    "model": os.getenv("LLM_MODEL", "llama3-8b-8192"),
    "api_key": os.getenv("LLM_API_KEY", ""),
    "temperature": 0.1,
    "max_tokens": 1000
}

# ARGO Data Sources Configuration
ARGO_DATA_SOURCES = {
    "noaa_argo_floats": {
        "base_url": "https://www.nodc.noaa.gov/argo/floats_data.htm",
        "type": "direct_download",
        "priority": 1
    },
    "incois_indian_ocean": {
        "base_url": "https://services.incois.gov.in/argo/ADV.jsp",
        "type": "api",
        "priority": 2
    },
    "ucsd_argo_products": {
        "base_url": "https://argo.ucsd.edu/data/argo-data-products/",
        "type": "direct_download",
        "priority": 3
    },
    "data_gov_in": {
        "base_url": "https://www.data.gov.in/resource/indian-ocean-argo-data",
        "type": "api",
        "priority": 4
    },
    "incois_oon": {
        "base_url": "https://incois.gov.in/OON/index.jsp",
        "type": "api",
        "priority": 5
    },
    "ocean_ops": {
        "base_url": "https://www.ocean-ops.org/board/?t=argo",
        "type": "api",
        "priority": 6
    },
    "ifremer_gdac": {
        "base_url": "https://tds0.ifremer.fr/thredds/catalog/CORIOLIS-ARGO-GDAC-OBS/catalog.html",
        "type": "opendap",
        "priority": 7
    },
    "ncei_aoml": {
        "base_url": "https://www.ncei.noaa.gov/data/oceans/argo/gadr/data/aoml/",
        "type": "direct_download",
        "priority": 8
    },
    "ncei_indian": {
        "base_url": "https://www.ncei.noaa.gov/data/oceans/argo/gadr/data/indian/",
        "type": "direct_download",
        "priority": 9
    },
    "bgc_argo": {
        "base_url": "https://maps.biogeochemical-argo.com/bgcargo/",
        "type": "api",
        "priority": 10
    },
    "incois_las": {
        "base_url": "https://las.incois.gov.in/las/UI.vm",
        "type": "opendap",
        "priority": 11
    }
}

# Data Processing Configuration
DATA_PROCESSING_CONFIG = {
    "core_variables": [
        "pressure", "temperature", "salinity", "latitude", 
        "longitude", "time", "profile_id", "platform_id"
    ],
    "bgc_variables": [
        "oxygen", "nitrate", "chlorophyll", "ph", "alkalinity",
        "dissolved_organic_carbon", "particulate_organic_carbon"
    ],
    "qc_flags": {
        "good": [1, 2],  # Good and probably good
        "bad": [3, 4, 9],  # Bad and missing
        "questionable": [5, 6, 7, 8]  # Various questionable flags
    },
    "depth_levels": list(range(0, 2001, 10)),  # 0-2000m in 10m intervals
    "parquet_partitions": ["year", "month", "region"]
}

# Geographical Regions for Partitioning
GEOGRAPHICAL_REGIONS = {
    "indian_ocean": {"lat_min": -50, "lat_max": 30, "lon_min": 30, "lon_max": 120},
    "pacific_ocean": {"lat_min": -60, "lat_max": 60, "lon_min": 120, "lon_max": -70},
    "atlantic_ocean": {"lat_min": -60, "lat_max": 70, "lon_min": -70, "lon_max": 30},
    "southern_ocean": {"lat_min": -90, "lat_max": -50, "lon_min": -180, "lon_max": 180},
    "arctic_ocean": {"lat_min": 66, "lat_max": 90, "lon_min": -180, "lon_max": 180}
}

# Background Task Configuration
SCHEDULER_CONFIG = {
    "data_update_interval": 6,  # hours
    "embedding_refresh_interval": 24,  # hours
    "cleanup_old_data_interval": 168,  # hours (1 week)
    "max_concurrent_downloads": 5,
    "retry_attempts": 3,
    "timeout_seconds": 300
}

# API Configuration
API_CONFIG = {
    "host": "0.0.0.0",
    "port": int(os.getenv("CHAT_API_PORT", "8002")),
    "reload": os.getenv("ENV", "production") == "development",
    "cors_origins": [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
    "rotation": "1 week",
    "retention": "1 month",
    "compression": "gz"
}

# Cache Configuration
CACHE_CONFIG = {
    "redis_url": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    "default_ttl": 3600,  # 1 hour
    "max_memory": "100mb"
}

# Model Context Protocol Configuration
MCP_CONFIG = {
    "enable_mcp": True,
    "mcp_server_url": os.getenv("MCP_SERVER_URL", "http://localhost:8003"),
    "supported_tools": [
        "sql_query_executor",
        "vector_similarity_search", 
        "parquet_data_loader",
        "visualization_generator"
    ]
}

# Combined ARGO System Configuration
ARGO_CONFIG = {
    "database": DATABASE_CONFIG,
    "argo_sources": ARGO_DATA_SOURCES,
    "processing": DATA_PROCESSING_CONFIG,
    "vector_db": VECTOR_DB_CONFIG,
    "llm": LLM_CONFIG,
    "api": API_CONFIG,
    "scheduler": SCHEDULER_CONFIG,
    "mcp": MCP_CONFIG
}