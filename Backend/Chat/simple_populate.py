"""
Simple Database Population Script - Direct SQL inserts to bypass RLS
"""
import os
import asyncio
from supabase import create_client, Client
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta
import random

load_dotenv()

async def populate_with_direct_sql():
    """Populate database using direct SQL to bypass RLS policies"""
    
    # Initialize Supabase client with service role
    url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not service_key:
        print("❌ Missing Supabase credentials")
        return
    
    supabase: Client = create_client(url, service_key)
    print("✅ Connected to Supabase with service role")
    
    try:
        print("\n🗄️ Step 1: Creating sample ARGO floats...")
        
        # Insert sample floats directly
        float_data = []
        for i in range(5):
            float_id = f"DEMO_{5000000 + i}"
            float_data.append({
                'float_id': float_id,
                'platform_number': f"PLAT_{i+1}",
                'project_name': 'Demo FloatChat Project',
                'deployment_latitude': round(random.uniform(-60, 60), 6),
                'deployment_longitude': round(random.uniform(-180, 180), 6),
                'status': 'active',
                'metadata': json.dumps({'demo': True, 'created_by': 'system'})
            })
        
        # Use raw SQL to bypass RLS
        for float_record in float_data:
            try:
                result = supabase.table('argo_floats').insert(float_record).execute()
                print(f"   ✅ Created float: {float_record['float_id']}")
            except Exception as e:
                print(f"   ❌ Failed to create float {float_record['float_id']}: {str(e)}")
        
        print("\n🌊 Step 2: Creating sample ARGO profiles...")
        
        # Create profiles for each float
        profile_data = []
        base_date = datetime.now() - timedelta(days=30)
        
        for i, float_record in enumerate(float_data):
            for cycle in range(3):  # 3 profiles per float
                profile_date = base_date + timedelta(days=cycle*5)
                profile_id = f"{float_record['float_id']}_{cycle+1}"
                
                # Random oceanographic measurements
                temp_measurements = [round(random.uniform(2.5, 25.0), 2) for _ in range(50)]
                salinity_measurements = [round(random.uniform(34.0, 37.5), 2) for _ in range(50)]
                pressure_measurements = [round(random.uniform(0, 2000), 1) for _ in range(50)]
                
                measurements = {
                    'temperature': temp_measurements,
                    'salinity': salinity_measurements, 
                    'pressure': pressure_measurements,
                    'depth_levels': 50
                }
                
                profile_data.append({
                    'profile_id': profile_id,
                    'float_id': float_record['float_id'],
                    'cycle_number': cycle + 1,
                    'date_time': profile_date.isoformat(),
                    'latitude': float_record['deployment_latitude'] + random.uniform(-2, 2),
                    'longitude': float_record['deployment_longitude'] + random.uniform(-2, 2),
                    'measurements': json.dumps(measurements),
                    'data_mode': 'R',
                    'ocean_basin': 'Demo Ocean'
                })
        
        # Insert profiles
        for profile_record in profile_data:
            try:
                result = supabase.table('argo_profiles').insert(profile_record).execute()
                print(f"   ✅ Created profile: {profile_record['profile_id']}")
            except Exception as e:
                print(f"   ❌ Failed to create profile {profile_record['profile_id']}: {str(e)}")
        
        print("\n💬 Step 3: Creating sample chat session...")
        
        # Create chat session
        session_data = {
            'session_id': 'demo_session_001',
            'user_id': 'demo_user',
            'session_name': 'Demo ARGO Chat Session',
            'status': 'active',
            'message_count': 2,
            'session_data': json.dumps({'demo': True, 'topic': 'ARGO introduction'})
        }
        
        try:
            supabase.table('chat_sessions').insert(session_data).execute()
            print(f"   ✅ Created chat session: {session_data['session_id']}")
            
            # Create sample messages
            messages = [
                {
                    'message_id': 'msg_001',
                    'session_id': 'demo_session_001',
                    'role': 'user',
                    'content': 'What is ARGO and how does it work?',
                    'token_count': 8,
                    'context_data': json.dumps({'query_type': 'educational'})
                },
                {
                    'message_id': 'msg_002', 
                    'session_id': 'demo_session_001',
                    'role': 'assistant',
                    'content': 'ARGO is a global ocean observing system that uses autonomous floats to collect temperature, salinity, and pressure data from the ocean. These floats dive to depths of up to 2000 meters, drift with currents, and surface regularly to transmit data via satellite.',
                    'token_count': 45,
                    'response_time_ms': 1250,
                    'context_data': json.dumps({'sources': ['demo'], 'confidence': 0.9})
                }
            ]
            
            for message in messages:
                supabase.table('chat_messages').insert(message).execute()
                print(f"   ✅ Created message: {message['message_id']}")
                
        except Exception as e:
            print(f"   ❌ Failed to create chat data: {str(e)}")
        
        print("\n📊 Final Database Status:")
        await check_table_counts(supabase)
        
    except Exception as e:
        print(f"❌ Error during population: {str(e)}")

async def check_table_counts(supabase):
    """Check final table counts"""
    tables = ['data_sources', 'argo_floats', 'argo_profiles', 'chat_sessions', 'chat_messages', 'data_processing_jobs']
    
    for table in tables:
        try:
            result = supabase.table(table).select("*", count="exact").execute()
            count = result.count
            status = "✅" if count > 0 else "❌"
            print(f"   {status} {table}: {count} records")
        except Exception as e:
            print(f"   ❌ {table}: Error - {str(e)}")

if __name__ == "__main__":
    asyncio.run(populate_with_direct_sql())