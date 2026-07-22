-- FloatChat ARGO Database Schema for Supabase (Simple Version)
-- Execute this SQL in your Supabase SQL Editor to create the database structure

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create ARGO Floats table
CREATE TABLE IF NOT EXISTS argo_floats (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    float_id VARCHAR(20) UNIQUE NOT NULL,
    platform_number VARCHAR(20),
    project_name VARCHAR(100),
    pi_name VARCHAR(100),
    deployment_date TIMESTAMP WITH TIME ZONE,
    deployment_latitude DOUBLE PRECISION,
    deployment_longitude DOUBLE PRECISION,
    wmo_inst_type VARCHAR(10),
    status VARCHAR(20) DEFAULT 'active',
    last_update TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create ARGO Profiles table
CREATE TABLE IF NOT EXISTS argo_profiles (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    profile_id VARCHAR(50) UNIQUE NOT NULL,
    float_id VARCHAR(20) NOT NULL REFERENCES argo_floats(float_id) ON DELETE CASCADE,
    cycle_number INTEGER,
    date_time TIMESTAMP WITH TIME ZONE NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    position_qc INTEGER DEFAULT 1,
    profile_temp_qc INTEGER DEFAULT 1,
    profile_psal_qc INTEGER DEFAULT 1,
    profile_pres_qc INTEGER DEFAULT 1,
    ocean_basin VARCHAR(50),
    data_mode CHAR(1) DEFAULT 'R',
    parameter_data_mode VARCHAR(10) DEFAULT 'R',
    vertical_sampling_scheme VARCHAR(100),
    direction CHAR(1) DEFAULT 'A',
    data_centre VARCHAR(10),
    dc_reference VARCHAR(50),
    data_state_indicator CHAR(4) DEFAULT '2B',
    data_file_path VARCHAR(500),
    measurements JSONB DEFAULT '[]',
    qc_flags JSONB DEFAULT '{}',
    processing_metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create Chat Sessions table
CREATE TABLE IF NOT EXISTS chat_sessions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id VARCHAR(100) UNIQUE NOT NULL,
    user_id VARCHAR(100),
    session_name VARCHAR(200) DEFAULT 'ARGO Chat Session',
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    session_data JSONB DEFAULT '{}',
    message_count INTEGER DEFAULT 0
);

-- Create Chat Messages table
CREATE TABLE IF NOT EXISTS chat_messages (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    message_id VARCHAR(100) UNIQUE NOT NULL,
    session_id VARCHAR(100) NOT NULL REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    token_count INTEGER DEFAULT 0,
    response_time_ms INTEGER,
    context_data JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}'
);

-- Create Data Processing Jobs table
CREATE TABLE IF NOT EXISTS data_processing_jobs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    job_id VARCHAR(100) UNIQUE NOT NULL,
    job_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    progress DOUBLE PRECISION DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    parameters JSONB DEFAULT '{}',
    results JSONB DEFAULT '{}',
    error_message TEXT,
    logs TEXT
);

-- Create Data Sources table for tracking external data feeds
CREATE TABLE IF NOT EXISTS data_sources (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    source_id VARCHAR(50) UNIQUE NOT NULL,
    source_name VARCHAR(100) NOT NULL,
    source_url VARCHAR(500),
    source_type VARCHAR(50) DEFAULT 'argo',
    is_active BOOLEAN DEFAULT true,
    last_sync TIMESTAMP WITH TIME ZONE,
    sync_frequency_hours INTEGER DEFAULT 24,
    sync_status VARCHAR(20) DEFAULT 'pending',
    configuration JSONB DEFAULT '{}',
    statistics JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create Vector Embeddings table for RAG system (using TEXT for embeddings)
CREATE TABLE IF NOT EXISTS vector_embeddings (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    content_id VARCHAR(100) NOT NULL,
    content_type VARCHAR(50) NOT NULL,
    content_text TEXT NOT NULL,
    embedding TEXT, -- Store as JSON array string
    embedding_dimension INTEGER DEFAULT 384,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_argo_floats_float_id ON argo_floats(float_id);
CREATE INDEX IF NOT EXISTS idx_argo_floats_status ON argo_floats(status);
CREATE INDEX IF NOT EXISTS idx_argo_floats_deployment_date ON argo_floats(deployment_date);

CREATE INDEX IF NOT EXISTS idx_argo_profiles_float_id ON argo_profiles(float_id);
CREATE INDEX IF NOT EXISTS idx_argo_profiles_date_time ON argo_profiles(date_time);
CREATE INDEX IF NOT EXISTS idx_argo_profiles_location ON argo_profiles(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_argo_profiles_profile_id ON argo_profiles(profile_id);

CREATE INDEX IF NOT EXISTS idx_chat_sessions_session_id ON chat_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_last_activity ON chat_sessions(last_activity);

CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_timestamp ON chat_messages(timestamp);

CREATE INDEX IF NOT EXISTS idx_data_processing_jobs_status ON data_processing_jobs(status);
CREATE INDEX IF NOT EXISTS idx_data_processing_jobs_job_type ON data_processing_jobs(job_type);

CREATE INDEX IF NOT EXISTS idx_data_sources_source_id ON data_sources(source_id);
CREATE INDEX IF NOT EXISTS idx_data_sources_is_active ON data_sources(is_active);

CREATE INDEX IF NOT EXISTS idx_vector_embeddings_content_id ON vector_embeddings(content_id);
CREATE INDEX IF NOT EXISTS idx_vector_embeddings_content_type ON vector_embeddings(content_type);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add updated_at triggers
CREATE TRIGGER update_argo_floats_updated_at 
    BEFORE UPDATE ON argo_floats 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_argo_profiles_updated_at 
    BEFORE UPDATE ON argo_profiles 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_vector_embeddings_updated_at 
    BEFORE UPDATE ON vector_embeddings 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert default data sources
INSERT INTO data_sources (source_id, source_name, source_url, source_type, configuration) VALUES
('noaa_global', 'NOAA Global Marine Argo Atlas', 'https://www.aoml.noaa.gov/phod/gdac/index.html', 'argo', '{"region": "global", "variables": ["temperature", "salinity", "pressure"]}'),
('euro_argo', 'Euro-Argo Data Centre', 'https://www.euro-argo.eu/', 'argo', '{"region": "european", "variables": ["temperature", "salinity", "pressure"]}'),
('china_argo', 'China Argo Real-time Data Center', 'http://www.argo.org.cn/', 'argo', '{"region": "pacific", "variables": ["temperature", "salinity", "pressure"]}'),
('australia_argo', 'Australian ARGO Data Centre', 'http://www.imos.org.au/argo.html', 'argo', '{"region": "southern_ocean", "variables": ["temperature", "salinity", "pressure"]}'),
('france_argo', 'Coriolis ARGO Data Centre', 'http://www.coriolis.eu.org/', 'argo', '{"region": "atlantic", "variables": ["temperature", "salinity", "pressure"]}')
ON CONFLICT (source_id) DO NOTHING;

-- Create functions for common operations
CREATE OR REPLACE FUNCTION get_active_floats()
RETURNS TABLE (
    float_id VARCHAR(20),
    platform_number VARCHAR(20),
    deployment_latitude DOUBLE PRECISION,
    deployment_longitude DOUBLE PRECISION,
    last_update TIMESTAMP WITH TIME ZONE
) 
LANGUAGE SQL
AS $$
    SELECT float_id, platform_number, deployment_latitude, deployment_longitude, last_update
    FROM argo_floats 
    WHERE status = 'active'
    ORDER BY last_update DESC;
$$;

CREATE OR REPLACE FUNCTION get_recent_profiles(days_back INTEGER DEFAULT 30)
RETURNS TABLE (
    profile_id VARCHAR(50),
    float_id VARCHAR(20),
    date_time TIMESTAMP WITH TIME ZONE,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
)
LANGUAGE SQL
AS $$
    SELECT profile_id, float_id, date_time, latitude, longitude
    FROM argo_profiles 
    WHERE date_time >= NOW() - INTERVAL '1 day' * days_back
    ORDER BY date_time DESC;
$$;

-- Completion message
SELECT 'FloatChat ARGO Database Schema created successfully!' as status;