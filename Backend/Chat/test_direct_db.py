"""
Direct SQL test for Supabase tables - bypasses PostgREST API
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Get database connection details from Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not supabase_url:
    print("❌ Missing SUPABASE_URL")
    exit(1)

# Extract connection details from Supabase URL
# Format: https://[project-id].supabase.co
project_id = supabase_url.split("//")[1].split(".")[0]
db_host = f"db.{project_id}.supabase.co"
db_port = 5432
db_name = "postgres"
db_user = "postgres"

# You need to get the database password from Supabase Settings > Database > Connection string
# For now, let's try to get it from environment or ask user to provide it
db_password = os.getenv("SUPABASE_DB_PASSWORD")

if not db_password:
    print("❌ Missing SUPABASE_DB_PASSWORD in .env file")
    print("💡 Go to Supabase Dashboard > Settings > Database > Connection string to find the password")
    print("💡 Add SUPABASE_DB_PASSWORD=your_db_password to your .env file")
    exit(1)

try:
    print(f"🔗 Connecting to PostgreSQL database: {db_host}")
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )
    
    cursor = conn.cursor()
    print("✅ Direct PostgreSQL connection successful!")
    
    # Check if tables exist
    tables_to_check = [
        'data_sources',
        'argo_floats', 
        'argo_profiles',
        'chat_sessions',
        'chat_messages',
        'data_processing_jobs',
        'vector_embeddings'
    ]
    
    print("\n📊 Checking table existence:")
    for table in tables_to_check:
        cursor.execute(f"""
            SELECT COUNT(*)
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = '{table}';
        """)
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"✅ Table '{table}' exists")
            
            # Check row count
            cursor.execute(f"SELECT COUNT(*) FROM public.{table};")
            row_count = cursor.fetchone()[0]
            print(f"   📊 Contains {row_count} rows")
        else:
            print(f"❌ Table '{table}' does not exist")
    
    cursor.close()
    conn.close()
    
    print(f"\n💡 If tables exist but API fails, try refreshing the Supabase schema cache:")
    print(f"   Go to Supabase Dashboard > Settings > API > Refresh Schema")
    
except psycopg2.Error as e:
    print(f"❌ PostgreSQL connection failed: {e}")
    print("💡 Make sure SUPABASE_DB_PASSWORD is correct in your .env file")
except Exception as e:
    print(f"❌ Unexpected error: {e}")