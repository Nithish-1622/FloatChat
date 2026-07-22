"""
Check and Update RLS Policies - Alternative approach
Uses REST API to temporarily disable RLS on tables
"""
import asyncio
from supabase_config import get_supabase_client
import requests
import os

def check_table_permissions():
    """Check current table permissions and RLS status"""
    try:
        supabase = get_supabase_client()
        
        # Test inserting into each table to see current permissions
        tables_to_test = ['argo_floats', 'argo_profiles', 'chat_sessions', 'chat_messages', 'data_processing_jobs', 'vector_embeddings']
        
        print("🔍 Testing table permissions...")
        
        for table in tables_to_test:
            try:
                # Try a simple select first
                result = supabase.table(table).select("*").limit(1).execute()
                print(f"✅ {table}: READ access OK")
                
                # Try inserting a test record (will fail due to constraints but will show RLS status)
                if table == 'argo_floats':
                    test_data = {
                        'float_id': 'TEST_RLS_CHECK',
                        'platform_type': 'TEST',
                        'wmo_id': 'TEST123',
                        'deployment_date': '2024-01-01',
                        'status': 'TEST',
                        'last_location_date': '2024-01-01T00:00:00Z',
                        'last_location_latitude': 0.0,
                        'last_location_longitude': 0.0,
                        'source': 'test_rls'
                    }
                    
                    try:
                        insert_result = supabase.table(table).insert(test_data).execute()
                        print(f"✅ {table}: INSERT access OK")
                        # Clean up the test record
                        supabase.table(table).delete().eq('float_id', 'TEST_RLS_CHECK').execute()
                    except Exception as e:
                        if 'row-level security policy' in str(e):
                            print(f"❌ {table}: RLS policy blocking inserts - {str(e)}")
                        else:
                            print(f"⚠️  {table}: INSERT failed (but not due to RLS) - {str(e)}")
                            
            except Exception as e:
                print(f"❌ {table}: Access failed - {str(e)}")
                
        return True
        
    except Exception as e:
        print(f"❌ Error checking permissions: {str(e)}")
        return False

def create_bypass_user_policies():
    """Create policies that bypass RLS for authenticated users"""
    try:
        supabase = get_supabase_client()
        
        # For now, let's just try to insert with the current authentication
        # The real fix would be done in Supabase dashboard or with database admin privileges
        
        print("🔧 Current approach: Testing direct insertion...")
        
        # Try creating a simple test float to see what happens
        test_float_data = {
            'float_id': 'RLS_TEST_001',
            'platform_type': 'APEX',
            'wmo_id': 'TEST001',
            'deployment_date': '2024-01-01',
            'status': 'ACTIVE',
            'last_location_date': '2024-01-01T00:00:00Z',
            'last_location_latitude': 45.0,
            'last_location_longitude': -125.0,
            'source': 'test_bypass'
        }
        
        try:
            result = supabase.table('argo_floats').insert(test_float_data).execute()
            print("✅ Direct insertion successful!")
            
            # Clean up
            supabase.table('argo_floats').delete().eq('float_id', 'RLS_TEST_001').execute()
            print("✅ Test record cleaned up")
            return True
            
        except Exception as e:
            print(f"❌ Direct insertion failed: {str(e)}")
            
            if 'row-level security policy' in str(e):
                print("\n💡 RLS is blocking the insert. Need to fix policies.")
                print("   Recommended solutions:")
                print("   1. Access Supabase dashboard → Authentication → RLS")  
                print("   2. Temporarily disable RLS on affected tables")
                print("   3. Or create policies that allow service_role access")
                
        return False
        
    except Exception as e:
        print(f"❌ Error in bypass attempt: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 Checking RLS status and table permissions...\n")
    
    check_table_permissions()
    
    print("\n🔧 Attempting to create bypass policies...")
    create_bypass_user_policies()