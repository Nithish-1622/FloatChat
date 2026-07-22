"""
Pydantic models for ARGO float data and API responses
"""
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator
import numpy as np

class ArgoProfile(BaseModel):
    """Core ARGO profile data model"""
    profile_id: str = Field(..., description="Unique profile identifier")
    platform_id: str = Field(..., description="Float platform identifier")
    cycle_number: int = Field(..., description="Profile cycle number")
    
    # Location and Time
    latitude: float = Field(..., ge=-90, le=90, description="Profile latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Profile longitude")
    timestamp: datetime = Field(..., description="Profile timestamp")
    
    # Core Measurements
    pressure: List[float] = Field(default_factory=list, description="Pressure measurements (dbar)")
    temperature: List[float] = Field(default_factory=list, description="Temperature measurements (°C)")
    salinity: List[float] = Field(default_factory=list, description="Salinity measurements (PSU)")
    
    # Quality Control Flags
    pressure_qc: List[int] = Field(default_factory=list, description="Pressure QC flags")
    temperature_qc: List[int] = Field(default_factory=list, description="Temperature QC flags")
    salinity_qc: List[int] = Field(default_factory=list, description="Salinity QC flags")
    
    # BGC Variables (optional)
    oxygen: Optional[List[float]] = Field(default=None, description="Oxygen measurements (µmol/kg)")
    nitrate: Optional[List[float]] = Field(default=None, description="Nitrate measurements (µmol/kg)")
    chlorophyll: Optional[List[float]] = Field(default=None, description="Chlorophyll measurements (mg/m³)")
    ph: Optional[List[float]] = Field(default=None, description="pH measurements")
    alkalinity: Optional[List[float]] = Field(default=None, description="Alkalinity measurements")
    
    # BGC QC Flags (optional)
    oxygen_qc: Optional[List[int]] = Field(default=None, description="Oxygen QC flags")
    nitrate_qc: Optional[List[int]] = Field(default=None, description="Nitrate QC flags")
    chlorophyll_qc: Optional[List[int]] = Field(default=None, description="Chlorophyll QC flags")
    
    # Metadata
    data_mode: str = Field(default="R", description="Data mode (R/A/D)")
    data_centre: Optional[str] = Field(default=None, description="Data centre code")
    data_source: str = Field(..., description="Source repository")
    processing_level: Optional[str] = Field(default=None, description="Processing level")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            np.float64: lambda v: float(v),
            np.int64: lambda v: int(v)
        }

class ArgoFloat(BaseModel):
    """ARGO float metadata model"""
    platform_id: str = Field(..., description="Float platform identifier")
    wmo_inst_type: Optional[str] = Field(default=None, description="WMO instrument type")
    project_name: Optional[str] = Field(default=None, description="Project name")
    pi_name: Optional[str] = Field(default=None, description="Principal investigator")
    
    # Deployment info
    deployment_date: Optional[datetime] = Field(default=None, description="Deployment date")
    deployment_latitude: Optional[float] = Field(default=None, description="Deployment latitude")
    deployment_longitude: Optional[float] = Field(default=None, description="Deployment longitude")
    
    # Current status
    last_location_date: Optional[datetime] = Field(default=None, description="Last known location date")
    last_latitude: Optional[float] = Field(default=None, description="Last known latitude")
    last_longitude: Optional[float] = Field(default=None, description="Last known longitude")
    
    # Technical details
    positioning_system: Optional[str] = Field(default=None, description="Positioning system")
    profile_count: Optional[int] = Field(default=0, description="Total number of profiles")
    
    # Status
    status: str = Field(default="ACTIVE", description="Float status")
    data_centre: Optional[str] = Field(default=None, description="Data centre")

class ChatRequest(BaseModel):
    """Chat request model"""
    message: str = Field(..., min_length=1, description="User message")
    session_id: str = Field(default="default", description="Chat session ID")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")
    include_visualizations: bool = Field(default=True, description="Include visualizations in response")

class ChatResponse(BaseModel):
    """Chat response model"""
    message: str = Field(..., description="AI response message")
    session_id: str = Field(..., description="Chat session ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    
    # Data and visualizations
    data_summary: Optional[Dict[str, Any]] = Field(default=None, description="Summary of retrieved data")
    visualizations: Optional[List[Dict[str, Any]]] = Field(default=None, description="Visualization specifications")
    download_links: Optional[List[str]] = Field(default=None, description="Data download links")
    
    # Metadata
    query_type: Optional[str] = Field(default=None, description="Type of query processed")
    data_sources: Optional[List[str]] = Field(default=None, description="Data sources used")
    processing_time: Optional[float] = Field(default=None, description="Processing time in seconds")

class DataQuery(BaseModel):
    """Data query model for structured requests"""
    # Spatial bounds
    latitude_min: Optional[float] = Field(default=None, ge=-90, le=90)
    latitude_max: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude_min: Optional[float] = Field(default=None, ge=-180, le=180)
    longitude_max: Optional[float] = Field(default=None, ge=-180, le=180)
    
    # Temporal bounds
    start_date: Optional[datetime] = Field(default=None, description="Start date for data query")
    end_date: Optional[datetime] = Field(default=None, description="End date for data query")
    
    # Variables
    variables: Optional[List[str]] = Field(default=None, description="Variables to retrieve")
    include_bgc: bool = Field(default=False, description="Include BGC variables")
    
    # Quality control
    qc_level: str = Field(default="good", description="QC level (good/all)")
    
    # Limits
    max_profiles: Optional[int] = Field(default=1000, description="Maximum number of profiles")
    max_floats: Optional[int] = Field(default=100, description="Maximum number of floats")

class VisualizationRequest(BaseModel):
    """Visualization request model"""
    plot_type: str = Field(..., description="Type of plot (trajectory, profile, timeseries, map)")
    data_query: DataQuery = Field(..., description="Data query parameters")
    style_options: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Plot styling options")
    export_format: str = Field(default="json", description="Export format (json/png/svg/html)")

class ProfileSummary(BaseModel):
    """Profile summary for vector database"""
    profile_id: str = Field(..., description="Profile identifier")
    summary_text: str = Field(..., description="Natural language summary")
    embedding_vector: Optional[List[float]] = Field(default=None, description="Embedding vector")
    
    # Metadata for retrieval
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Profile metadata")
    parquet_path: Optional[str] = Field(default=None, description="Path to parquet file")
    database_id: Optional[int] = Field(default=None, description="Database record ID")

class SystemStatus(BaseModel):
    """System status model"""
    status: str = Field(..., description="System status")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Database status
    database_connected: bool = Field(..., description="Database connection status")
    vector_db_connected: bool = Field(..., description="Vector database connection status")
    
    # Data statistics
    total_profiles: Optional[int] = Field(default=None, description="Total profiles in database")
    total_floats: Optional[int] = Field(default=None, description="Total floats in database")
    latest_data_update: Optional[datetime] = Field(default=None, description="Latest data update timestamp")
    
    # Background tasks
    active_downloads: int = Field(default=0, description="Active download tasks")
    pending_processing: int = Field(default=0, description="Pending processing tasks")

class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(default="healthy")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = Field(default="1.0.0")
    uptime_seconds: Optional[float] = Field(default=None)

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Error code")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = Field(default=None, description="Request ID for tracking")