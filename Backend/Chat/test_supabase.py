"""
Simple test script to check if Supabase tables exist
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
url = os.getenv("SUPABASE_URL")
anon_key = os.getenv("SUPABASE_ANON_KEY")
service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not url or not anon_key:
    print("❌ Missing Supabase credentials in .env file")
    exit(1)

print(f"🔗 Connecting to: {url}")

# Try with service role key first (has full access)
if service_key:
    print("🔑 Testing with SERVICE ROLE key...")
    try:
        supabase: Client = create_client(url, service_key)
        print("✅ Supabase client created successfully with service role")
    except Exception as e:
        print(f"❌ Service role connection failed: {e}")
        supabase = None
else:
    print("🔑 Testing with ANON key...")
    try:
        supabase: Client = create_client(url, anon_key)
        print("✅ Supabase client created successfully with anon key")
    except Exception as e:
        print(f"❌ Anon connection failed: {e}")
        supabase = None

if not supabase:
    print("❌ Could not create Supabase client")
    exit(1)
    
# Test different tables
tables_to_test = [
    'data_sources',
    'argo_floats', 
    'argo_profiles',
    'chat_sessions',
    'chat_messages',
    'data_processing_jobs',
    'vector_embeddings'
]

for table in tables_to_test:
    try:
        result = supabase.table(table).select("*").limit(1).execute()
        print(f"✅ Table '{table}' exists and accessible")
    except Exception as e:
        print(f"❌ Table '{table}' error: {str(e)}")

print("\n📊 Testing data_sources table specifically:")
try:
    # Test if we can select from data_sources
    result = supabase.table('data_sources').select('source_id, source_name').execute()
    print(f"✅ data_sources query successful: {len(result.data)} records found")
    
    if result.data:
        print("📋 Found data sources:")
        for source in result.data:
            print(f"  - {source.get('source_id')}: {source.get('source_name')}")
    else:
        print("📋 data_sources table exists but is empty")
        
except Exception as e:
    print(f"❌ data_sources query failed: {str(e)}")

print("\n✅ Test completed!")