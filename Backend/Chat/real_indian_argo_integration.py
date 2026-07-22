#!/usr/bin/env python3
"""
Real Indian ARGO Data Integration
Integrates IFREMER-based real ARGO data fetching with FloatChat system
"""

import sys
sys.path.append('.')

from ifremer_http_fetcher import IfremerHttpArgoFetcher
from supabase_data_storage import SupabaseDataStorageService
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealIndianArgoIntegration:
    """Integrates real ARGO data fetching with FloatChat system"""
    
    def __init__(self):
        self.fetcher = IfremerHttpArgoFetcher()
        self.storage = SupabaseDataStorageService()
    
    def clear_existing_data(self):
        """Clear all existing ARGO data to replace with real data"""
        if not self.storage.is_available:
            logger.error("Storage service not available")
            return False
        
        try:
            logger.info("🧹 Clearing existing synthetic data...")
            
            # Clear profiles first (due to foreign key constraint)
            profiles = self.storage.supabase_client.table('argo_profiles').select('profile_id').execute()
            if profiles.data:
                for profile in profiles.data:
                    self.storage.supabase_client.table('argo_profiles').delete().eq('profile_id', profile['profile_id']).execute()
                logger.info(f"Cleared {len(profiles.data)} existing profiles")
            
            # Clear floats
            floats = self.storage.supabase_client.table('argo_floats').select('float_id').execute()
            if floats.data:
                for float_data in floats.data:
                    self.storage.supabase_client.table('argo_floats').delete().eq('float_id', float_data['float_id']).execute()
                logger.info(f"Cleared {len(floats.data)} existing floats")
            
            return True
            
        except Exception as e:
            logger.error(f"Error clearing data: {e}")
            return False
    
    def convert_profile_to_argo_format(self, profile_data: dict) -> dict:
        """Convert fetched profile to ARGO format for storage"""
        try:
            # Extract basic info
            float_id = profile_data.get('platform_number', f'IN{hash(str(profile_data)) % 9999999}')
            
            # Handle datetime conversion
            date_obj = profile_data.get('date', datetime.now())
            if isinstance(date_obj, datetime):
                date_str = date_obj.isoformat()
            else:
                date_str = str(date_obj)
            
            # Create float record - matching actual schema
            float_record = {
                'float_id': float_id,
                'platform_number': float_id,
                'project_name': profile_data.get('project_name', 'INDIAN_ARGO'),
                'pi_name': profile_data.get('pi_name', 'Indian ARGO Team'),
                'deployment_date': date_str,
                'deployment_latitude': profile_data.get('latitude', 0.0),
                'deployment_longitude': profile_data.get('longitude', 0.0),
                'wmo_inst_type': profile_data.get('platform_type', 'FLOAT')[:10],
                'status': 'active'
            }
            
            # Create profile record - matching actual schema
            profile_id = f"{float_id}_{profile_data.get('cycle_number', 1)}"
            profile_record = {
                'profile_id': profile_id,
                'float_id': float_id,
                'cycle_number': profile_data.get('cycle_number', 1),
                'date_time': date_str,
                'latitude': profile_data.get('latitude', 0.0),
                'longitude': profile_data.get('longitude', 0.0),
                'data_mode': 'R',  # Real-time
                'data_centre': profile_data.get('data_centre', 'INCOIS'),
                'ocean_basin': profile_data.get('region', 'Indian_Ocean'),
                'measurements': profile_data.get('measurements', [])
            }
            
            return {
                'float': float_record,
                'profile': profile_record
            }
            
        except Exception as e:
            logger.error(f"Error converting profile: {e}")
            return {}
    
    def store_real_argo_data(self, profiles_data: list) -> dict:
        """Store real ARGO data in the database"""
        if not self.storage.is_available:
            return {'success': False, 'error': 'Storage not available'}
        
        results = {'floats_stored': 0, 'profiles_stored': 0, 'errors': []}
        stored_floats = set()
        
        try:
            for profile_data in profiles_data:
                converted = self.convert_profile_to_argo_format(profile_data)
                if not converted:
                    continue
                
                float_record = converted['float']
                profile_record = converted['profile']
                
                try:
                    # Store float if not already stored
                    float_id = float_record['float_id']
                    if float_id not in stored_floats:
                        # Check if float exists
                        existing = self.storage.supabase_client.table('argo_floats').select('*').eq('float_id', float_id).execute()
                        
                        if not existing.data:
                            # Create new float
                            self.storage.supabase_client.table('argo_floats').insert(float_record).execute()
                            results['floats_stored'] += 1
                        else:
                            # Update existing float
                            self.storage.supabase_client.table('argo_floats').update(float_record).eq('float_id', float_id).execute()
                        
                        stored_floats.add(float_id)
                    
                    # Store profile
                    profile_id = profile_record['profile_id']
                    existing_profile = self.storage.supabase_client.table('argo_profiles').select('*').eq('profile_id', profile_id).execute()
                    
                    if not existing_profile.data:
                        self.storage.supabase_client.table('argo_profiles').insert(profile_record).execute()
                        results['profiles_stored'] += 1
                    
                except Exception as e:
                    error_msg = f"Error storing {float_id}: {e}"
                    results['errors'].append(error_msg)
                    logger.error(error_msg)
                    continue
            
            results['success'] = True
            return results
            
        except Exception as e:
            logger.error(f"Storage error: {e}")
            return {'success': False, 'error': str(e)}
    
    def run_real_data_integration(self, max_profiles: int = 40):
        """Main integration process"""
        print("🇮🇳 Real Indian ARGO Data Integration")
        print("=" * 50)
        
        # Step 1: Fetch real data
        logger.info("Step 1: Fetching real Indian Ocean ARGO data...")
        profiles_data = self.fetcher.fetch_indian_argo_data(max_profiles=max_profiles)
        
        if not profiles_data:
            print("❌ Failed to fetch real ARGO data")
            return False
        
        print(f"✅ Fetched {len(profiles_data)} real Indian Ocean profiles")
        
        # Step 2: Clear existing synthetic data
        logger.info("Step 2: Clearing existing synthetic data...")
        if not self.clear_existing_data():
            print("❌ Failed to clear existing data")
            return False
        
        print("✅ Cleared existing synthetic data")
        
        # Step 3: Store real data
        logger.info("Step 3: Storing real ARGO data...")
        results = self.store_real_argo_data(profiles_data)
        
        if not results.get('success'):
            print(f"❌ Failed to store data: {results.get('error')}")
            return False
        
        print(f"✅ Stored {results['floats_stored']} floats and {results['profiles_stored']} profiles")
        
        if results['errors']:
            print(f"⚠️ {len(results['errors'])} errors occurred during storage")
        
        # Step 4: Verify data
        logger.info("Step 4: Verifying stored data...")
        floats = self.storage.supabase_client.table('argo_floats').select('*').execute()
        profiles = self.storage.supabase_client.table('argo_profiles').select('*').execute()
        
        print(f"📊 Final verification:")
        print(f"   Floats in database: {len(floats.data)}")
        print(f"   Profiles in database: {len(profiles.data)}")
        
        # Regional breakdown
        if profiles.data:
            regions = {}
            for profile in profiles.data:
                region = profile.get('region', 'Unknown')
                regions[region] = regions.get(region, 0) + 1
            
            print(f"🗺️ Regional distribution:")
            for region, count in regions.items():
                print(f"   {region.replace('_', ' ')}: {count} profiles")
        
        print("\n🎉 Real Indian ARGO data integration completed successfully!")
        print("Your FloatChat system now uses REAL Indian Ocean ARGO data!")
        
        return True

def main():
    integration = RealIndianArgoIntegration()
    integration.run_real_data_integration(max_profiles=35)

if __name__ == '__main__':
    main()