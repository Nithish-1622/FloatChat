"""
Supabase ARGO Data Storage and Preprocessing Service
Handles storing ARGO profiles in Supabase and Parquet files
"""
import asyncio
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import logging
import json
import uuid

# Supabase imports
try:
    from supabase_models import argo_floats_db, argo_profiles_db
    from supabase_config import get_supabase_client
    SUPABASE_AVAILABLE = True
except ImportError:
    # Fallback for development without Supabase
    argo_floats_db = None
    argo_profiles_db = None
    get_supabase_client = None
    SUPABASE_AVAILABLE = False

# Arrow/Parquet imports
try:
    import pyarrow as pa
    import pyarrow.parquet as pq
    PARQUET_AVAILABLE = True
except ImportError:
    # Fallback for development
    pa = None
    pq = None
    PARQUET_AVAILABLE = False

from config import (
    DATA_PROCESSING_CONFIG,
    GEOGRAPHICAL_REGIONS,
    DATA_DIR
)

from models.schemas import ArgoProfile, ArgoFloat

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseDataStorageService:
    """
    Supabase-based ARGO data storage and preprocessing service
    """
    
    def __init__(self):
        """Initialize the Supabase data storage service"""
        self.data_dir = Path(DATA_DIR)
        self.cache_dir = self.data_dir / "cache"
        self.parquet_dir = self.data_dir / "parquet"
        
        # Ensure directories exist
        self.data_dir.mkdir(exist_ok=True)
        self.cache_dir.mkdir(exist_ok=True)
        self.parquet_dir.mkdir(exist_ok=True)
        
        # Initialize Supabase client
        self.supabase_client = None
        supabase_available = SUPABASE_AVAILABLE
        
        if supabase_available:
            try:
                # Use admin client (service role) for full database access
                self.supabase_client = get_supabase_client(admin=True)
                if self.supabase_client:
                    logger.info("Supabase client initialized successfully")
                else:
                    logger.warning("Supabase client initialization failed")
                    supabase_available = False
            except Exception as e:
                logger.error(f"Error initializing Supabase client: {str(e)}")
                supabase_available = False
        
        self.is_available = supabase_available
        logger.info(f"SupabaseDataStorageService initialized - Available: {self.is_available}")
    
    async def store_argo_profiles(self, profiles: List[Dict[str, Any]], source_name: str) -> Dict[str, Any]:
        """
        Store ARGO profiles in Supabase database with comprehensive preprocessing
        
        Args:
            profiles: List of profile dictionaries with full measurements
            source_name: Name of the data source
            
        Returns:
            Dictionary with detailed storage results
        """
        if not self.is_available:
            return await self._store_profiles_fallback(profiles, source_name)
        
        try:
            results = {
                "total_profiles": len(profiles),
                "stored_profiles": 0,
                "updated_profiles": 0,
                "failed_profiles": 0,
                "stored_floats": 0,
                "processed_measurements": 0,
                "qc_failed_profiles": 0,
                "errors": []
            }
            
            # Group profiles by platform/float for batch processing
            float_groups = {}
            for profile in profiles:
                platform_id = profile.get('platform_number', profile.get('float_id', 'unknown'))
                if platform_id not in float_groups:
                    float_groups[platform_id] = []
                float_groups[platform_id].append(profile)
            
            # Process each float with comprehensive data processing
            for platform_id, float_profiles in float_groups.items():
                try:
                    # Preprocess profiles for quality control
                    processed_profiles = self._preprocess_profiles(float_profiles)
                    
                    # Store/update float metadata
                    float_result = await self._store_float_metadata(platform_id, processed_profiles, source_name)
                    if float_result["success"]:
                        results["stored_floats"] += 1
                    
                    # Store individual profiles with full measurements
                    for profile in processed_profiles:
                        # Apply quality control filters
                        if not self._passes_quality_control(profile):
                            results["qc_failed_profiles"] += 1
                            continue
                        
                        # Store profile with measurements
                        profile_result = await self._store_profile_with_measurements(profile, source_name)
                        if profile_result["success"]:
                            if "created" in profile_result.get("message", ""):
                                results["stored_profiles"] += 1
                            else:
                                results["updated_profiles"] += 1
                            
                            # Count processed measurements
                            measurements = profile.get("measurements", [])
                            results["processed_measurements"] += len(measurements)
                        else:
                            results["failed_profiles"] += 1
                            results["errors"].append(f"Profile {profile.get('profile_id', 'unknown')}: {profile_result.get('error', 'Unknown error')}")
                
                except Exception as e:
                    logger.error(f"Error processing float {platform_id}: {str(e)}")
                    results["failed_profiles"] += len(float_profiles)
                    results["errors"].append(f"Float {platform_id}: {str(e)}")
            
            # Store as Parquet for backup and analytics
            if PARQUET_AVAILABLE:
                await self._store_profiles_parquet(profiles, source_name)
            
            # Create summary statistics
            success_rate = (results["stored_profiles"] + results["updated_profiles"]) / max(results["total_profiles"], 1) * 100
            
            logger.info(f"Storage completed: {results['stored_profiles']} stored, {results['updated_profiles']} updated, "
                       f"{results['failed_profiles']} failed, {results['qc_failed_profiles']} QC failed, "
                       f"{results['processed_measurements']} measurements processed (Success rate: {success_rate:.1f}%)")
            
            return {
                "success": True,
                "results": results,
                "statistics": {
                    "success_rate": success_rate,
                    "qc_pass_rate": (results["total_profiles"] - results["qc_failed_profiles"]) / max(results["total_profiles"], 1) * 100,
                    "avg_measurements_per_profile": results["processed_measurements"] / max(results["stored_profiles"] + results["updated_profiles"], 1)
                },
                "message": f"Processed {results['total_profiles']} profiles from {source_name}"
            }
            
        except Exception as e:
            logger.error(f"Error storing ARGO profiles: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to store ARGO profiles"
            }
    
    def _preprocess_profiles(self, profiles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Comprehensive preprocessing of ARGO profiles
        """
        processed_profiles = []
        
        for profile in profiles:
            try:
                # Extract and validate coordinates
                latitude = self._validate_coordinate(profile.get('latitude', 0), 'latitude')
                longitude = self._validate_coordinate(profile.get('longitude', 0), 'longitude')
                
                # Validate and parse datetime
                date_time = self._parse_datetime(profile.get('date_time', profile.get('juld')))
                
                # Extract measurement arrays
                measurements = self._extract_comprehensive_measurements(profile)
                
                # Calculate derived parameters
                derived_params = self._calculate_derived_parameters(measurements, latitude, longitude)
                
                # Apply quality control to measurements
                qc_results = self._apply_quality_control(measurements, profile)
                
                # Build processed profile
                processed_profile = {
                    **profile,  # Keep original data
                    "latitude": latitude,
                    "longitude": longitude,
                    "date_time": date_time,
                    "measurements": measurements,
                    "derived_parameters": derived_params,
                    "qc_summary": qc_results,
                    "processing_metadata": {
                        "processed_at": datetime.utcnow().isoformat(),
                        "processor_version": "FloatChat_v2.0_comprehensive",
                        "preprocessing_flags": self._get_preprocessing_flags(profile, measurements)
                    }
                }
                
                processed_profiles.append(processed_profile)
                
            except Exception as e:
                logger.error(f"Error preprocessing profile {profile.get('profile_id', 'unknown')}: {str(e)}")
                # Include original profile with error flag
                profile["preprocessing_error"] = str(e)
                processed_profiles.append(profile)
        
        return processed_profiles
    
    def _extract_comprehensive_measurements(self, profile: Dict[str, Any]) -> List[Dict]:
        """
        Extract all measurement data with comprehensive parameter support
        """
        measurements = []
        
        # Core ARGO parameters
        core_params = {
            'pres': 'pressure',
            'temp': 'temperature', 
            'psal': 'salinity'
        }
        
        # BGC parameters
        bgc_params = {
            'doxy': 'dissolved_oxygen',
            'chla': 'chlorophyll_a',
            'bbp700': 'backscatter_700nm',
            'ph_in_situ_total': 'ph_total',
            'nitrate': 'nitrate',
            'cdom': 'colored_dissolved_organic_matter',
            'downwelling_par': 'photosynthetically_active_radiation'
        }
        
        # Deep float parameters
        deep_params = {
            'cndc': 'conductivity',
            'fluorescence_cdom': 'fluorescence_cdom',
            'beta_backscattering': 'beta_backscattering'
        }
        
        # Combine all parameters
        all_params = {**core_params, **bgc_params, **deep_params}
        
        # Extract measurements
        for param_key, param_name in all_params.items():
            if param_key in profile and profile[param_key] is not None:
                values = profile[param_key]
                
                # Ensure values is a list
                if not isinstance(values, list):
                    if isinstance(values, (int, float)):
                        values = [values]
                    else:
                        continue
                
                # Get corresponding QC flags and adjusted values
                qc_values = profile.get(f"{param_key}_qc", [1] * len(values))
                adjusted_values = profile.get(f"{param_key}_adjusted", None)
                adjusted_qc = profile.get(f"{param_key}_adjusted_qc", None)
                adjusted_error = profile.get(f"{param_key}_adjusted_error", None)
                
                # Get depth/pressure values for this measurement
                depths = profile.get('pres', list(range(len(values))))
                
                # Create measurement entries
                for i, value in enumerate(values):
                    if i < len(depths):
                        measurement = {
                            "parameter": param_name,
                            "parameter_code": param_key,
                            "depth": depths[i] if i < len(depths) else i * 10,  # Fallback depth
                            "value": float(value) if value is not None else None,
                            "qc": int(qc_values[i]) if i < len(qc_values) else 1,
                            "adjusted": float(adjusted_values[i]) if adjusted_values and i < len(adjusted_values) else None,
                            "adjusted_qc": int(adjusted_qc[i]) if adjusted_qc and i < len(adjusted_qc) else None,
                            "adjusted_error": float(adjusted_error[i]) if adjusted_error and i < len(adjusted_error) else None,
                            "measurement_index": i
                        }
                        measurements.append(measurement)
        
        # Sort measurements by depth
        measurements.sort(key=lambda x: x['depth'])
        
        return measurements
    
    def _calculate_derived_parameters(self, measurements: List[Dict], latitude: float, longitude: float) -> Dict[str, Any]:
        """
        Calculate derived oceanographic parameters
        """
        derived = {}
        
        try:
            # Group measurements by parameter
            params = {}
            for m in measurements:
                param = m['parameter']
                if param not in params:
                    params[param] = []
                params[param].append(m)
            
            # Calculate mixed layer depth (if temperature available)
            if 'temperature' in params:
                temps = [(m['depth'], m['value']) for m in params['temperature'] if m['value'] is not None]
                if len(temps) > 5:
                    mixed_layer_depth = self._calculate_mixed_layer_depth(temps)
                    derived['mixed_layer_depth'] = mixed_layer_depth
            
            # Calculate thermocline depth and strength
            if 'temperature' in params:
                temps = [(m['depth'], m['value']) for m in params['temperature'] if m['value'] is not None]
                if len(temps) > 10:
                    thermocline_info = self._calculate_thermocline_properties(temps)
                    derived.update(thermocline_info)
            
            # Calculate halocline properties
            if 'salinity' in params:
                sals = [(m['depth'], m['value']) for m in params['salinity'] if m['value'] is not None]
                if len(sals) > 10:
                    halocline_info = self._calculate_halocline_properties(sals)
                    derived.update(halocline_info)
            
            # Calculate water mass properties
            if 'temperature' in params and 'salinity' in params:
                ts_pairs = self._get_temperature_salinity_pairs(params['temperature'], params['salinity'])
                if ts_pairs:
                    water_mass_info = self._identify_water_masses(ts_pairs, latitude, longitude)
                    derived.update(water_mass_info)
            
            # Calculate oxygen saturation (if oxygen available)
            if 'dissolved_oxygen' in params and 'temperature' in params:
                o2_sat = self._calculate_oxygen_saturation(params['dissolved_oxygen'], params['temperature'])
                derived['oxygen_saturation_profile'] = o2_sat
            
            # Calculate productivity indicators (if chlorophyll available)
            if 'chlorophyll_a' in params:
                chla_values = [m['value'] for m in params['chlorophyll_a'] if m['value'] is not None and m['value'] > 0]
                if chla_values:
                    derived.update({
                        'surface_chlorophyll': min(chla_values),
                        'max_chlorophyll': max(chla_values),
                        'integrated_chlorophyll': sum(chla_values) * 10,  # Rough integration
                        'chlorophyll_max_depth': params['chlorophyll_a'][chla_values.index(max(chla_values))]['depth']
                    })
            
        except Exception as e:
            logger.error(f"Error calculating derived parameters: {str(e)}")
            derived['calculation_error'] = str(e)
        
        return derived
    
    def _calculate_mixed_layer_depth(self, temp_profile: List[Tuple[float, float]]) -> float:
        """Calculate mixed layer depth using temperature criterion"""
        if len(temp_profile) < 3:
            return None
        
        # Sort by depth
        temp_profile.sort(key=lambda x: x[0])
        
        # Use 0.2°C temperature difference criterion
        surface_temp = temp_profile[0][1]
        threshold = 0.2
        
        for depth, temp in temp_profile[1:]:
            if abs(temp - surface_temp) > threshold:
                return depth
        
        return temp_profile[-1][0]  # Return bottom depth if no MLD found
    
    def _calculate_thermocline_properties(self, temp_profile: List[Tuple[float, float]]) -> Dict[str, float]:
        """Calculate thermocline depth and strength"""
        if len(temp_profile) < 10:
            return {}
        
        temp_profile.sort(key=lambda x: x[0])
        
        # Calculate temperature gradients
        gradients = []
        for i in range(1, len(temp_profile)):
            depth_diff = temp_profile[i][0] - temp_profile[i-1][0]
            temp_diff = temp_profile[i][1] - temp_profile[i-1][1]
            if depth_diff > 0:
                gradient = temp_diff / depth_diff
                gradients.append((temp_profile[i][0], gradient))
        
        if not gradients:
            return {}
        
        # Find maximum gradient (thermocline center)
        max_gradient_idx = min(range(len(gradients)), key=lambda i: gradients[i][1])
        
        return {
            'thermocline_depth': gradients[max_gradient_idx][0],
            'thermocline_strength': abs(gradients[max_gradient_idx][1]),
            'temperature_gradient_max': gradients[max_gradient_idx][1]
        }
    
    def _calculate_halocline_properties(self, sal_profile: List[Tuple[float, float]]) -> Dict[str, float]:
        """Calculate halocline depth and strength"""
        if len(sal_profile) < 10:
            return {}
        
        sal_profile.sort(key=lambda x: x[0])
        
        # Calculate salinity gradients
        gradients = []
        for i in range(1, len(sal_profile)):
            depth_diff = sal_profile[i][0] - sal_profile[i-1][0]
            sal_diff = sal_profile[i][1] - sal_profile[i-1][1]
            if depth_diff > 0:
                gradient = sal_diff / depth_diff
                gradients.append((sal_profile[i][0], gradient))
        
        if not gradients:
            return {}
        
        # Find maximum gradient (halocline center)
        max_gradient_idx = max(range(len(gradients)), key=lambda i: abs(gradients[i][1]))
        
        return {
            'halocline_depth': gradients[max_gradient_idx][0],
            'halocline_strength': abs(gradients[max_gradient_idx][1]),
            'salinity_gradient_max': gradients[max_gradient_idx][1]
        }
    
    def _get_temperature_salinity_pairs(self, temp_measurements: List[Dict], sal_measurements: List[Dict]) -> List[Tuple[float, float, float]]:
        """Get matched temperature-salinity pairs with depth"""
        pairs = []
        
        # Create depth-indexed dictionaries
        temp_by_depth = {m['depth']: m['value'] for m in temp_measurements if m['value'] is not None}
        sal_by_depth = {m['depth']: m['value'] for m in sal_measurements if m['value'] is not None}
        
        # Find common depths
        common_depths = set(temp_by_depth.keys()) & set(sal_by_depth.keys())
        
        for depth in sorted(common_depths):
            pairs.append((depth, temp_by_depth[depth], sal_by_depth[depth]))
        
        return pairs
    
    def _identify_water_masses(self, ts_pairs: List[Tuple[float, float, float]], latitude: float, longitude: float) -> Dict[str, Any]:
        """Identify water masses based on T-S properties"""
        if not ts_pairs:
            return {}
        
        # Simple water mass classification
        water_masses = []
        
        for depth, temp, sal in ts_pairs:
            # Basic water mass identification
            if depth < 50:  # Surface water
                if temp > 20 and sal < 35:
                    mass_type = "tropical_surface"
                elif temp < 10:
                    mass_type = "polar_surface"
                else:
                    mass_type = "temperate_surface"
            elif depth < 500:  # Intermediate water
                if sal > 36 and temp > 15:
                    mass_type = "mediterranean_water"
                elif sal < 34.5:
                    mass_type = "intermediate_water"
                else:
                    mass_type = "central_water"
            else:  # Deep water
                if temp < 4 and sal < 34.8:
                    mass_type = "deep_water"
                elif temp < 2:
                    mass_type = "bottom_water"
                else:
                    mass_type = "deep_central_water"
            
            water_masses.append({
                "depth": depth,
                "temperature": temp,
                "salinity": sal,
                "water_mass_type": mass_type
            })
        
        # Summarize water masses
        mass_types = [wm["water_mass_type"] for wm in water_masses]
        unique_masses = list(set(mass_types))
        
        return {
            "water_masses_identified": unique_masses,
            "water_mass_profile": water_masses[:10],  # Limit to top 10 entries
            "dominant_water_mass": max(set(mass_types), key=mass_types.count) if mass_types else "unknown"
        }
    
    def _calculate_oxygen_saturation(self, o2_measurements: List[Dict], temp_measurements: List[Dict]) -> List[Dict]:
        """Calculate oxygen saturation percentage"""
        o2_sat = []
        
        # Create temperature lookup by depth
        temp_by_depth = {m['depth']: m['value'] for m in temp_measurements if m['value'] is not None}
        
        for o2_measure in o2_measurements:
            if o2_measure['value'] is not None:
                depth = o2_measure['depth']
                temp = temp_by_depth.get(depth)
                
                if temp is not None:
                    # Simplified oxygen saturation calculation (Garcia & Gordon, 1992)
                    # O2sat = exp(A0 + A1*T + A2*T^2 + ...) where T is scaled temperature
                    T = (temp + 273.15) / 100  # Convert to scaled temperature
                    ln_O2sat = -173.4292 + 249.6339/T + 143.3483*np.log(T) - 21.8492*T
                    O2sat = np.exp(ln_O2sat)  # μmol/kg
                    
                    # Calculate saturation percentage
                    sat_percent = (o2_measure['value'] / O2sat) * 100 if O2sat > 0 else None
                    
                    o2_sat.append({
                        "depth": depth,
                        "oxygen_measured": o2_measure['value'],
                        "oxygen_saturation": O2sat,
                        "saturation_percent": sat_percent
                    })
        
        return o2_sat
    
    def _apply_quality_control(self, measurements: List[Dict], profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply comprehensive quality control to measurements
        """
        qc_results = {
            "total_measurements": len(measurements),
            "passed_qc": 0,
            "failed_qc": 0,
            "questionable_qc": 0,
            "flags_summary": {},
            "parameter_qc": {}
        }
        
        # QC flag meanings: 1=Good, 2=Not evaluated, 3=Questionable, 4=Bad, 9=Missing
        for measurement in measurements:
            qc_flag = measurement.get('qc', 1)
            
            if qc_flag == 1:
                qc_results["passed_qc"] += 1
            elif qc_flag in [3]:
                qc_results["questionable_qc"] += 1  
            elif qc_flag in [4, 9]:
                qc_results["failed_qc"] += 1
            
            # Count flags
            flag_key = f"flag_{qc_flag}"
            qc_results["flags_summary"][flag_key] = qc_results["flags_summary"].get(flag_key, 0) + 1
            
            # Parameter-specific QC
            param = measurement['parameter']
            if param not in qc_results["parameter_qc"]:
                qc_results["parameter_qc"][param] = {"good": 0, "questionable": 0, "bad": 0}
            
            if qc_flag == 1:
                qc_results["parameter_qc"][param]["good"] += 1
            elif qc_flag == 3:
                qc_results["parameter_qc"][param]["questionable"] += 1
            else:
                qc_results["parameter_qc"][param]["bad"] += 1
        
        # Calculate QC pass rate
        qc_results["qc_pass_rate"] = qc_results["passed_qc"] / max(qc_results["total_measurements"], 1) * 100
        
        return qc_results
    
    def _passes_quality_control(self, profile: Dict[str, Any]) -> bool:
        """
        Determine if profile passes overall quality control
        """
        qc_summary = profile.get("qc_summary", {})
        
        # Minimum QC pass rate threshold
        min_pass_rate = 70  # 70% of measurements must pass QC
        
        qc_pass_rate = qc_summary.get("qc_pass_rate", 0)
        
        # Additional checks
        measurements = profile.get("measurements", [])
        if len(measurements) < 5:  # Minimum number of measurements
            return False
        
        # Check for essential parameters
        parameters = set(m['parameter'] for m in measurements)
        essential_params = {'temperature', 'salinity', 'pressure'}
        has_essential = len(essential_params & parameters) >= 2
        
        return qc_pass_rate >= min_pass_rate and has_essential
    
    def _is_recent_profile(self, profile: Dict[str, Any], cutoff_date: datetime) -> bool:
        """Check if profile is recent (after cutoff date)"""
        try:
            profile_date_str = profile.get('date') or profile.get('measurement_date')
            if not profile_date_str:
                return False
            
            # Parse the date string
            if isinstance(profile_date_str, str):
                # Try different date formats
                for fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%Y%m%d']:
                    try:
                        profile_date = datetime.strptime(profile_date_str.replace('Z', ''), fmt)
                        break
                    except ValueError:
                        continue
                else:
                    return False
            else:
                profile_date = profile_date_str
            
            return profile_date >= cutoff_date
        except Exception:
            return False
    
    def _get_preprocessing_flags(self, profile: Dict[str, Any], measurements: List[Dict]) -> Dict[str, Any]:
        """Get preprocessing flags and indicators"""
        flags = {
            "has_bgc_data": any(m['parameter'] in ['dissolved_oxygen', 'chlorophyll_a', 'ph_total'] for m in measurements),
            "profile_depth_range": max([m['depth'] for m in measurements]) - min([m['depth'] for m in measurements]) if measurements else 0,
            "measurement_count": len(measurements),
            "data_mode": profile.get("data_mode", "R"),
            "position_qc": profile.get("position_qc", 1),
            "temporal_qc": "recent" if self._is_recent_profile(profile, datetime.utcnow() - timedelta(days=30)) else "historical"
        }
        
        return flags
    
    async def _store_float_metadata(self, platform_id: str, profiles: List[Dict[str, Any]], source_name: str) -> Dict[str, Any]:
        """Store or update ARGO float metadata"""
        try:
            # Get float information from first profile
            first_profile = profiles[0]
            
            # Check if float already exists
            existing_float = await argo_floats_db.get_float(platform_id)
            
            float_data = {
                "float_id": platform_id,
                "platform_number": platform_id,
                "project_name": first_profile.get('project_name', 'Unknown'),
                "pi_name": first_profile.get('pi_name', 'Unknown'),
                "deployment_latitude": first_profile.get('deployment_latitude'),
                "deployment_longitude": first_profile.get('deployment_longitude'),
                "wmo_inst_type": first_profile.get('wmo_inst_type', ''),
                "status": "active",
                "last_update": datetime.utcnow().isoformat(),
                "metadata": {
                    "source_name": source_name,
                    "profile_count": len(profiles),
                    "data_mode": first_profile.get('data_mode', 'R'),
                    "data_centre": first_profile.get('data_centre', ''),
                    "processing_info": {
                        "last_processed": datetime.utcnow().isoformat(),
                        "processor_version": "FloatChat_v1.0"
                    }
                }
            }
            
            if existing_float["success"]:
                # Update existing float
                result = await argo_floats_db.update_float(platform_id, float_data)
            else:
                # Create new float
                result = await argo_floats_db.create_float(float_data)
            
            return result
            
        except Exception as e:
            logger.error(f"Error storing float metadata for {platform_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to store float metadata for {platform_id}"
            }
    
    async def _store_profile_with_measurements(self, profile: Dict[str, Any], source_name: str) -> Dict[str, Any]:
        """
        Store ARGO profile with full measurement data and processing results
        """
        try:
            # Generate profile ID if not present
            profile_id = profile.get('profile_id')
            if not profile_id:
                platform_id = profile.get('platform_number', profile.get('float_id', 'unknown'))
                cycle_num = profile.get('cycle_number', 0)
                profile_id = f"{platform_id}_{cycle_num}"
            
            # Prepare comprehensive profile data for Supabase
            profile_data = {
                "profile_id": profile_id,
                "float_id": profile.get('platform_number', profile.get('float_id', 'unknown')),
                "cycle_number": profile.get('cycle_number', 0),
                "date_time": profile.get('date_time'),
                "latitude": float(profile.get('latitude', 0)),
                "longitude": float(profile.get('longitude', 0)),
                "position_qc": profile.get('position_qc', 1),
                "profile_temp_qc": profile.get('profile_temp_qc', 1),
                "profile_psal_qc": profile.get('profile_psal_qc', 1),
                "profile_pres_qc": profile.get('profile_pres_qc', 1),
                "ocean_basin": self._determine_ocean_basin(
                    float(profile.get('latitude', 0)),
                    float(profile.get('longitude', 0))
                ),
                "data_mode": profile.get('data_mode', 'R'),
                "parameter_data_mode": profile.get('parameter_data_mode', 'R'),
                "vertical_sampling_scheme": profile.get('vertical_sampling_scheme', ''),
                "direction": profile.get('direction', 'A'),
                "data_centre": profile.get('data_centre', ''),
                "dc_reference": profile.get('dc_reference', ''),
                "data_state_indicator": profile.get('data_state_indicator', '2B'),
                
                # Comprehensive measurement data
                "measurements": profile.get('measurements', []),
                "derived_parameters": profile.get('derived_parameters', {}),
                "qc_flags": profile.get('qc_summary', {}),
                
                # Enhanced processing metadata
                "processing_metadata": {
                    "source_name": source_name,
                    "processed_at": datetime.utcnow().isoformat(),
                    "processor_version": "FloatChat_v2.0_comprehensive",
                    "preprocessing_flags": profile.get('processing_metadata', {}).get('preprocessing_flags', {}),
                    "measurement_count": len(profile.get('measurements', [])),
                    "qc_pass_rate": profile.get('qc_summary', {}).get('qc_pass_rate', 0),
                    "has_derived_parameters": bool(profile.get('derived_parameters')),
                    "original_keys": list(profile.keys())
                }
            }
            
            # Store in Supabase
            result = await argo_profiles_db.create_profile(profile_data)
            return result
            
        except Exception as e:
            logger.error(f"Error storing profile with measurements: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to store profile with measurements"
            }
    
    async def _store_profiles_parquet(self, profiles: List[Dict[str, Any]], source_name: str):
        """Store profiles as Parquet files for backup and fast access"""
        if not PARQUET_AVAILABLE:
            logger.warning("Parquet not available, skipping file storage")
            return
        
        try:
            # Convert to DataFrame
            df = pd.DataFrame(profiles)
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"argo_profiles_{source_name}_{timestamp}.parquet"
            filepath = self.parquet_dir / filename
            
            # Write to Parquet
            df.to_parquet(filepath, index=False, compression='snappy')
            logger.info(f"Stored {len(profiles)} profiles in Parquet file: {filepath}")
            
        except Exception as e:
            logger.error(f"Error storing Parquet file: {str(e)}")
    
    async def _store_profiles_fallback(self, profiles: List[Dict[str, Any]], source_name: str) -> Dict[str, Any]:
        """Fallback storage method when Supabase is not available"""
        try:
            # Store as JSON cache
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            cache_file = self.cache_dir / f"argo_profiles_{source_name}_{timestamp}.json"
            
            with open(cache_file, 'w') as f:
                json.dump(profiles, f, indent=2, default=str)
            
            # Also store as Parquet if available
            if PARQUET_AVAILABLE:
                await self._store_profiles_parquet(profiles, source_name)
            
            logger.info(f"Fallback storage: {len(profiles)} profiles cached to {cache_file}")
            
            return {
                "success": True,
                "results": {
                    "total_profiles": len(profiles),
                    "stored_profiles": len(profiles),
                    "method": "fallback_cache"
                },
                "message": f"Profiles cached locally (Supabase not available)"
            }
            
        except Exception as e:
            logger.error(f"Error in fallback storage: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Fallback storage failed"
            }
    
    def _parse_datetime(self, date_value) -> str:
        """Parse various datetime formats to ISO string"""
        if not date_value:
            return datetime.utcnow().isoformat()
        
        if isinstance(date_value, str):
            return date_value
        
        if isinstance(date_value, (int, float)):
            # Assume Julian day or Unix timestamp
            if date_value > 1000000:  # Unix timestamp
                return datetime.fromtimestamp(date_value).isoformat()
            else:  # Julian day
                base_date = datetime(1900, 1, 1)
                return (base_date + timedelta(days=date_value)).isoformat()
        
        return str(date_value)
    
    def _determine_ocean_basin(self, latitude: float, longitude: float) -> str:
        """
        Comprehensive ocean basin determination based on coordinates
        Enhanced with detailed regional classifications
        """
        try:
            # Normalize longitude to -180 to 180
            lon = ((longitude + 180) % 360) - 180
            lat = latitude
            
            # Arctic Ocean (>66.5°N)
            if lat > 66.5:
                return "Arctic Ocean"
            
            # Antarctic/Southern Ocean (<-60°S)
            if lat < -60:
                return "Southern Ocean"
            
            # Pacific Ocean
            if ((lon >= -180 and lon <= -70) or (lon >= 120 and lon <= 180)):
                if lat >= -60 and lat <= 66.5:
                    # Regional subdivisions
                    if lat > 20:
                        return "North Pacific" if lon > -70 else "Northeast Pacific"
                    elif lat < -20:
                        return "South Pacific"
                    else:
                        return "Equatorial Pacific"
            
            # Atlantic Ocean
            elif lon >= -70 and lon <= 20:
                if lat >= -60 and lat <= 66.5:
                    # Regional subdivisions
                    if lat > 20:
                        return "North Atlantic"
                    elif lat < -20:
                        return "South Atlantic"
                    else:
                        return "Equatorial Atlantic"
            
            # Indian Ocean
            elif lon >= 20 and lon <= 120:
                if lat >= -60 and lat <= 30:
                    # Regional subdivisions
                    if lat > 0:
                        return "North Indian Ocean"
                    else:
                        return "South Indian Ocean"
            
            # Mediterranean and other marginal seas
            if 30 <= lat <= 46 and -6 <= lon <= 36:
                return "Mediterranean Sea"
            elif 18 <= lat <= 31 and 34 <= lon <= 46:
                return "Red Sea"
            elif 24 <= lat <= 30 and 48 <= lon <= 56:
                return "Persian Gulf"
            elif lat >= 45 and ((lon >= -10 and lon <= 30) or (lon >= 120 and lon <= 150)):
                return "Baltic Sea" if lon < 30 else "Sea of Okhotsk"
            
            # Default classification
            return "Unknown Ocean Basin"
            
        except Exception as e:
            logger.warning(f"Error determining ocean basin: {e}")
            return "Unknown Ocean Basin"
    
    def _parse_datetime(self, dt_value) -> str:
        """Enhanced datetime parsing for various ARGO formats"""
        try:
            if dt_value is None:
                return datetime.utcnow().isoformat()
            
            if isinstance(dt_value, str):
                # Try multiple datetime formats
                formats = [
                    "%Y-%m-%dT%H:%M:%S",
                    "%Y-%m-%d %H:%M:%S",
                    "%Y%m%d%H%M%S",
                    "%Y-%m-%d",
                    "%Y%m%d"
                ]
                
                for fmt in formats:
                    try:
                        return datetime.strptime(dt_value, fmt).isoformat()
                    except ValueError:
                        continue
                
                return dt_value  # Return as is if can't parse
            
            elif isinstance(dt_value, (int, float)):
                # Julian day conversion (ARGO standard)
                base_date = datetime(1950, 1, 1)
                target_date = base_date + timedelta(days=float(dt_value))
                return target_date.isoformat()
            
            else:
                return str(dt_value)
                
        except Exception as e:
            logger.warning(f"Error parsing datetime {dt_value}: {e}")
            return datetime.utcnow().isoformat()
    
    def _calculate_seawater_properties(self, temp: float, sal: float, pres: float) -> Dict[str, float]:
        """
        Calculate comprehensive seawater properties
        Based on TEOS-10 equations of state
        """
        try:
            properties = {}
            
            # Basic validation
            if not all(isinstance(x, (int, float)) and not np.isnan(x) for x in [temp, sal, pres]):
                return properties
            
            # Convert pressure to absolute pressure (add atmospheric)
            abs_pressure = pres + 10.1325  # dbar to absolute pressure
            
            # Density calculation (simplified UNESCO formula)
            # UNESCO 1983 equation of state for seawater
            # This is a simplified version - full TEOS-10 would be more accurate
            
            # Pure water density at atmospheric pressure
            rho_w = (999.842594 + 6.793952e-2*temp - 9.095290e-3*temp**2 + 
                     1.001685e-4*temp**3 - 1.120083e-6*temp**4 + 6.536332e-9*temp**5)
            
            # Salinity effects
            A = (8.24493e-1 - 4.0899e-3*temp + 7.6438e-5*temp**2 - 
                 8.2467e-7*temp**3 + 5.3875e-9*temp**4)
            B = (-5.72466e-3 + 1.0227e-4*temp - 1.6546e-6*temp**2)
            C = 4.8314e-4
            
            rho_0 = rho_w + A*sal + B*sal**(3/2) + C*sal**2
            
            # Pressure effects (simplified)
            K = (19652.21 + 148.4206*temp - 2.327105*temp**2 + 
                 1.360477e-2*temp**3 - 5.155288e-5*temp**4)
            K += (54.6746 - 0.603459*temp + 1.09987e-2*temp**2 - 6.1670e-5*temp**3) * sal
            K += (7.944e-2 + 1.6483e-2*temp - 5.3009e-4*temp**2) * sal**(3/2)
            K += pres * (3.239908 + 1.43713e-3*temp + 1.16092e-4*temp**2 - 5.77905e-7*temp**3)
            
            properties['density'] = rho_0 / (1 - abs_pressure/K)
            
            # Potential temperature (simplified)
            # This would require iterative solution in full implementation
            theta_factor = pres * (3.6504e-4 + temp * (8.3198e-5 + temp * (-5.4065e-7 + temp * 4.0274e-9)))
            properties['potential_temperature'] = temp - theta_factor
            
            # Buoyancy frequency squared (N²) - placeholder
            # This would require vertical gradient calculation in practice
            properties['buoyancy_frequency_squared'] = 0.0
            
            # Sound speed (simplified Chen-Millero equation)
            c = (1402.388 + 5.03830*temp - 5.81090e-2*temp**2 + 3.3432e-4*temp**3 - 
                 1.47797e-6*temp**4 + 3.1419e-9*temp**5)
            c += (0.153563*sal + 6.8999e-4*sal**2 - 8.1829e-6*sal**3)
            c += pres * (3.1260e-5 - 1.7111e-6*temp + 2.5986e-8*temp**2 - 2.5353e-10*temp**3)
            c += pres**2 * (-9.7729e-9 + 3.8513e-10*temp - 2.3654e-12*temp**2)
            
            properties['sound_speed'] = c
            
            # Oxygen solubility (Garcia-Gordon formula - simplified)
            if sal > 0:
                ln_C_star = (-58.3877 + 85.8079/((temp + 273.15)/100) + 
                            23.8439 * np.log((temp + 273.15)/100))
                ln_C_star += sal * (-0.034892 + 0.015568 * (temp + 273.15)/100 - 
                                  0.0019387 * ((temp + 273.15)/100)**2)
                properties['oxygen_solubility'] = np.exp(ln_C_star)  # μmol/kg
            
            return properties
            
        except Exception as e:
            logger.warning(f"Error calculating seawater properties: {e}")
            return {}

    def _identify_water_masses_comprehensive(self, profiles: List[Dict]) -> Dict[str, Any]:
        """
        Comprehensive water mass identification using T-S characteristics
        Enhanced with multiple classification schemes
        """
        try:
            water_masses = []
            classification_stats = {}
            
            for profile in profiles:
                measurements = profile.get('measurements', [])
                if not measurements:
                    continue
                
                profile_water_masses = []
                
                for measurement in measurements:
                    temp = measurement.get('temperature')
                    sal = measurement.get('salinity')
                    pres = measurement.get('pressure')
                    
                    if not all(x is not None for x in [temp, sal, pres]):
                        continue
                    
                    # Comprehensive water mass classification
                    water_mass_type = self._classify_water_mass_type(temp, sal, pres)
                    
                    if water_mass_type != 'Unclassified':
                        profile_water_masses.append({
                            'pressure': pres,
                            'water_mass_type': water_mass_type,
                            'temperature': temp,
                            'salinity': sal,
                            'confidence': self._calculate_classification_confidence(temp, sal, water_mass_type)
                        })
                
                if profile_water_masses:
                    water_masses.append({
                        'profile_id': profile.get('profile_id'),
                        'water_masses': profile_water_masses,
                        'dominant_water_mass': max(profile_water_masses, 
                                                 key=lambda x: x['confidence'])['water_mass_type']
                    })
            
            # Calculate classification statistics
            all_types = [wm['water_mass_type'] for profile in water_masses 
                        for wm in profile.get('water_masses', [])]
            
            if all_types:
                from collections import Counter
                type_counts = Counter(all_types)
                classification_stats = {
                    'total_classifications': len(all_types),
                    'unique_types': len(type_counts),
                    'type_distribution': dict(type_counts),
                    'dominant_type': type_counts.most_common(1)[0][0]
                }
            
            return {
                'water_masses': water_masses,
                'statistics': classification_stats,
                'processing_info': {
                    'classification_method': 'T-S_characteristics_comprehensive',
                    'total_profiles_analyzed': len(profiles),
                    'profiles_with_classifications': len(water_masses)
                }
            }
            
        except Exception as e:
            logger.error(f"Error in comprehensive water mass identification: {e}")
            return {'water_masses': [], 'statistics': {}, 'processing_info': {}}
    
    def _classify_water_mass_type(self, temp: float, sal: float, pres: float) -> str:
        """
        Detailed water mass classification based on T-S characteristics
        """
        try:
            # Convert pressure to approximate depth (rough conversion)
            depth = pres * 1.02  # dbar to meters approximately
            
            # Surface waters (0-200m)
            if depth < 200:
                if temp > 25 and sal > 35:
                    return 'Tropical Surface Water'
                elif temp > 20 and sal < 35:
                    return 'Subtropical Surface Water'
                elif 10 < temp < 20:
                    return 'Temperate Surface Water'
                elif temp < 10:
                    return 'Subpolar Surface Water'
            
            # Intermediate waters (200-1000m)
            elif 200 <= depth < 1000:
                if temp > 15:
                    return 'Subtropical Underwater'
                elif 8 < temp <= 15 and 34.5 < sal < 35.5:
                    return 'Central Water'
                elif 4 < temp <= 8 and sal < 34.5:
                    return 'Intermediate Water'
                elif temp <= 4 and sal < 34.4:
                    return 'Antarctic Intermediate Water'
                elif sal > 35.5:
                    return 'Mediterranean Water'
            
            # Deep waters (1000-4000m)
            elif 1000 <= depth < 4000:
                if 2 < temp < 4 and 34.6 < sal < 35.0:
                    return 'North Atlantic Deep Water'
                elif 0 < temp <= 2 and sal < 34.7:
                    return 'Antarctic Deep Water'
                elif temp > 4:
                    return 'Modified Deep Water'
            
            # Bottom waters (>4000m)
            elif depth >= 4000:
                if temp < 2 and sal < 34.7:
                    return 'Antarctic Bottom Water'
                elif temp < 4:
                    return 'Deep Bottom Water'
            
            return 'Unclassified'
            
        except Exception as e:
            logger.warning(f"Error classifying water mass: {e}")
            return 'Unclassified'
    
    def _calculate_classification_confidence(self, temp: float, sal: float, water_mass_type: str) -> float:
        """
        Calculate confidence score for water mass classification
        """
        try:
            # Define typical ranges for each water mass type
            type_ranges = {
                'Tropical Surface Water': {'temp': (25, 30), 'sal': (35, 37)},
                'Subtropical Surface Water': {'temp': (20, 25), 'sal': (34, 36)},
                'Temperate Surface Water': {'temp': (10, 20), 'sal': (33, 35)},
                'Central Water': {'temp': (8, 15), 'sal': (34.5, 35.5)},
                'Antarctic Intermediate Water': {'temp': (2, 4), 'sal': (34.2, 34.4)},
                'North Atlantic Deep Water': {'temp': (2, 4), 'sal': (34.6, 35.0)},
                'Antarctic Bottom Water': {'temp': (-0.5, 2), 'sal': (34.6, 34.7)}
            }
            
            if water_mass_type not in type_ranges:
                return 0.5  # Default confidence for uncharacterized types
            
            ranges = type_ranges[water_mass_type]
            temp_range = ranges['temp']
            sal_range = ranges['sal']
            
            # Calculate how well the values fit within the expected ranges
            temp_fit = 1.0 if temp_range[0] <= temp <= temp_range[1] else max(0.1, 
                1.0 - min(abs(temp - temp_range[0]), abs(temp - temp_range[1])) / (temp_range[1] - temp_range[0]))
            
            sal_fit = 1.0 if sal_range[0] <= sal <= sal_range[1] else max(0.1,
                1.0 - min(abs(sal - sal_range[0]), abs(sal - sal_range[1])) / (sal_range[1] - sal_range[0]))
            
            # Combined confidence (weighted average)
            confidence = (temp_fit * 0.6 + sal_fit * 0.4)
            
            return min(1.0, max(0.1, confidence))
            
        except Exception as e:
            logger.warning(f"Error calculating classification confidence: {e}")
            return 0.5
    
    def _extract_measurements(self, profile: Dict[str, Any]) -> List[Dict]:
        """Extract measurement data from profile"""
        measurements = []
        
        # Common ARGO parameters
        params = ['temp', 'psal', 'pres', 'doxy', 'chla', 'bbp700', 'ph_in_situ_total']
        
        for param in params:
            if param in profile and profile[param] is not None:
                measurement = {
                    "parameter": param,
                    "value": profile[param],
                    "qc": profile.get(f"{param}_qc", 1),
                    "adjusted": profile.get(f"{param}_adjusted"),
                    "adjusted_qc": profile.get(f"{param}_adjusted_qc"),
                    "adjusted_error": profile.get(f"{param}_adjusted_error")
                }
                measurements.append(measurement)
        
        return measurements
    
    def _extract_qc_flags(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Extract QC flags from profile"""
        qc_flags = {}
        
        qc_keys = [k for k in profile.keys() if k.endswith('_qc')]
        for qc_key in qc_keys:
            qc_flags[qc_key] = profile[qc_key]
        
        return qc_flags
    
    async def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        if not self.is_available:
            return {
                "success": False,
                "message": "Supabase not available",
                "stats": {"storage_type": "fallback_cache"}
            }
        
        try:
            # Get float and profile counts
            floats_result = await argo_floats_db.get_all_floats(limit=1)
            profiles_result = await argo_profiles_db.search_profiles(limit=1)
            
            stats = {
                "storage_type": "supabase",
                "total_floats": 0,
                "total_profiles": 0,
                "data_sources": [],
                "last_update": datetime.utcnow().isoformat()
            }
            
            if floats_result["success"]:
                # This is a simplified count - in production you'd want proper count queries
                stats["total_floats"] = len(floats_result.get("data", []))
            
            if profiles_result["success"]:
                stats["total_profiles"] = len(profiles_result.get("data", []))
            
            return {
                "success": True,
                "stats": stats,
                "message": "Storage statistics retrieved"
            }
            
        except Exception as e:
            logger.error(f"Error getting storage stats: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to get storage statistics"
            }
    
    async def search_profiles(self, query_params: Dict[str, Any] = None, limit: int = 100) -> Dict[str, Any]:
        """Search ARGO profiles with filters"""
        if not self.is_available:
            return {
                "success": False,
                "message": "Supabase not available"
            }
        
        try:
            result = await argo_profiles_db.search_profiles(query_params, limit)
            return result
            
        except Exception as e:
            logger.error(f"Error searching profiles: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to search profiles"
            }

    async def store_float(self, float_data: Dict[str, Any]) -> bool:
        """
        Store a single ARGO float metadata
        
        Args:
            float_data: Dictionary with float metadata
            
        Returns:
            True if stored successfully, False otherwise
        """
        if not self.is_available:
            logger.warning("Supabase not available, cannot store float")
            return False
        
        try:
            # Insert float data into argo_floats table
            result = self.supabase_client.table('argo_floats').insert(float_data).execute()
            
            if result.data:
                logger.info(f"Float {float_data.get('float_id', 'unknown')} stored successfully")
                return True
            else:
                logger.error(f"Failed to store float {float_data.get('float_id', 'unknown')}")
                return False
                
        except Exception as e:
            logger.error(f"Error storing float: {str(e)}")
            return False

    def _validate_coordinate(self, coord: float, coord_type: str = "coordinate") -> bool:
        """
        Validate coordinate values (latitude/longitude)
        
        Args:
            coord: Coordinate value to validate
            coord_type: Type of coordinate ('latitude' or 'longitude')
            
        Returns:
            True if coordinate is valid, False otherwise
        """
        if coord is None:
            return False
            
        try:
            coord = float(coord)
            
            if coord_type.lower() == "latitude":
                return -90.0 <= coord <= 90.0
            elif coord_type.lower() == "longitude":
                return -180.0 <= coord <= 180.0
            else:
                # General coordinate validation
                return -180.0 <= coord <= 180.0
                
        except (ValueError, TypeError):
            return False

# Initialize the service
supabase_storage_service = SupabaseDataStorageService()