"""
Database Population Script - Add initial data to all tables
"""
import asyncio
import sys
sys.path.append('.')

from supabase_data_storage import SupabaseDataStorageService
from services.comprehensive_data_ingestion import ComprehensiveArgoDataIngestion
from services.vector_database import ArgoVectorDatabase
from services.conversational_ai import ArgoConversationalAI

async def populate_database():
    print("🌊 FloatChat Database Population Starting...")
    print("="*60)
    
    # Initialize services
    print("\n🔧 Initializing services...")
    data_storage = SupabaseDataStorageService()
    data_ingestion = ComprehensiveArgoDataIngestion()
    vector_db = ArgoVectorDatabase()
    ai_service = ArgoConversationalAI()
    
    if not data_storage.is_available:
        print("❌ Data storage service not available")
        return
    
    print("✅ All services initialized")
    
    try:
        # 1. Generate and store demo ARGO profiles
        print("\n📊 Step 1: Generating demo ARGO profiles...")
        demo_profiles = await data_ingestion.generate_demo_profiles(count=10, region="global")
        print(f"✅ Generated {len(demo_profiles)} demo profiles")
        
        # Store profiles in database
        storage_result = await data_storage.store_argo_profiles(demo_profiles, "demo_initialization")
        print(f"✅ Stored profiles in database: {storage_result.get('message', 'Success')}")
        
        # 2. Create sample chat session
        print("\n💬 Step 2: Creating sample chat session...")
        chat_result = await ai_service.process_query(
            "What is ARGO and how does it work?",
            session_id="demo_session_001",
            conversation_type="education",
            user_id="system_demo"
        )
        print(f"✅ Created chat session: {chat_result.get('session_id')}")
        print(f"   Response preview: {chat_result.get('response', '')[:100]}...")
        
        # 3. Add profiles to vector database
        print("\n🔍 Step 3: Adding profiles to vector database...")
        if len(demo_profiles) > 0:
            try:
                vector_result = await vector_db.add_profiles(demo_profiles[:5])  # Add first 5 profiles
                print(f"✅ Added profiles to vector database")
            except Exception as e:
                print(f"⚠️  Vector database population failed: {str(e)}")
        
        # 4. Create a processing job record
        print("\n⚙️ Step 4: Creating sample processing job...")
        job_data = {
            'job_id': 'demo_ingestion_001',
            'job_type': 'data_ingestion',
            'status': 'completed',
            'progress': 100,
            'parameters': {'source': 'demo', 'profiles_count': len(demo_profiles)},
            'results': {'profiles_processed': len(demo_profiles), 'profiles_stored': len(demo_profiles)}
        }
        
        job_result = data_storage.supabase_client.table('data_processing_jobs').insert(job_data).execute()
        print(f"✅ Created processing job record")
        
        print("\n" + "="*60)
        print("🎉 DATABASE POPULATION COMPLETED!")
        print("="*60)
        
        # Run final inspection
        print("\n📊 Final Database Status:")
        await run_quick_inspection()
        
    except Exception as e:
        print(f"❌ Error during database population: {str(e)}")
        import traceback
        traceback.print_exc()

async def run_quick_inspection():
    """Quick inspection of table counts"""
    from supabase_config import get_supabase_client
    
    supabase = get_supabase_client(admin=True)
    tables = ['data_sources', 'argo_floats', 'argo_profiles', 'chat_sessions', 'chat_messages', 'data_processing_jobs', 'vector_embeddings']
    
    for table in tables:
        try:
            result = supabase.table(table).select("*", count="exact").execute()
            count = result.count
            status = "✅" if count > 0 else "❌"
            print(f"   {status} {table}: {count} records")
        except Exception as e:
            print(f"   ❌ {table}: Error - {str(e)}")

if __name__ == "__main__":
    asyncio.run(populate_database())