-- Fix Row Level Security policies for service role data insertion

-- Temporarily disable RLS for data population
ALTER TABLE argo_floats DISABLE ROW LEVEL SECURITY;
ALTER TABLE argo_profiles DISABLE ROW LEVEL SECURITY;
ALTER TABLE chat_sessions DISABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages DISABLE ROW LEVEL SECURITY;
ALTER TABLE data_processing_jobs DISABLE ROW LEVEL SECURITY;
ALTER TABLE vector_embeddings DISABLE ROW LEVEL SECURITY;

-- Re-create service role policies that actually work
CREATE POLICY "Service role can insert floats" ON argo_floats
    FOR INSERT TO service_role
    USING (true);

CREATE POLICY "Service role can insert profiles" ON argo_profiles
    FOR INSERT TO service_role  
    USING (true);

CREATE POLICY "Service role can insert chat_sessions" ON chat_sessions
    FOR INSERT TO service_role
    USING (true);

CREATE POLICY "Service role can insert chat_messages" ON chat_messages
    FOR INSERT TO service_role
    USING (true);

CREATE POLICY "Service role can insert jobs" ON data_processing_jobs
    FOR INSERT TO service_role
    USING (true);

CREATE POLICY "Service role can insert embeddings" ON vector_embeddings
    FOR INSERT TO service_role
    USING (true);

-- Re-enable RLS
ALTER TABLE argo_floats ENABLE ROW LEVEL SECURITY;
ALTER TABLE argo_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE data_processing_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE vector_embeddings ENABLE ROW LEVEL SECURITY;

SELECT 'RLS policies fixed for service role!' as status;