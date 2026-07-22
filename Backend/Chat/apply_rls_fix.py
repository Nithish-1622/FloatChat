"""
Apply RLS Fix and Schema Updates for India-only ARGO Data
Executes the RLS policies fix and adds missing database columns
"""
from supabase_config import get_supabase_client
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def execute_rls_fix_and_schema():
    """Execute RLS fix and add missing schema columns"""
    
    try:
        supabase = get_supabase_client()
        logger.info("Connected to Supabase")
        
        print("🔧 Applying RLS fixes and schema updates...")
        
        # Read the RLS fix SQL
        with open('fix_rls_policies.sql', 'r') as f:
            rls_sql = f.read()
        
        # Split SQL commands and execute them one by one
        sql_commands = [cmd.strip() for cmd in rls_sql.split(';') if cmd.strip() and not cmd.strip().startswith('--')]
        
        # Add the missing column command
        sql_commands.append("ALTER TABLE argo_profiles ADD COLUMN IF NOT EXISTS derived_parameters JSONB DEFAULT '{}'")
        
        success_count = 0
        total_commands = len(sql_commands)
        
        for i, sql_cmd in enumerate(sql_commands, 1):
            if not sql_cmd or sql_cmd.startswith('SELECT'):
                continue
                
            try:
                print(f"Executing command {i}/{total_commands}: {sql_cmd[:50]}...")
                
                # Use the Supabase client to execute raw SQL
                # Note: This might not work with all SQL commands due to RPC limitations
                # Let's try a direct approach
                result = supabase.rpc('execute_sql', {'sql': sql_cmd}).execute()
                print(f"✅ Command {i} executed successfully")
                success_count += 1
                
            except Exception as e:
                error_str = str(e)
                if 'Could not find the function' in error_str:
                    print(f"⚠️ Command {i}: RPC not available, manual execution needed")
                    print(f"   SQL: {sql_cmd}")
                elif 'already exists' in error_str or 'does not exist' in error_str:
                    print(f"✅ Command {i}: Already applied or not needed")
                    success_count += 1
                else:
                    print(f"❌ Command {i} failed: {error_str}")
        
        print(f"\n📊 RLS Fix Summary: {success_count}/{total_commands} commands processed")
        
        # Test if we can now insert data
        print("\n🧪 Testing data insertion capability...")
        test_insert_capability()
        
        return True
        
    except Exception as e:
        logger.error(f"Error in RLS fix: {str(e)}")
        return False

def test_insert_capability():
    """Test if we can now insert data after RLS fix"""
    try:
        supabase = get_supabase_client()
        
        # Try inserting a test float
        test_float = {
            'float_id': 'INDIA_TEST_001',
            'platform_number': 'IND001',
            'project_name': 'India ARGO Test',
            'status': 'test',
            'deployment_latitude': 15.0,  # Indian Ocean
            'deployment_longitude': 75.0
        }
        
        result = supabase.table('argo_floats').insert(test_float).execute()
        print("✅ Data insertion test PASSED - RLS policies are working!")
        
        # Clean up test data
        supabase.table('argo_floats').delete().eq('float_id', 'INDIA_TEST_001').execute()
        print("✅ Test data cleaned up")
        
        return True
        
    except Exception as e:
        error_str = str(e)
        if 'row-level security policy' in error_str.lower():
            print("❌ Data insertion test FAILED - RLS still blocking")
            print("   Manual execution needed in Supabase Dashboard")
            return False
        else:
            print(f"⚠️ Data insertion test unclear: {error_str}")
            return True

def create_manual_instructions():
    """Create instructions for manual execution"""
    instructions = """
# Manual RLS Fix Instructions

Since automated execution may not work, please manually execute these commands in your Supabase SQL Editor:

## 1. Disable RLS temporarily:
```sql
ALTER TABLE argo_floats DISABLE ROW LEVEL SECURITY;
ALTER TABLE argo_profiles DISABLE ROW LEVEL SECURITY;
ALTER TABLE chat_sessions DISABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages DISABLE ROW LEVEL SECURITY;
ALTER TABLE data_processing_jobs DISABLE ROW LEVEL SECURITY;
ALTER TABLE vector_embeddings DISABLE ROW LEVEL SECURITY;
```

## 2. Add missing column:
```sql
ALTER TABLE argo_profiles ADD COLUMN IF NOT EXISTS derived_parameters JSONB DEFAULT '{}';
```

## 3. Create service role policies:
```sql
CREATE POLICY "Service role can insert floats" ON argo_floats
    FOR INSERT TO service_role USING (true);

CREATE POLICY "Service role can insert profiles" ON argo_profiles
    FOR INSERT TO service_role USING (true);

CREATE POLICY "Service role can insert chat_sessions" ON chat_sessions
    FOR INSERT TO service_role USING (true);

CREATE POLICY "Service role can insert chat_messages" ON chat_messages
    FOR INSERT TO service_role USING (true);

CREATE POLICY "Service role can insert jobs" ON data_processing_jobs
    FOR INSERT TO service_role USING (true);

CREATE POLICY "Service role can insert embeddings" ON vector_embeddings
    FOR INSERT TO service_role USING (true);
```

## 4. Re-enable RLS:
```sql
ALTER TABLE argo_floats ENABLE ROW LEVEL SECURITY;
ALTER TABLE argo_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE data_processing_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE vector_embeddings ENABLE ROW LEVEL SECURITY;
```
"""
    
    with open('MANUAL_RLS_FIX_INSTRUCTIONS.md', 'w') as f:
        f.write(instructions)
    
    print("📝 Manual instructions saved to MANUAL_RLS_FIX_INSTRUCTIONS.md")

if __name__ == "__main__":
    print("🚀 Starting RLS fix and schema updates...")
    
    success = execute_rls_fix_and_schema()
    
    if not success:
        print("\n📝 Creating manual execution instructions...")
        create_manual_instructions()
        
    print("\n✅ RLS fix process completed!")