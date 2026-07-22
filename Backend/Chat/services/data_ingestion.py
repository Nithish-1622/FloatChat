"""
ARGO Data Ingestion Service
Handles fetching, parsing, and storing ARGO float data from multiple sources
"""
import asyncio
import aiohttp
import aiofiles
import xarray as xr
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import logging
from urllib.parse import urljoin, urlparse
import re
import json

from config import (
    ARGO_DATA_SOURCES, 
    DATA_PROCESSING_CONFIG, 
    GEOGRAPHICAL_REGIONS,
    SCHEDULER_CONFIG,
    DATA_DIR,
    CACHE_DIR
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArgoDataIngestion:
    """Main class for ARGO data ingestion and processing"""
    
    def __init__(self):
        self.session = None
        self.data_sources = ARGO_DATA_SOURCES
        self.core_vars = DATA_PROCESSING_CONFIG["core_variables"]
        self.bgc_vars = DATA_PROCESSING_CONFIG["bgc_variables"]
        self.qc_flags = DATA_PROCESSING_CONFIG["qc_flags"]
        
        # Create data directories
        self.netcdf_dir = DATA_DIR / "netcdf"
        self.parquet_dir = DATA_DIR / "parquet"
        self.netcdf_dir.mkdir(parents=True, exist_ok=True)
        self.parquet_dir.mkdir(parents=True, exist_ok=True)
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=SCHEDULER_CONFIG["timeout_seconds"])
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    async def fetch_argo_catalog_urls(self, source_config: Dict[str, Any]) -> List[str]:
        """
        Fetch catalog URLs from different ARGO data sources
        """
        urls = []
        base_url = source_config["base_url"]
        source_type = source_config["type"]
        
        try:
            if source_type == "direct_download":
                urls.extend(await self._fetch_direct_download_urls(base_url))
            elif source_type == "opendap":
                urls.extend(await self._fetch_opendap_urls(base_url))
            elif source_type == "api":
                urls.extend(await self._fetch_api_urls(base_url))
                
        except Exception as e:
            logger.error(f"Error fetching URLs from {base_url}: {str(e)}")
            
        return urls
    
    async def _fetch_direct_download_urls(self, base_url: str) -> List[str]:
        """Fetch NetCDF file URLs from direct download sources"""
        urls = []
        
        if "nodc.noaa.gov" in base_url:
            # NOAA ARGO data structure
            urls.extend(await self._parse_noaa_argo_catalog(base_url))
        elif "ncei.noaa.gov" in base_url:
            # NCEI data structure
            urls.extend(await self._parse_ncei_catalog(base_url))
        elif "ucsd.edu" in base_url:
            # UCSD ARGO data structure
            urls.extend(await self._parse_ucsd_catalog(base_url))
            
        return urls
    
    async def _fetch_opendap_urls(self, base_url: str) -> List[str]:
        """Fetch OPeNDAP dataset URLs"""
        urls = []
        
        if "ifremer.fr" in base_url:
            urls.extend(await self._parse_ifremer_thredds(base_url))
        elif "incois.gov.in" in base_url and "las" in base_url:
            urls.extend(await self._parse_incois_las(base_url))
            
        return urls
    
    async def _fetch_api_urls(self, base_url: str) -> List[str]:
        """Fetch URLs from API endpoints"""
        urls = []
        
        if "incois.gov.in" in base_url and "argo" in base_url:
            urls.extend(await self._parse_incois_api(base_url))
        elif "data.gov.in" in base_url:
            urls.extend(await self._parse_data_gov_in(base_url))
        elif "ocean-ops.org" in base_url:
            urls.extend(await self._parse_ocean_ops_api(base_url))
        elif "biogeochemical-argo.com" in base_url:
            urls.extend(await self._parse_bgc_argo_api(base_url))
            
        return urls
    
    async def _parse_noaa_argo_catalog(self, base_url: str) -> List[str]:
        """Parse NOAA ARGO catalog for NetCDF files"""
        urls = []
        
        try:
            # NOAA typically has year/month directory structure
            current_date = datetime.now()
            for months_back in range(6):  # Get last 6 months
                target_date = current_date - timedelta(days=30 * months_back)
                year = target_date.year
                month = target_date.month
                
                catalog_url = f"{base_url}/data/{year}/{month:02d}/"
                
                async with self.session.get(catalog_url) as response:
                    if response.status == 200:
                        html = await response.text()
                        # Extract .nc file links
                        nc_pattern = r'href="([^"]*\.nc)"'
                        matches = re.findall(nc_pattern, html)
                        
                        for match in matches:
                            if not match.startswith('http'):
                                file_url = urljoin(catalog_url, match)
                            else:
                                file_url = match
                            urls.append(file_url)
                            
        except Exception as e:
            logger.error(f"Error parsing NOAA catalog: {str(e)}")
            
        return urls
    
    async def _parse_ncei_catalog(self, base_url: str) -> List[str]:
        """Parse NCEI ARGO catalog"""
        urls = []
        
        try:
            # NCEI has float-based directory structure
            async with self.session.get(base_url) as response:
                if response.status == 200:
                    html = await response.text()
                    # Look for float directories (numeric)
                    float_pattern = r'href="(\d+)/"'
                    float_dirs = re.findall(float_pattern, html)
                    
                    # Limit to first 50 floats to avoid overwhelming
                    for float_dir in float_dirs[:50]:
                        float_url = urljoin(base_url, f"{float_dir}/")
                        float_files = await self._get_float_netcdf_files(float_url)
                        urls.extend(float_files)
                        
        except Exception as e:
            logger.error(f"Error parsing NCEI catalog: {str(e)}")
            
        return urls
    
    async def _parse_ucsd_catalog(self, base_url: str) -> List[str]:
        """Parse UCSD ARGO catalog"""
        urls = []
        
        try:
            # UCSD has various data products
            products = ['argo_profiles', 'bgc_profiles', 'temperature_salinity']
            
            for product in products:
                product_url = urljoin(base_url, f"{product}/")
                
                async with self.session.get(product_url) as response:
                    if response.status == 200:
                        html = await response.text()
                        nc_pattern = r'href="([^"]*\.nc)"'
                        matches = re.findall(nc_pattern, html)
                        
                        for match in matches[:100]:  # Limit files
                            if not match.startswith('http'):
                                file_url = urljoin(product_url, match)
                            else:
                                file_url = match
                            urls.append(file_url)
                            
        except Exception as e:
            logger.error(f"Error parsing UCSD catalog: {str(e)}")
            
        return urls
    
    async def _parse_ifremer_thredds(self, base_url: str) -> List[str]:
        """Parse IFREMER THREDDS catalog"""
        urls = []
        
        try:
            # Convert HTML catalog to XML
            xml_url = base_url.replace('catalog.html', 'catalog.xml')
            
            async with self.session.get(xml_url) as response:
                if response.status == 200:
                    xml_content = await response.text()
                    
                    # Parse XML for dataset URLs
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(xml_content)
                    
                    # Find dataset elements
                    for dataset in root.iter():
                        if 'urlPath' in dataset.attrib:
                            url_path = dataset.attrib['urlPath']
                            opendap_url = base_url.replace('/catalog.html', f'/dodsC/{url_path}')
                            urls.append(opendap_url)
                            
        except Exception as e:
            logger.error(f"Error parsing IFREMER THREDDS: {str(e)}")
            
        return urls[:200]  # Limit to avoid overwhelming
    
    async def _parse_incois_las(self, base_url: str) -> List[str]:
        """Parse INCOIS LAS catalog"""
        urls = []
        
        try:
            # INCOIS LAS has specific dataset IDs
            api_url = base_url.replace('/UI.vm', '/productserver/dataset')
            
            async with self.session.get(api_url) as response:
                if response.status == 200:
                    datasets = await response.json()
                    
                    for dataset in datasets.get('datasets', []):
                        if 'argo' in dataset.get('name', '').lower():
                            dataset_id = dataset.get('id')
                            opendap_url = f"{api_url}/{dataset_id}/dodsC"
                            urls.append(opendap_url)
                            
        except Exception as e:
            logger.error(f"Error parsing INCOIS LAS: {str(e)}")
            
        return urls
    
    async def _parse_incois_api(self, base_url: str) -> List[str]:
        """Parse INCOIS ARGO API"""
        urls = []
        
        try:
            # INCOIS API for float data
            api_endpoint = urljoin(base_url, 'api/floats')
            
            async with self.session.get(api_endpoint) as response:
                if response.status == 200:
                    float_data = await response.json()
                    
                    for float_info in float_data.get('floats', []):
                        float_id = float_info.get('platform_id')
                        data_url = urljoin(base_url, f'data/{float_id}.nc')
                        urls.append(data_url)
                        
        except Exception as e:
            logger.error(f"Error parsing INCOIS API: {str(e)}")
            
        return urls
    
    async def _parse_data_gov_in(self, base_url: str) -> List[str]:
        """Parse Data.gov.in ARGO resources"""
        urls = []
        
        try:
            # Data.gov.in resource API
            resource_api = base_url.replace('/resource/', '/api/action/resource_show?id=')
            
            async with self.session.get(resource_api) as response:
                if response.status == 200:
                    resource_data = await response.json()
                    
                    result = resource_data.get('result', {})
                    resource_url = result.get('url')
                    
                    if resource_url and resource_url.endswith('.nc'):
                        urls.append(resource_url)
                        
        except Exception as e:
            logger.error(f"Error parsing Data.gov.in: {str(e)}")
            
        return urls
    
    async def _parse_ocean_ops_api(self, base_url: str) -> List[str]:
        """Parse Ocean-OPS API"""
        urls = []
        
        try:
            # Ocean-OPS API endpoint
            api_url = 'https://www.ocean-ops.org/api/1/data/platform'
            params = {
                'type': 'ARGO',
                'status': 'OPERATIONAL',
                'limit': 100
            }
            
            async with self.session.get(api_url, params=params) as response:
                if response.status == 200:
                    platform_data = await response.json()
                    
                    for platform in platform_data.get('data', []):
                        platform_id = platform.get('ref')
                        # Construct data URL (this is an example format)
                        data_url = f"https://data.ocean-ops.org/argo/{platform_id}.nc"
                        urls.append(data_url)
                        
        except Exception as e:
            logger.error(f"Error parsing Ocean-OPS API: {str(e)}")
            
        return urls
    
    async def _parse_bgc_argo_api(self, base_url: str) -> List[str]:
        """Parse BGC-ARGO API"""
        urls = []
        
        try:
            # BGC-ARGO API for biogeochemical data
            api_url = urljoin(base_url, 'api/floats')
            params = {
                'active': 'true',
                'bgc': 'true',
                'limit': 50
            }
            
            async with self.session.get(api_url, params=params) as response:
                if response.status == 200:
                    bgc_data = await response.json()
                    
                    for float_info in bgc_data.get('floats', []):
                        float_id = float_info.get('wmo')
                        data_url = urljoin(base_url, f'data/{float_id}_Sprof.nc')
                        urls.append(data_url)
                        
        except Exception as e:
            logger.error(f"Error parsing BGC-ARGO API: {str(e)}")
            
        return urls
    
    async def _get_float_netcdf_files(self, float_url: str) -> List[str]:
        """Get NetCDF files for a specific float"""
        urls = []
        
        try:
            async with self.session.get(float_url) as response:
                if response.status == 200:
                    html = await response.text()
                    nc_pattern = r'href="([^"]*\.nc)"'
                    matches = re.findall(nc_pattern, html)
                    
                    for match in matches:
                        if not match.startswith('http'):
                            file_url = urljoin(float_url, match)
                        else:
                            file_url = match
                        urls.append(file_url)
                        
        except Exception as e:
            logger.error(f"Error getting float files from {float_url}: {str(e)}")
            
        return urls
    
    async def download_netcdf_file(self, url: str, max_retries: int = 3) -> Optional[str]:
        """
        Download a NetCDF file and return the local path
        """
        filename = Path(urlparse(url).path).name
        if not filename.endswith('.nc'):
            filename += '.nc'
        
        local_path = self.netcdf_dir / filename
        
        # Skip if already exists
        if local_path.exists():
            logger.info(f"File already exists: {filename}")
            return str(local_path)
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Downloading {filename} (attempt {attempt + 1}/{max_retries})")
                
                async with self.session.get(url) as response:
                    if response.status == 200:
                        async with aiofiles.open(local_path, 'wb') as f:
                            async for chunk in response.content.iter_chunked(8192):
                                await f.write(chunk)
                        
                        logger.info(f"Successfully downloaded: {filename}")
                        return str(local_path)
                    else:
                        logger.warning(f"HTTP {response.status} for {url}")
                        
            except Exception as e:
                logger.error(f"Download attempt {attempt + 1} failed for {url}: {str(e)}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    
        return None
    
    def parse_netcdf_to_profiles(self, netcdf_path: str) -> List[Dict[str, Any]]:
        """
        Parse NetCDF file and extract ARGO profiles
        """
        profiles = []
        
        try:
            # Open NetCDF file with xarray
            ds = xr.open_dataset(netcdf_path)
            
            # Get number of profiles
            n_prof = ds.dims.get('N_PROF', 0)
            
            for prof_idx in range(n_prof):
                try:
                    profile_data = self._extract_profile_data(ds, prof_idx)
                    if profile_data:
                        profiles.append(profile_data)
                except Exception as e:
                    logger.warning(f"Error processing profile {prof_idx} in {netcdf_path}: {str(e)}")
                    continue
            
            ds.close()
            
        except Exception as e:
            logger.error(f"Error parsing NetCDF file {netcdf_path}: {str(e)}")
            
        return profiles
    
    def _extract_profile_data(self, ds: xr.Dataset, prof_idx: int) -> Optional[Dict[str, Any]]:
        """
        Extract data for a single profile
        """
        try:
            # Basic profile info
            profile_data = {
                'platform_id': self._get_string_variable(ds, 'PLATFORM_NUMBER', prof_idx),
                'cycle_number': int(ds.CYCLE_NUMBER.isel(N_PROF=prof_idx).values),
                'latitude': float(ds.LATITUDE.isel(N_PROF=prof_idx).values),
                'longitude': float(ds.LONGITUDE.isel(N_PROF=prof_idx).values),
                'timestamp': pd.to_datetime(ds.JULD.isel(N_PROF=prof_idx).values).to_pydatetime()
            }
            
            # Generate profile ID
            profile_data['profile_id'] = f"{profile_data['platform_id']}_{profile_data['cycle_number']}"
            
            # Extract measurement data
            n_levels = ds.dims.get('N_LEVELS', 0)
            
            # Core variables
            for var_name in self.core_vars:
                if var_name in ['latitude', 'longitude', 'time', 'profile_id', 'platform_id']:
                    continue  # Already extracted
                
                data, qc_data = self._extract_variable_data(ds, var_name.upper(), prof_idx, n_levels)
                if data is not None:
                    profile_data[var_name.lower()] = data
                    profile_data[f"{var_name.lower()}_qc"] = qc_data
            
            # BGC variables (if present)
            for var_name in self.bgc_vars:
                if var_name.upper() in ds.variables:
                    data, qc_data = self._extract_variable_data(ds, var_name.upper(), prof_idx, n_levels)
                    if data is not None:
                        profile_data[var_name.lower()] = data
                        profile_data[f"{var_name.lower()}_qc"] = qc_data
            
            # Metadata
            profile_data['data_mode'] = self._get_string_variable(ds, 'DATA_MODE', prof_idx, default='R')
            profile_data['data_centre'] = self._get_string_variable(ds, 'DATA_CENTRE', prof_idx)
            
            return profile_data
            
        except Exception as e:
            logger.error(f"Error extracting profile data: {str(e)}")
            return None
    
    def _get_string_variable(self, ds: xr.Dataset, var_name: str, prof_idx: int, default: str = "") -> str:
        """Extract string variable from dataset"""
        try:
            if var_name in ds.variables:
                value = ds[var_name].isel(N_PROF=prof_idx).values
                if isinstance(value, bytes):
                    return value.decode('utf-8').strip()
                elif isinstance(value, np.ndarray):
                    return ''.join([chr(x) for x in value if x != 0]).strip()
                else:
                    return str(value).strip()
        except Exception as e:
            logger.warning(f"Error extracting {var_name}: {str(e)}")
        
        return default
    
    def _extract_variable_data(self, ds: xr.Dataset, var_name: str, prof_idx: int, n_levels: int) -> Tuple[Optional[List[float]], Optional[List[int]]]:
        """Extract variable data and QC flags"""
        try:
            if var_name not in ds.variables:
                return None, None
            
            # Get data
            data = ds[var_name].isel(N_PROF=prof_idx).values
            
            # Convert to list and filter out fill values
            data_list = []
            qc_list = []
            
            # Get QC data if available
            qc_var_name = f"{var_name}_QC"
            has_qc = qc_var_name in ds.variables
            
            if has_qc:
                qc_data = ds[qc_var_name].isel(N_PROF=prof_idx).values
            
            for i in range(min(len(data), n_levels)):
                value = data[i]
                
                # Skip fill values (typically very large negative numbers)
                if not np.isnan(value) and abs(value) < 1e10:
                    data_list.append(float(value))
                    
                    if has_qc:
                        qc_flag = int(qc_data[i]) if i < len(qc_data) else 9
                        qc_list.append(qc_flag)
                    else:
                        qc_list.append(1)  # Assume good if no QC
            
            return data_list if data_list else None, qc_list if qc_list else None
            
        except Exception as e:
            logger.warning(f"Error extracting {var_name}: {str(e)}")
            return None, None
    
    def filter_profiles_by_qc(self, profiles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter profiles based on QC flags
        """
        filtered_profiles = []
        good_flags = self.qc_flags["good"]
        
        for profile in profiles:
            # Check if core variables have good QC
            has_good_temp = self._has_good_qc(profile.get('temperature_qc', []), good_flags)
            has_good_sal = self._has_good_qc(profile.get('salinity_qc', []), good_flags)
            has_good_pres = self._has_good_qc(profile.get('pressure_qc', []), good_flags)
            
            # Keep profile if at least temperature and pressure are good
            if has_good_temp and has_good_pres:
                filtered_profiles.append(profile)
        
        return filtered_profiles
    
    def _has_good_qc(self, qc_flags: List[int], good_flags: List[int]) -> bool:
        """Check if at least 50% of measurements have good QC"""
        if not qc_flags:
            return False
        
        good_count = sum(1 for flag in qc_flags if flag in good_flags)
        return good_count / len(qc_flags) >= 0.5
    
    def assign_geographical_region(self, latitude: float, longitude: float) -> str:
        """Assign geographical region for data partitioning"""
        for region_name, bounds in GEOGRAPHICAL_REGIONS.items():
            if (bounds["lat_min"] <= latitude <= bounds["lat_max"] and
                bounds["lon_min"] <= longitude <= bounds["lon_max"]):
                return region_name
        
        return "other"

    async def run_ingestion_cycle(self, max_files_per_source: int = 10):
        """
        Run a complete data ingestion cycle
        """
        logger.info("Starting ARGO data ingestion cycle")
        
        total_downloaded = 0
        total_processed = 0
        
        # Sort sources by priority
        sorted_sources = sorted(
            self.data_sources.items(), 
            key=lambda x: x[1]["priority"]
        )
        
        for source_name, source_config in sorted_sources:
            logger.info(f"Processing source: {source_name}")
            
            try:
                # Get catalog URLs
                urls = await self.fetch_argo_catalog_urls(source_config)
                logger.info(f"Found {len(urls)} URLs from {source_name}")
                
                # Limit files per source
                urls = urls[:max_files_per_source]
                
                # Download and process files
                for url in urls:
                    try:
                        # Download file
                        local_path = await self.download_netcdf_file(url)
                        if local_path:
                            total_downloaded += 1
                            
                            # Parse profiles
                            profiles = self.parse_netcdf_to_profiles(local_path)
                            filtered_profiles = self.filter_profiles_by_qc(profiles)
                            
                            logger.info(f"Extracted {len(filtered_profiles)} good profiles from {Path(local_path).name}")
                            total_processed += len(filtered_profiles)
                            
                            # TODO: Store profiles in database and parquet
                            # This would be implemented in the next phase
                            
                    except Exception as e:
                        logger.error(f"Error processing {url}: {str(e)}")
                        continue
                
            except Exception as e:
                logger.error(f"Error processing source {source_name}: {str(e)}")
                continue
        
        logger.info(f"Ingestion cycle complete. Downloaded: {total_downloaded}, Processed: {total_processed}")
        return {"downloaded": total_downloaded, "processed": total_processed}

# Usage example
async def main():
    """Example usage of the ingestion system"""
    async with ArgoDataIngestion() as ingestion:
        results = await ingestion.run_ingestion_cycle(max_files_per_source=5)
        print(f"Ingestion results: {results}")

if __name__ == "__main__":
    asyncio.run(main())