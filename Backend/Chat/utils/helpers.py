"""
Utility functions for the FloatChat ARGO system
"""
import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
import logging

logger = logging.getLogger(__name__)

def generate_id(prefix: str = "") -> str:
    """Generate a unique ID with optional prefix"""
    import uuid
    
    unique_id = str(uuid.uuid4())
    return f"{prefix}_{unique_id}" if prefix else unique_id

def hash_content(content: str) -> str:
    """Generate SHA-256 hash of content"""
    return hashlib.sha256(content.encode()).hexdigest()

def safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert value to float"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int(value: Any, default: int = 0) -> int:
    """Safely convert value to integer"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def format_coordinates(latitude: float, longitude: float) -> str:
    """Format coordinates as human-readable string"""
    lat_dir = "N" if latitude >= 0 else "S"
    lon_dir = "E" if longitude >= 0 else "W"
    
    return f"{abs(latitude):.2f}°{lat_dir}, {abs(longitude):.2f}°{lon_dir}"

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two points using Haversine formula
    Returns distance in kilometers
    """
    import math
    
    # Convert to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = (math.sin(dlat/2)**2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
    
    c = 2 * math.asin(math.sqrt(a))
    
    # Earth radius in kilometers
    earth_radius = 6371
    
    return earth_radius * c

def parse_iso_datetime(datetime_str: str) -> Optional[datetime]:
    """Parse ISO format datetime string"""
    try:
        # Handle various ISO formats
        if datetime_str.endswith('Z'):
            datetime_str = datetime_str[:-1] + '+00:00'
        
        return datetime.fromisoformat(datetime_str)
    except Exception as e:
        logger.warning(f"Error parsing datetime '{datetime_str}': {str(e)}")
        return None

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"

def clean_text(text: str) -> str:
    """Clean text for processing"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = " ".join(text.split())
    
    # Remove non-printable characters
    text = "".join(char for char in text if char.isprintable() or char.isspace())
    
    return text.strip()

def validate_coordinates(latitude: float, longitude: float) -> bool:
    """Validate coordinate values"""
    return -90 <= latitude <= 90 and -180 <= longitude <= 180

def get_ocean_region(latitude: float, longitude: float) -> str:
    """Determine ocean region from coordinates"""
    if not validate_coordinates(latitude, longitude):
        return "unknown"
    
    # Simplified ocean boundaries
    if -50 <= latitude <= 30 and 30 <= longitude <= 120:
        return "indian_ocean"
    elif -60 <= latitude <= 60 and (120 <= longitude <= 180 or -180 <= longitude <= -70):
        return "pacific_ocean"
    elif -60 <= latitude <= 70 and -70 <= longitude <= 30:
        return "atlantic_ocean"
    elif latitude < -50:
        return "southern_ocean"
    elif latitude > 66:
        return "arctic_ocean"
    else:
        return "other"

def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """Load JSON file safely"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading JSON file {file_path}: {str(e)}")
        return None

def save_json_file(data: Dict[str, Any], file_path: str) -> bool:
    """Save data to JSON file safely"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return True
    except Exception as e:
        logger.error(f"Error saving JSON file {file_path}: {str(e)}")
        return False

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split list into chunks of specified size"""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """Decorator for retrying functions on failure"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            import asyncio
            
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                    await asyncio.sleep(delay * (2 ** attempt))  # Exponential backoff
            
        return wrapper
    return decorator

def get_environment_info() -> Dict[str, Any]:
    """Get environment information"""
    import platform
    import sys
    
    return {
        'platform': platform.platform(),
        'python_version': sys.version,
        'architecture': platform.architecture(),
        'processor': platform.processor(),
        'hostname': platform.node(),
        'working_directory': os.getcwd(),
        'environment_variables': {
            k: v for k, v in os.environ.items() 
            if not k.upper().endswith(('KEY', 'TOKEN', 'PASSWORD', 'SECRET'))
        }
    }

class PerformanceTimer:
    """Context manager for timing operations"""
    
    def __init__(self, operation_name: str = "Operation"):
        self.operation_name = operation_name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = datetime.utcnow()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = datetime.utcnow()
        duration = (self.end_time - self.start_time).total_seconds()
        
        if exc_type is None:
            logger.info(f"{self.operation_name} completed in {duration:.2f}s")
        else:
            logger.error(f"{self.operation_name} failed after {duration:.2f}s: {exc_val}")
    
    @property
    def duration_seconds(self) -> Optional[float]:
        """Get duration in seconds"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file system operations"""
    import re
    
    # Remove or replace unsafe characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing whitespace and dots
    filename = filename.strip('. ')
    
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    
    return filename

def get_file_info(file_path: str) -> Dict[str, Any]:
    """Get file information"""
    try:
        stat = os.stat(file_path)
        
        return {
            'size_bytes': stat.st_size,
            'size_formatted': format_file_size(stat.st_size),
            'created': datetime.fromtimestamp(stat.st_ctime),
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'accessed': datetime.fromtimestamp(stat.st_atime),
            'permissions': oct(stat.st_mode)[-3:],
            'exists': True
        }
    except Exception as e:
        return {
            'error': str(e),
            'exists': False
        }

def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge two dictionaries"""
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result