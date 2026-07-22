"""
Check actual database schema and test RLS
Uses only existing columns from the database
"""
from supabase_config import get_supabase_client

def check_actual_schema():
    """Check what columns actually exist in the tables"""
    try:
        supabase = get_supabase_client()
        
        print("🔍 Checking actual table schema...")
        
        # Get sample records to see actual columns
        tables = ['argo_floats', 'argo_profiles', 'data_sources']
        
        for table in tables:
            try:
                result = supabase.table(table).select("*").limit(1).execute()
                if result.data:
                    print(f"\n✅ {table} - Columns available:")
                    for col in result.data[0].keys():
                        print(f"   - {col}")
                else:
                    print(f"\n⚠️  {table} - No data to show column structure")
                    
            except Exception as e:
                print(f"❌ {table}: {str(e)}")
                
    except Exception as e:
        print(f"❌ Error checking schema: {str(e)}")

def test_rls_with_correct_columns():
    """Test RLS with correct column names"""
    try:
        supabase = get_supabase_client()
        
        print("\n🔧 Testing RLS with correct column structure...")
        
        # Test with minimal argo_floats data using actual columns
        test_float_data = {
            'float_id': 'RLS_TEST_002',
            'wmo_id': 'TEST002',
            'status': 'TEST',
            'source': 'test_rls'
        }
        
        try:
            print("Attempting insert into argo_floats...")
            result = supabase.table('argo_floats').insert(test_float_data).execute()
            print("✅ Insert successful! RLS is NOT blocking.")
            print(f"Inserted record: {result.data}")
            
            # Clean up
            supabase.table('argo_floats').delete().eq('float_id', 'RLS_TEST_002').execute()
            print("✅ Test record cleaned up")
            return True
            
        except Exception as e:
            error_str = str(e)
            print(f"❌ Insert failed: {error_str}")
            
            if 'row-level security policy' in error_str.lower():
                print("🚨 RLS IS BLOCKING INSERTS")
                return False
            elif 'violates' in error_str:
                print("⚠️  Insert blocked by database constraints (not RLS)")
                return True  # RLS is not the issue
            else:
                print("❓ Unknown error - might not be RLS related")
                return False
                
    except Exception as e:
        print(f"❌ Error in RLS test: {str(e)}")
        return False

if __name__ == "__main__":
    check_actual_schema()
    test_rls_with_correct_columns()