"""
Database models for ARGO float data using SQLAlchemy
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from datetime import datetime
import uuid

Base = declarative_base()

class ArgoFloatDB(Base):
    """Database model for ARGO float metadata"""
    __tablename__ = "argo_floats"
    
    id = Column(Integer, primary_key=True, index=True)
    platform_id = Column(String(50), unique=True, index=True, nullable=False)
    wmo_inst_type = Column(String(100))
    project_name = Column(String(200))
    pi_name = Column(String(200))
    
    # Deployment info
    deployment_date = Column(DateTime(timezone=True))
    deployment_latitude = Column(Float)
    deployment_longitude = Column(Float)
    
    # Current status
    last_location_date = Column(DateTime(timezone=True))
    last_latitude = Column(Float)
    last_longitude = Column(Float)
    
    # Technical details
    positioning_system = Column(String(50))
    profile_count = Column(Integer, default=0)
    
    # Status and metadata
    status = Column(String(20), default="ACTIVE")
    data_centre = Column(String(10))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profiles = relationship("ArgoProfileDB", back_populates="float")

class ArgoProfileDB(Base):
    """Database model for ARGO profile metadata"""
    __tablename__ = "argo_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(String(100), unique=True, index=True, nullable=False)
    platform_id = Column(String(50), ForeignKey("argo_floats.platform_id"), nullable=False)
    cycle_number = Column(Integer, nullable=False)
    
    # Location and time
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Data availability flags
    has_temperature = Column(Boolean, default=False)
    has_salinity = Column(Boolean, default=False)
    has_oxygen = Column(Boolean, default=False)
    has_nitrate = Column(Boolean, default=False)
    has_chlorophyll = Column(Boolean, default=False)
    has_ph = Column(Boolean, default=False)
    
    # Data quality summary
    temperature_qc_summary = Column(String(20))  # good, questionable, bad, mixed
    salinity_qc_summary = Column(String(20))
    oxygen_qc_summary = Column(String(20))
    
    # File paths
    parquet_path = Column(String(500))
    netcdf_path = Column(String(500))
    
    # Processing metadata
    data_mode = Column(String(1), default="R")  # R/A/D
    data_centre = Column(String(10))
    data_source = Column(String(100), nullable=False)
    processing_level = Column(String(20))
    
    # Depth statistics
    max_depth = Column(Float)
    n_levels = Column(Integer)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    float = relationship("ArgoFloatDB", back_populates="profiles")
    summary = relationship("ProfileSummaryDB", back_populates="profile", uselist=False)

class ProfileSummaryDB(Base):
    """Database model for profile summaries and embeddings"""
    __tablename__ = "profile_summaries"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(String(100), ForeignKey("argo_profiles.profile_id"), unique=True, nullable=False)
    
    # Summary text
    summary_text = Column(Text, nullable=False)
    
    # Embedding metadata
    embedding_model = Column(String(100))
    embedding_dimension = Column(Integer)
    
    # Vector database metadata
    vector_db_id = Column(String(100))  # ID in Chroma
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profile = relationship("ArgoProfileDB", back_populates="summary")

class ChatSessionDB(Base):
    """Database model for chat sessions"""
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    
    # Session metadata
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    last_activity = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Session context
    context = Column(JSON)
    
    # Relationships
    messages = relationship("ChatMessageDB", back_populates="session")

class ChatMessageDB(Base):
    """Database model for chat messages"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), ForeignKey("chat_sessions.session_id"), nullable=False)
    
    # Message content
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    
    # Query metadata
    query_type = Column(String(50))
    data_sources = Column(ARRAY(String))
    processing_time = Column(Float)
    
    # Data references
    profiles_used = Column(ARRAY(String))
    visualizations = Column(JSON)
    
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    session = relationship("ChatSessionDB", back_populates="messages")

class DataProcessingJobDB(Base):
    """Database model for tracking data processing jobs"""
    __tablename__ = "data_processing_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(100), unique=True, index=True, nullable=False)
    job_type = Column(String(50), nullable=False)  # download, process, embedding
    
    # Job parameters
    source_url = Column(String(500))
    target_path = Column(String(500))
    parameters = Column(JSON)
    
    # Status tracking
    status = Column(String(20), default="PENDING")  # PENDING, RUNNING, COMPLETED, FAILED
    progress = Column(Float, default=0.0)
    
    # Timing
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Results
    result_metadata = Column(JSON)
    error_message = Column(Text)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

class SystemMetricsDB(Base):
    """Database model for system metrics and monitoring"""
    __tablename__ = "system_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Metrics
    total_profiles = Column(Integer, default=0)
    total_floats = Column(Integer, default=0)
    active_downloads = Column(Integer, default=0)
    pending_processing = Column(Integer, default=0)
    
    # Performance metrics
    avg_query_time = Column(Float)
    avg_embedding_time = Column(Float)
    
    # Data freshness
    latest_profile_date = Column(DateTime(timezone=True))
    last_update_check = Column(DateTime(timezone=True))
    
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)