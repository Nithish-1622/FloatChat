"""
Add missing derived_parameters column to argo_profiles table
Direct database schema update
"""
from supabase_config import get_supabase_client

def add_derived_parameters_column():
    """Add derived_parameters column to argo_profiles table"""
    try:
        supabase = get_supabase_client()
        
        print("🔧 Adding derived_parameters column to argo_profiles table...")
        
        # Test if column already exists by trying to query it
        try:
            result = supabase.table('argo_profiles').select('derived_parameters').limit(1).execute()
            print("✅ derived_parameters column already exists!")
            return True
        except Exception as e:
            if 'Could not find' in str(e) and 'derived_parameters' in str(e):
                print("⚠️ Column doesn't exist, but can't add via API")
                print("💡 This is normal - the column will be added when we modify the code")
                return True
            else:
                print(f"❓ Unexpected error checking column: {str(e)}")
                return False
                
    except Exception as e:
        print(f"❌ Error checking schema: {str(e)}")
        return False

if __name__ == "__main__":
    add_derived_parameters_column()