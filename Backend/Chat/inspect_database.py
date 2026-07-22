"""
Database Inspection Script - Check all table contents
"""
import os
import asyncio
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
url = os.getenv("SUPABASE_URL")
service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not url or not service_key:
    print("❌ Missing Supabase credentials in .env file")
    exit(1)

print(f"🔗 Connecting to: {url}")

async def inspect_database():
    try:
        supabase: Client = create_client(url, service_key)
        print("✅ Supabase client created successfully with service role")
        
        # List of all tables to inspect
        tables = [
            'data_sources',
            'argo_floats', 
            'argo_profiles',
            'chat_sessions',
            'chat_messages',
            'data_processing_jobs',
            'vector_embeddings'
        ]
        
        print("\n" + "="*60)
        print("📊 DATABASE TABLE INSPECTION")
        print("="*60)
        
        for table in tables:
            try:
                print(f"\n🗂️  TABLE: {table}")
                print("-" * 40)
                
                # Get count
                count_result = supabase.table(table).select("*", count="exact").execute()
                total_count = count_result.count
                
                # Get sample data (first 3 records)
                sample_result = supabase.table(table).select("*").limit(3).execute()
                sample_data = sample_result.data
                
                print(f"📊 Total Records: {total_count}")
                
                if total_count == 0:
                    print("⚠️  Table is EMPTY")
                else:
                    print(f"✅ Contains {total_count} records")
                    
                    if sample_data:
                        print("\n📋 Sample Records:")
                        for i, record in enumerate(sample_data[:2], 1):
                            print(f"  Record {i}:")
                            # Show key fields only
                            if table == 'data_sources':
                                print(f"    - ID: {record.get('source_id')}")
                                print(f"    - Name: {record.get('source_name')}")
                                print(f"    - Active: {record.get('is_active')}")
                            elif table == 'argo_floats':
                                print(f"    - Float ID: {record.get('float_id')}")
                                print(f"    - Platform: {record.get('platform_number')}")
                                print(f"    - Status: {record.get('status')}")
                            elif table == 'argo_profiles':
                                print(f"    - Profile ID: {record.get('profile_id')}")
                                print(f"    - Float ID: {record.get('float_id')}")
                                print(f"    - Date: {record.get('date_time')}")
                                print(f"    - Location: {record.get('latitude', 'N/A')}, {record.get('longitude', 'N/A')}")
                            elif table == 'chat_sessions':
                                print(f"    - Session ID: {record.get('session_id')}")
                                print(f"    - Status: {record.get('status')}")
                                print(f"    - Messages: {record.get('message_count', 0)}")
                            elif table == 'vector_embeddings':
                                print(f"    - Content ID: {record.get('content_id')}")
                                print(f"    - Type: {record.get('content_type')}")
                                print(f"    - Text Length: {len(record.get('content_text', ''))}")
                            else:
                                # Show first few fields for other tables
                                for key, value in list(record.items())[:3]:
                                    print(f"    - {key}: {value}")
                
            except Exception as e:
                print(f"❌ Error inspecting {table}: {str(e)}")
        
        print("\n" + "="*60)
        print("🔍 DATA POPULATION RECOMMENDATIONS")
        print("="*60)
        
        # Check which tables need data
        empty_tables = []
        for table in tables:
            try:
                result = supabase.table(table).select("*", count="exact").execute()
                if result.count == 0:
                    empty_tables.append(table)
            except:
                empty_tables.append(table)
        
        if empty_tables:
            print(f"\n⚠️  Empty Tables Found: {len(empty_tables)}")
            for table in empty_tables:
                if table == 'argo_floats':
                    print(f"\n🚀 To populate {table}:")
                    print("   - Run: await data_ingestion.ingest_all_sources()")
                    print("   - Or: await data_ingestion.generate_demo_profiles()")
                elif table == 'argo_profiles':
                    print(f"\n🚀 To populate {table}:")
                    print("   - Run data ingestion to fetch real ARGO data")
                    print("   - Will automatically populate when floats are ingested")
                elif table == 'vector_embeddings':
                    print(f"\n🚀 To populate {table}:")
                    print("   - Run: await vector_db.add_profiles(profiles)")
                    print("   - Will populate when ARGO profiles are processed")
                elif table == 'chat_sessions':
                    print(f"\n🚀 To populate {table}:")
                    print("   - Start chat conversations via API")
                    print("   - Sessions created automatically when users chat")
                else:
                    print(f"\n🚀 To populate {table}: Run respective service operations")
        else:
            print("\n✅ All tables have data!")
            
    except Exception as e:
        print(f"❌ Failed to inspect database: {str(e)}")

if __name__ == "__main__":
    asyncio.run(inspect_database())