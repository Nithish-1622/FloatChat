"""
ARGO Data Storage and Preprocessing Service
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
except ImportError:
    # Fallback for development
    pa = None
    pq = None

from config import (
    DATA_PROCESSING_CONFIG,
    GEOGRAPHICAL_REGIONS,
    DATA_DIR
)

from models.schemas import ArgoProfile, ArgoFloat

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArgoDataStorage:
    """Main class for ARGO data storage and preprocessing"""
    
    def __init__(self):
        self.engine = None
        self.Session = None
        self.parquet_dir = DATA_DIR / "parquet"
        self.parquet_dir.mkdir(parents=True, exist_ok=True)
        
        # Data partitioning configuration
        self.core_vars = DATA_PROCESSING_CONFIG["core_variables"]
        self.bgc_vars = DATA_PROCESSING_CONFIG["bgc_variables"]
        self.depth_levels = DATA_PROCESSING_CONFIG["depth_levels"]
        
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize database connection and create tables"""
        try:
            if create_engine is None:
                logger.warning("SQLAlchemy not available - running in mock mode")
                return
                
            self.engine = create_engine(
                DATABASE_URL,
                echo=False,
                pool_size=10,
                max_overflow=20,
                pool_timeout=30,
                pool_recycle=3600
            )
            
            self.Session = sessionmaker(bind=self.engine)
            
            # Create tables if they don't exist
            Base.metadata.create_all(self.engine)
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {str(e)}")
            self.engine = None
            self.Session = None
    
    def store_profiles_batch(self, profiles: List[Dict[str, Any]], source_name: str) -> Dict[str, int]:
        """
        Store a batch of ARGO profiles in both PostgreSQL and Parquet
        """
        results = {
            "stored_profiles": 0,
            "stored_floats": 0,
            "skipped_profiles": 0,
            "errors": 0
        }
        
        if not profiles:
            return results
        
        try:
            # Group profiles by float
            float_groups = self._group_profiles_by_float(profiles)
            
            # Store in database
            if self.Session:
                db_results = self._store_in_database(float_groups, source_name)
                results.update(db_results)
            
            # Store in Parquet
            parquet_results = self._store_in_parquet(profiles, source_name)
            results["parquet_files"] = parquet_results
            
            logger.info(f"Batch storage complete: {results}")
            
        except Exception as e:
            logger.error(f"Error in batch storage: {str(e)}")
            results["errors"] += 1
        
        return results
    
    def _group_profiles_by_float(self, profiles: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group profiles by platform_id (float)"""
        float_groups = {}
        
        for profile in profiles:
            platform_id = profile.get("platform_id", "unknown")
            if platform_id not in float_groups:
                float_groups[platform_id] = []
            float_groups[platform_id].append(profile)
        
        return float_groups
    
    def _store_in_database(self, float_groups: Dict[str, List[Dict[str, Any]]], source_name: str) -> Dict[str, int]:
        """Store profiles in PostgreSQL database"""
        results = {"stored_profiles": 0, "stored_floats": 0, "skipped_profiles": 0}
        
        with self.Session() as session:
            try:
                for platform_id, profiles in float_groups.items():
                    # Store or update float metadata
                    float_stored = self._store_float_metadata(session, platform_id, profiles, source_name)
                    if float_stored:
                        results["stored_floats"] += 1
                    
                    # Store profiles
                    for profile in profiles:
                        profile_stored = self._store_profile_metadata(session, profile, source_name)
                        if profile_stored:
                            results["stored_profiles"] += 1
                        else:
                            results["skipped_profiles"] += 1
                
                session.commit()
                
            except Exception as e:
                logger.error(f"Database storage error: {str(e)}")
                session.rollback()
                raise
        
        return results
    
    def _store_float_metadata(self, session: Session, platform_id: str, profiles: List[Dict[str, Any]], source_name: str) -> bool:
        """Store or update float metadata"""
        try:
            # Check if float already exists
            existing_float = session.query(ArgoFloatDB).filter_by(platform_id=platform_id).first()
            
            if existing_float:
                # Update existing float with latest information
                latest_profile = max(profiles, key=lambda p: p.get('timestamp', datetime.min))
                
                existing_float.last_location_date = latest_profile.get('timestamp')
                existing_float.last_latitude = latest_profile.get('latitude')
                existing_float.last_longitude = latest_profile.get('longitude')
                existing_float.profile_count = len(profiles)
                existing_float.updated_at = datetime.utcnow()
                
                return False  # Updated, not newly stored
            else:
                # Create new float record
                first_profile = min(profiles, key=lambda p: p.get('timestamp', datetime.max))
                latest_profile = max(profiles, key=lambda p: p.get('timestamp', datetime.min))
                
                new_float = ArgoFloatDB(
                    platform_id=platform_id,
                    deployment_date=first_profile.get('timestamp'),
                    deployment_latitude=first_profile.get('latitude'),
                    deployment_longitude=first_profile.get('longitude'),
                    last_location_date=latest_profile.get('timestamp'),
                    last_latitude=latest_profile.get('latitude'),
                    last_longitude=latest_profile.get('longitude'),
                    profile_count=len(profiles),
                    data_centre=first_profile.get('data_centre'),
                    status="ACTIVE"
                )
                
                session.add(new_float)
                return True  # Newly stored
                
        except Exception as e:
            logger.error(f"Error storing float metadata for {platform_id}: {str(e)}")
            return False
    
    def _store_profile_metadata(self, session: Session, profile: Dict[str, Any], source_name: str) -> bool:
        """Store profile metadata"""
        try:
            profile_id = profile.get('profile_id')
            if not profile_id:
                return False
            
            # Check if profile already exists
            existing_profile = session.query(ArgoProfileDB).filter_by(profile_id=profile_id).first()
            
            if existing_profile:
                logger.debug(f"Profile {profile_id} already exists")
                return False
            
            # Create parquet file path
            timestamp = profile.get('timestamp', datetime.utcnow())
            region = self._assign_geographical_region(
                profile.get('latitude', 0), 
                profile.get('longitude', 0)
            )
            
            parquet_path = self._generate_parquet_path(timestamp, region, profile_id)
            
            # Create new profile record
            new_profile = ArgoProfileDB(
                profile_id=profile_id,
                platform_id=profile.get('platform_id'),
                cycle_number=profile.get('cycle_number', 0),
                latitude=profile.get('latitude'),
                longitude=profile.get('longitude'),
                timestamp=timestamp,
                
                # Data availability flags
                has_temperature=bool(profile.get('temperature')),
                has_salinity=bool(profile.get('salinity')),
                has_oxygen=bool(profile.get('oxygen')),
                has_nitrate=bool(profile.get('nitrate')),
                has_chlorophyll=bool(profile.get('chlorophyll')),
                has_ph=bool(profile.get('ph')),
                
                # QC summaries
                temperature_qc_summary=self._summarize_qc_flags(profile.get('temperature_qc', [])),
                salinity_qc_summary=self._summarize_qc_flags(profile.get('salinity_qc', [])),
                oxygen_qc_summary=self._summarize_qc_flags(profile.get('oxygen_qc', [])),
                
                # File paths
                parquet_path=str(parquet_path),
                
                # Metadata
                data_mode=profile.get('data_mode', 'R'),
                data_centre=profile.get('data_centre'),
                data_source=source_name,
                
                # Depth statistics
                max_depth=max(profile.get('pressure', [0])) if profile.get('pressure') else None,
                n_levels=len(profile.get('pressure', []))
            )
            
            session.add(new_profile)
            return True
            
        except Exception as e:
            logger.error(f"Error storing profile metadata: {str(e)}")
            return False
    
    def _summarize_qc_flags(self, qc_flags: List[int]) -> str:
        """Summarize QC flags as good/questionable/bad/mixed"""
        if not qc_flags:
            return "unknown"
        
        good_flags = DATA_PROCESSING_CONFIG["qc_flags"]["good"]
        bad_flags = DATA_PROCESSING_CONFIG["qc_flags"]["bad"]
        
        good_count = sum(1 for flag in qc_flags if flag in good_flags)
        bad_count = sum(1 for flag in qc_flags if flag in bad_flags)
        
        total = len(qc_flags)
        good_ratio = good_count / total
        bad_ratio = bad_count / total
        
        if good_ratio >= 0.8:
            return "good"
        elif bad_ratio >= 0.5:
            return "bad"
        elif good_ratio >= 0.5:
            return "mixed"
        else:
            return "questionable"
    
    def _assign_geographical_region(self, latitude: float, longitude: float) -> str:
        """Assign geographical region for data partitioning"""
        for region_name, bounds in GEOGRAPHICAL_REGIONS.items():
            if (bounds["lat_min"] <= latitude <= bounds["lat_max"] and
                bounds["lon_min"] <= longitude <= bounds["lon_max"]):
                return region_name
        
        return "other"
    
    def _generate_parquet_path(self, timestamp: datetime, region: str, profile_id: str) -> Path:
        """Generate parquet file path with partitioning"""
        year = timestamp.year
        month = timestamp.month
        
        parquet_path = (
            self.parquet_dir / 
            f"year={year}" / 
            f"month={month:02d}" / 
            f"region={region}" / 
            f"{profile_id}.parquet"
        )
        
        # Create directory structure
        parquet_path.parent.mkdir(parents=True, exist_ok=True)
        
        return parquet_path
    
    def _store_in_parquet(self, profiles: List[Dict[str, Any]], source_name: str) -> List[str]:
        """Store profiles in Parquet files"""
        parquet_files = []
        
        if pa is None or pq is None:
            logger.warning("PyArrow not available - skipping Parquet storage")
            return parquet_files
        
        try:
            for profile in profiles:
                parquet_file = self._store_single_profile_parquet(profile, source_name)
                if parquet_file:
                    parquet_files.append(parquet_file)
        
        except Exception as e:
            logger.error(f"Error storing profiles in Parquet: {str(e)}")
        
        return parquet_files
    
    def _store_single_profile_parquet(self, profile: Dict[str, Any], source_name: str) -> Optional[str]:
        """Store a single profile in Parquet format"""
        try:
            profile_id = profile.get('profile_id')
            timestamp = profile.get('timestamp', datetime.utcnow())
            region = self._assign_geographical_region(
                profile.get('latitude', 0), 
                profile.get('longitude', 0)
            )
            
            parquet_path = self._generate_parquet_path(timestamp, region, profile_id)
            
            # Skip if file already exists
            if parquet_path.exists():
                logger.debug(f"Parquet file already exists: {parquet_path}")
                return str(parquet_path)
            
            # Prepare data for Parquet storage
            parquet_data = self._prepare_profile_for_parquet(profile, source_name)
            
            # Convert to PyArrow table
            table = pa.table(parquet_data)
            
            # Write to Parquet file
            pq.write_table(table, parquet_path, compression='snappy')
            
            logger.debug(f"Stored profile in Parquet: {parquet_path}")
            return str(parquet_path)
            
        except Exception as e:
            logger.error(f"Error storing profile {profile.get('profile_id')} in Parquet: {str(e)}")
            return None
    
    def _prepare_profile_for_parquet(self, profile: Dict[str, Any], source_name: str) -> Dict[str, Any]:
        """Prepare profile data for Parquet storage"""
        # Flatten profile data into tabular format
        measurements = []
        
        # Get core measurement arrays
        pressure = profile.get('pressure', [])
        temperature = profile.get('temperature', [])
        salinity = profile.get('salinity', [])
        
        # Get QC flags
        pressure_qc = profile.get('pressure_qc', [])
        temperature_qc = profile.get('temperature_qc', [])
        salinity_qc = profile.get('salinity_qc', [])
        
        # Get BGC variables (optional)
        oxygen = profile.get('oxygen', [])
        nitrate = profile.get('nitrate', [])
        chlorophyll = profile.get('chlorophyll', [])
        ph = profile.get('ph', [])
        
        # Get BGC QC flags
        oxygen_qc = profile.get('oxygen_qc', [])
        nitrate_qc = profile.get('nitrate_qc', [])
        chlorophyll_qc = profile.get('chlorophyll_qc', [])
        
        # Determine maximum length
        max_len = max(
            len(pressure), len(temperature), len(salinity),
            len(oxygen), len(nitrate), len(chlorophyll), len(ph)
        ) if any([pressure, temperature, salinity, oxygen, nitrate, chlorophyll, ph]) else 0
        
        # Create measurements table
        for i in range(max_len):
            measurement = {
                'profile_id': profile.get('profile_id'),
                'platform_id': profile.get('platform_id'),
                'cycle_number': profile.get('cycle_number', 0),
                'latitude': profile.get('latitude'),
                'longitude': profile.get('longitude'),
                'timestamp': profile.get('timestamp'),
                'data_source': source_name,
                'level_index': i,
                
                # Core measurements
                'pressure': pressure[i] if i < len(pressure) else None,
                'temperature': temperature[i] if i < len(temperature) else None,
                'salinity': salinity[i] if i < len(salinity) else None,
                
                # Core QC flags
                'pressure_qc': pressure_qc[i] if i < len(pressure_qc) else 9,
                'temperature_qc': temperature_qc[i] if i < len(temperature_qc) else 9,
                'salinity_qc': salinity_qc[i] if i < len(salinity_qc) else 9,
                
                # BGC measurements
                'oxygen': oxygen[i] if i < len(oxygen) else None,
                'nitrate': nitrate[i] if i < len(nitrate) else None,
                'chlorophyll': chlorophyll[i] if i < len(chlorophyll) else None,
                'ph': ph[i] if i < len(ph) else None,
                
                # BGC QC flags
                'oxygen_qc': oxygen_qc[i] if i < len(oxygen_qc) else 9,
                'nitrate_qc': nitrate_qc[i] if i < len(nitrate_qc) else 9,
                'chlorophyll_qc': chlorophyll_qc[i] if i < len(chlorophyll_qc) else 9,
                
                # Metadata
                'data_mode': profile.get('data_mode', 'R'),
                'data_centre': profile.get('data_centre'),
            }
            
            measurements.append(measurement)
        
        # Convert to columnar format for PyArrow
        if not measurements:
            return {}
        
        columnar_data = {}
        for key in measurements[0].keys():
            columnar_data[key] = [m[key] for m in measurements]
        
        return columnar_data
    
    def load_profiles_from_parquet(self, 
                                 start_date: Optional[datetime] = None,
                                 end_date: Optional[datetime] = None,
                                 region: Optional[str] = None,
                                 max_profiles: int = 1000) -> List[Dict[str, Any]]:
        """Load profiles from Parquet files based on filters"""
        
        if pq is None:
            logger.warning("PyArrow not available - cannot load from Parquet")
            return []
        
        try:
            # Build file path filters
            file_patterns = []
            
            if start_date and end_date:
                # Generate year/month combinations in date range
                current_date = start_date.replace(day=1)
                while current_date <= end_date:
                    year = current_date.year
                    month = current_date.month
                    
                    if region:
                        pattern = f"year={year}/month={month:02d}/region={region}/*.parquet"
                    else:
                        pattern = f"year={year}/month={month:02d}/*/*.parquet"
                    
                    file_patterns.append(pattern)
                    
                    # Move to next month
                    if current_date.month == 12:
                        current_date = current_date.replace(year=current_date.year + 1, month=1)
                    else:
                        current_date = current_date.replace(month=current_date.month + 1)
            else:
                # Load all files (limited by max_profiles)
                if region:
                    file_patterns.append(f"*/*/region={region}/*.parquet")
                else:
                    file_patterns.append(f"*/*/*/*.parquet")
            
            # Load matching files
            profiles = []
            files_loaded = 0
            
            for pattern in file_patterns:
                matching_files = list(self.parquet_dir.glob(pattern))
                
                for parquet_file in matching_files[:max_profiles - len(profiles)]:
                    try:
                        table = pq.read_table(parquet_file)
                        df = table.to_pandas()
                        
                        # Convert back to profile format
                        profile = self._parquet_to_profile(df)
                        if profile:
                            profiles.append(profile)
                            files_loaded += 1
                        
                        if len(profiles) >= max_profiles:
                            break
                            
                    except Exception as e:
                        logger.warning(f"Error loading {parquet_file}: {str(e)}")
                        continue
                
                if len(profiles) >= max_profiles:
                    break
            
            logger.info(f"Loaded {len(profiles)} profiles from {files_loaded} Parquet files")
            return profiles
            
        except Exception as e:
            logger.error(f"Error loading profiles from Parquet: {str(e)}")
            return []
    
    def _parquet_to_profile(self, df: 'pd.DataFrame') -> Optional[Dict[str, Any]]:
        """Convert Parquet DataFrame back to profile format"""
        try:
            if df.empty:
                return None
            
            # Profile metadata (should be same for all rows)
            first_row = df.iloc[0]
            profile = {
                'profile_id': first_row['profile_id'],
                'platform_id': first_row['platform_id'],
                'cycle_number': first_row['cycle_number'],
                'latitude': first_row['latitude'],
                'longitude': first_row['longitude'],
                'timestamp': first_row['timestamp'],
                'data_mode': first_row['data_mode'],
                'data_centre': first_row['data_centre'],
                'data_source': first_row['data_source']
            }
            
            # Extract measurement arrays
            core_vars = ['pressure', 'temperature', 'salinity']
            bgc_vars = ['oxygen', 'nitrate', 'chlorophyll', 'ph']
            
            for var in core_vars + bgc_vars:
                # Get non-null values
                values = df[var].dropna().tolist()
                qc_values = df[f'{var}_qc'].dropna().tolist()
                
                if values:
                    profile[var] = values
                    profile[f'{var}_qc'] = qc_values
            
            return profile
            
        except Exception as e:
            logger.error(f"Error converting Parquet to profile: {str(e)}")
            return None
    
    def get_database_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        if not self.Session:
            return {"error": "Database not available"}
        
        try:
            with self.Session() as session:
                # Count floats and profiles
                float_count = session.query(ArgoFloatDB).count()
                profile_count = session.query(ArgoProfileDB).count()
                
                # Get latest profile date
                latest_profile = session.query(ArgoProfileDB).order_by(ArgoProfileDB.timestamp.desc()).first()
                latest_date = latest_profile.timestamp if latest_profile else None
                
                # Count by data source
                source_counts = session.execute(text("""
                    SELECT data_source, COUNT(*) as count 
                    FROM argo_profiles 
                    GROUP BY data_source
                """)).fetchall()
                
                # Count by region
                region_counts = session.execute(text("""
                    SELECT 
                        CASE 
                            WHEN latitude BETWEEN -50 AND 30 AND longitude BETWEEN 30 AND 120 THEN 'indian_ocean'
                            WHEN latitude BETWEEN -60 AND 60 AND longitude BETWEEN 120 AND -70 THEN 'pacific_ocean'
                            WHEN latitude BETWEEN -60 AND 70 AND longitude BETWEEN -70 AND 30 THEN 'atlantic_ocean'
                            WHEN latitude < -50 THEN 'southern_ocean'
                            WHEN latitude > 66 THEN 'arctic_ocean'
                            ELSE 'other'
                        END as region,
                        COUNT(*) as count
                    FROM argo_profiles
                    GROUP BY region
                """)).fetchall()
                
                return {
                    "total_floats": float_count,
                    "total_profiles": profile_count,
                    "latest_profile_date": latest_date.isoformat() if latest_date else None,
                    "profiles_by_source": {row[0]: row[1] for row in source_counts},
                    "profiles_by_region": {row[0]: row[1] for row in region_counts}
                }
                
        except Exception as e:
            logger.error(f"Error getting database statistics: {str(e)}")
            return {"error": str(e)}