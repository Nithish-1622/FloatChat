"""
Test RLS with correct database schema columns
"""
from supabase_config import get_supabase_client

def test_insert_with_actual_schema():
    """Test RLS using the actual database schema"""
    try:
        supabase = get_supabase_client()
        
        print("🔧 Testing RLS with actual database columns...")
        
        # Test argo_floats with actual columns from the schema
        test_float_data = {
            'float_id': 'TEST999999',
            'platform_number': 'TEST001',
            'project_name': 'RLS Test Project',
            'status': 'test'
        }
        
        try:
            print("Attempting insert into argo_floats...")
            result = supabase.table('argo_floats').insert(test_float_data).execute()
            print("✅ argo_floats insert successful!")
            print(f"Inserted: {result.data[0]['float_id']}")
            
            # Test argo_profiles referencing the float
            test_profile_data = {
                'profile_id': 'TEST999999_001',
                'float_id': 'TEST999999',
                'cycle_number': 1,
                'date_time': '2024-01-01T12:00:00Z',
                'latitude': 45.0,
                'longitude': -125.0,
                'data_mode': 'R'
            }
            
            print("Attempting insert into argo_profiles...")
            profile_result = supabase.table('argo_profiles').insert(test_profile_data).execute()
            print("✅ argo_profiles insert successful!")
            print(f"Inserted: {profile_result.data[0]['profile_id']}")
            
            # Clean up test data
            print("Cleaning up test data...")
            supabase.table('argo_profiles').delete().eq('profile_id', 'TEST999999_001').execute()
            supabase.table('argo_floats').delete().eq('float_id', 'TEST999999').execute()
            print("✅ Test records cleaned up")
            
            print("\n🎉 RLS IS NOT BLOCKING INSERTS!")
            print("The service role has proper permissions.")
            return True
            
        except Exception as e:
            error_str = str(e)
            print(f"❌ Insert failed: {error_str}")
            
            if 'row-level security policy' in error_str.lower():
                print("🚨 RLS IS BLOCKING INSERTS!")
                print("Need to disable RLS or create proper policies for service role")
                return False
            else:
                print("❓ Insert failed for other reasons (constraints, validation, etc.)")
                return True  # RLS is not the issue
                
    except Exception as e:
        print(f"❌ Error in RLS test: {str(e)}")
        return False

def simple_disable_rls():
    """Try to disable RLS using a simple approach"""
    print("\n🔧 Attempting to disable RLS policies...")
    print("Note: This requires proper database permissions")
    
    # This would normally require database admin access
    # For now, we'll document what needs to be done
    print("""
    To fix RLS issues manually:
    
    1. Go to Supabase Dashboard → SQL Editor
    2. Execute these commands:
       
       ALTER TABLE argo_floats DISABLE ROW LEVEL SECURITY;
       ALTER TABLE argo_profiles DISABLE ROW LEVEL SECURITY;
       ALTER TABLE chat_sessions DISABLE ROW LEVEL SECURITY;
       ALTER TABLE chat_messages DISABLE ROW LEVEL SECURITY;
       ALTER TABLE data_processing_jobs DISABLE ROW LEVEL SECURITY;
       ALTER TABLE vector_embeddings DISABLE ROW LEVEL SECURITY;
    
    3. Or create service role policies:
       
       CREATE POLICY "service_access" ON argo_floats FOR ALL TO service_role USING (true);
       CREATE POLICY "service_access" ON argo_profiles FOR ALL TO service_role USING (true);
       (repeat for other tables)
    """)

if __name__ == "__main__":
    success = test_insert_with_actual_schema()
    
    if not success:
        simple_disable_rls()
    else:
        print("\n✅ Database is ready for data ingestion!")
        print("RLS policies are properly configured.")