#!/usr/bin/env python3
"""
IFREMER ARGO Data Fetcher for Indian Ocean Floats
Fetches real ARGO data from ftp.ifremer.fr/ifremer/argo
Focuses on Indian Ocean region and INCOIS data center
"""

import ftplib
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import logging
import netCDF4 as nc
from typing import List, Dict, Any, Optional
import requests
from urllib.parse import urljoin
import tempfile
import gzip

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IfremerArgoFetcher:
    """Fetches ARGO data from IFREMER FTP server focusing on Indian Ocean"""
    
    def __init__(self):
        self.ftp_host = "ftp.ifremer.fr"
        self.base_path = "/ifremer/argo"
        self.indian_ocean_bounds = {
            'lat_min': -50.0,  # Southern Indian Ocean
            'lat_max': 30.0,   # Northern Arabian Sea/Bay of Bengal
            'lon_min': 30.0,   # Western Indian Ocean
            'lon_max': 120.0   # Eastern Bay of Bengal/Indonesian waters
        }
        self.data_centers = ['IN']  # INCOIS (India) data center
        self.cache_dir = Path("cache/ifremer")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def connect_ftp(self) -> Optional[ftplib.FTP]:
        """Establish FTP connection to IFREMER"""
        try:
            ftp = ftplib.FTP(self.ftp_host)
            ftp.login()  # Anonymous login
            ftp.cwd(self.base_path)
            logger.info(f"Connected to {self.ftp_host}{self.base_path}")
            return ftp
        except Exception as e:
            logger.error(f"Failed to connect to IFREMER FTP: {e}")
            return None
    
    def get_argo_index(self) -> Optional[pd.DataFrame]:
        """Download and parse ARGO float index"""
        try:
            ftp = self.connect_ftp()
            if not ftp:
                return None
            
            # Download ar_index_global_prof.txt
            index_file = "ar_index_global_prof.txt.gz"
            local_path = self.cache_dir / index_file
            
            logger.info("Downloading ARGO index file...")
            with open(local_path, 'wb') as f:
                ftp.retrbinary(f'RETR {index_file}', f.write)
            
            ftp.quit()
            
            # Read compressed file
            logger.info("Parsing ARGO index...")
            with gzip.open(local_path, 'rt') as f:
                # Skip header lines
                lines = f.readlines()
                header_line = None
                data_start = 0
                
                for i, line in enumerate(lines):
                    if line.startswith('#'):
                        continue
                    if 'file' in line.lower() and 'date' in line.lower():
                        header_line = line.strip()
                        data_start = i + 1
                        break
                
                if header_line:
                    # Parse header
                    columns = header_line.split(',')
                    # Read data
                    df = pd.read_csv(local_path, compression='gzip', 
                                   skiprows=data_start, names=columns, 
                                   skipinitialspace=True)
                else:
                    # Fallback parsing
                    df = pd.read_csv(local_path, compression='gzip', 
                                   comment='#', skipinitialspace=True)
            
            logger.info(f"Loaded {len(df)} ARGO profiles from index")
            return df
            
        except Exception as e:
            logger.error(f"Failed to get ARGO index: {e}")
            return None
    
    def filter_indian_ocean_profiles(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter profiles for Indian Ocean region"""
        try:
            # Standardize column names
            lat_col = None
            lon_col = None
            for col in df.columns:
                col_lower = col.lower().strip()
                if 'latitude' in col_lower or col_lower == 'lat':
                    lat_col = col
                elif 'longitude' in col_lower or col_lower == 'lon':
                    lon_col = col
            
            if not lat_col or not lon_col:
                logger.error("Could not find latitude/longitude columns")
                return pd.DataFrame()
            
            # Convert to numeric
            df[lat_col] = pd.to_numeric(df[lat_col], errors='coerce')
            df[lon_col] = pd.to_numeric(df[lon_col], errors='coerce')
            
            # Filter for Indian Ocean
            mask = (
                (df[lat_col] >= self.indian_ocean_bounds['lat_min']) &
                (df[lat_col] <= self.indian_ocean_bounds['lat_max']) &
                (df[lon_col] >= self.indian_ocean_bounds['lon_min']) &
                (df[lon_col] <= self.indian_ocean_bounds['lon_max'])
            )
            
            indian_df = df[mask].copy()
            
            # Prefer INCOIS (India) data center if available
            if 'data_centre' in df.columns:
                incois_mask = indian_df['data_centre'].str.contains('IN', na=False)
                if incois_mask.any():
                    logger.info("Found INCOIS (Indian) data center profiles")
                    return indian_df[incois_mask]
            
            logger.info(f"Filtered to {len(indian_df)} Indian Ocean profiles")
            return indian_df
            
        except Exception as e:
            logger.error(f"Error filtering Indian Ocean profiles: {e}")
            return pd.DataFrame()
    
    def download_profile_file(self, profile_path: str) -> Optional[str]:
        """Download individual ARGO profile NetCDF file"""
        try:
            ftp = self.connect_ftp()
            if not ftp:
                return None
            
            # Create local filename
            local_filename = profile_path.replace('/', '_')
            local_path = self.cache_dir / local_filename
            
            # Download file
            logger.info(f"Downloading {profile_path}")
            with open(local_path, 'wb') as f:
                ftp.retrbinary(f'RETR {profile_path}', f.write)
            
            ftp.quit()
            return str(local_path)
            
        except Exception as e:
            logger.error(f"Failed to download {profile_path}: {e}")
            return None
    
    def parse_netcdf_profile(self, file_path: str) -> Dict[str, Any]:
        """Parse NetCDF ARGO profile file"""
        try:
            with nc.Dataset(file_path, 'r') as dataset:
                profile = {}
                
                # Basic metadata
                profile['platform_number'] = getattr(dataset, 'platform_number', '').strip()
                profile['project_name'] = getattr(dataset, 'project_name', '').strip()
                profile['pi_name'] = getattr(dataset, 'pi_name', '').strip()
                profile['data_centre'] = getattr(dataset, 'data_centre', '').strip()
                
                # Platform type and WMO
                if 'PLATFORM_TYPE' in dataset.variables:
                    profile['platform_type'] = ''.join([s.decode() for s in dataset.variables['PLATFORM_TYPE'][:].data]).strip()
                
                # Position and time
                if 'LATITUDE' in dataset.variables:
                    profile['latitude'] = float(dataset.variables['LATITUDE'][:].data[0])
                if 'LONGITUDE' in dataset.variables:
                    profile['longitude'] = float(dataset.variables['LONGITUDE'][:].data[0])
                
                # Reference date (days since 1950-01-01)
                if 'JULD' in dataset.variables:
                    juld = float(dataset.variables['JULD'][:].data[0])
                    if not np.isnan(juld):
                        ref_date = datetime(1950, 1, 1)
                        profile['date'] = ref_date + timedelta(days=juld)
                
                # Cycle number
                if 'CYCLE_NUMBER' in dataset.variables:
                    profile['cycle_number'] = int(dataset.variables['CYCLE_NUMBER'][:].data[0])
                
                # Temperature, Salinity, Pressure data
                measurements = []
                n_levels = dataset.dimensions['N_LEVELS'].size
                
                for level in range(n_levels):
                    measurement = {}
                    
                    # Pressure
                    if 'PRES' in dataset.variables:
                        pres = dataset.variables['PRES'][:].data[0, level]
                        if not np.isnan(pres):
                            measurement['pressure'] = float(pres)
                    
                    # Temperature
                    if 'TEMP' in dataset.variables:
                        temp = dataset.variables['TEMP'][:].data[0, level]
                        if not np.isnan(temp):
                            measurement['temperature'] = float(temp)
                    
                    # Salinity
                    if 'PSAL' in dataset.variables:
                        sal = dataset.variables['PSAL'][:].data[0, level]
                        if not np.isnan(sal):
                            measurement['salinity'] = float(sal)
                    
                    if measurement:  # Only add if has data
                        measurements.append(measurement)
                
                profile['measurements'] = measurements
                
                logger.info(f"Parsed profile: {profile['platform_number']} with {len(measurements)} measurements")
                return profile
                
        except Exception as e:
            logger.error(f"Failed to parse NetCDF file {file_path}: {e}")
            return {}
    
    def fetch_indian_argo_data(self, max_profiles: int = 50) -> List[Dict[str, Any]]:
        """Fetch Indian Ocean ARGO data from IFREMER"""
        logger.info("🇮🇳 Fetching Indian ARGO data from IFREMER...")
        
        # Get ARGO index
        index_df = self.get_argo_index()
        if index_df is None or index_df.empty:
            logger.error("Failed to get ARGO index")
            return []
        
        # Filter for Indian Ocean
        indian_profiles_df = self.filter_indian_ocean_profiles(index_df)
        if indian_profiles_df.empty:
            logger.warning("No Indian Ocean profiles found")
            return []
        
        # Sort by date (most recent first) and limit
        if 'date' in indian_profiles_df.columns:
            indian_profiles_df = indian_profiles_df.sort_values('date', ascending=False)
        
        limited_df = indian_profiles_df.head(max_profiles)
        
        profiles = []
        for _, row in limited_df.iterrows():
            try:
                # Get file path from index
                file_path = row.get('file', '')
                if not file_path:
                    continue
                
                # Download profile file
                local_file = self.download_profile_file(file_path)
                if not local_file:
                    continue
                
                # Parse NetCDF
                profile = self.parse_netcdf_profile(local_file)
                if profile:
                    profiles.append(profile)
                
                # Clean up
                if os.path.exists(local_file):
                    os.remove(local_file)
                
            except Exception as e:
                logger.error(f"Error processing profile: {e}")
                continue
        
        logger.info(f"Successfully fetched {len(profiles)} Indian ARGO profiles")
        return profiles

def main():
    """Main function to test IFREMER data fetching"""
    print("🇮🇳 IFREMER ARGO Data Fetcher for Indian Ocean")
    print("=" * 50)
    
    fetcher = IfremerArgoFetcher()
    
    # Test fetching a few profiles
    profiles = fetcher.fetch_indian_argo_data(max_profiles=10)
    
    if profiles:
        print(f"\n✅ Successfully fetched {len(profiles)} profiles:")
        for i, profile in enumerate(profiles[:3], 1):
            platform = profile.get('platform_number', 'Unknown')
            lat = profile.get('latitude', 0.0)
            lon = profile.get('longitude', 0.0)
            measurements = len(profile.get('measurements', []))
            date = profile.get('date', 'Unknown')
            print(f"   {i}. Platform {platform} at ({lat:.2f}, {lon:.2f}) - {measurements} measurements - {date}")
    else:
        print("❌ No profiles fetched")

if __name__ == '__main__':
    main()