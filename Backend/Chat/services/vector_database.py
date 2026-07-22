"""
Vector Database Service for ARGO Data
Comprehensive ChromaDB implementation with SentenceTransformers for semantic search
Provides RAG (Retrieval-Augmented Generation) capabilities for oceanographic data
"""
import chromadb
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional, Tuple, Union
import logging
import json
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
import uuid
import hashlib

# Supabase integration
try:
    from ..supabase_models import argo_profiles_db
    from ..supabase_config import get_supabase_client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

logger = logging.getLogger(__name__)

class ArgoVectorDatabase:
    """
    Comprehensive Vector Database for ARGO Oceanographic Data
    Features:
    - ChromaDB for vector storage and similarity search
    - SentenceTransformer embeddings for semantic search
    - Multi-modal embeddings (text descriptions, numerical data, metadata)
    - Hybrid search combining vector similarity and metadata filtering
    - RAG system for context-aware oceanographic queries
    """
    
    def __init__(self, collection_name: str = "argo_profiles", persist_directory: str = "./chroma_db"):
        self.collection_name = collection_name
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(exist_ok=True)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=str(self.persist_directory))
        
        # Initialize sentence transformer for embeddings
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast and efficient
        # Alternative models for specialized use:
        # 'sentence-transformers/all-mpnet-base-v2'  # Better quality
        # 'sentence-transformers/msmarco-distilbert-base-v4'  # Better for search
        
        # Create or get collection
        self.collection = self._initialize_collection()
        
        # Configuration for embedding generation
        self.embedding_config = {
            'max_sequence_length': 512,
            'include_metadata_fields': [
                'ocean_basin', 'water_mass_types', 'depth_range', 
                'temperature_range', 'salinity_range', 'data_mode'
            ],
            'numerical_scaling': {
                'temperature': (-5, 35),  # Typical ocean temperature range
                'salinity': (30, 40),     # Typical salinity range
                'pressure': (0, 6000),    # Typical depth range
                'oxygen': (0, 400)        # Typical oxygen range
            }
        }
    def _initialize_collection(self) -> chromadb.Collection:
        """Initialize or get existing ChromaDB collection"""
        try:
            # Try to get existing collection
            collection = self.client.get_collection(name=self.collection_name)
            logger.info(f"Using existing collection '{self.collection_name}' with {collection.count()} documents")
        except Exception:
            # Create new collection
            collection = self.client.create_collection(
                name=self.collection_name,
                metadata={
                    "description": "ARGO oceanographic profile embeddings",
                    "embedding_model": "all-MiniLM-L6-v2",
                    "created_at": datetime.utcnow().isoformat()
                }
            )
            logger.info(f"Created new collection '{self.collection_name}'")
        
        return collection
    
    async def add_profile_embeddings(self, profiles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Add ARGO profiles to vector database with comprehensive embeddings
        """
        try:
            processed_profiles = 0
            successful_embeddings = 0
            errors = []
            
            for profile in profiles:
                try:
                    # Generate comprehensive embedding
                    embedding_data = await self._generate_profile_embedding(profile)
                    
                    if embedding_data:
                        # Add to ChromaDB
                        self.collection.add(
                            embeddings=[embedding_data['embedding']],
                            documents=[embedding_data['document_text']],
                            metadatas=[embedding_data['metadata']],
                            ids=[embedding_data['id']]
                        )
                        successful_embeddings += 1
                    
                    processed_profiles += 1
                    
                    # Log progress for large batches
                    if processed_profiles % 100 == 0:
                        logger.info(f"Processed {processed_profiles} profiles for embedding")
                
                except Exception as e:
                    error_msg = f"Error processing profile {profile.get('profile_id', 'unknown')}: {str(e)}"
                    errors.append(error_msg)
                    logger.warning(error_msg)
            
            return {
                'success': True,
                'processed_profiles': processed_profiles,
                'successful_embeddings': successful_embeddings,
                'errors': errors,
                'collection_size': self.collection.count()
            }
            
        except Exception as e:
            logger.error(f"Error adding profile embeddings: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'processed_profiles': 0,
                'successful_embeddings': 0
            }
    
    async def add_profiles(self, profiles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Alias for add_profile_embeddings - Add ARGO profiles to vector database
        
        Args:
            profiles: List of ARGO profile dictionaries
            
        Returns:
            Result dictionary with success status and counts
        """
        return await self.add_profile_embeddings(profiles)

    async def _generate_profile_embedding(self, profile: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Generate comprehensive embedding for ARGO profile
        Combines textual description, numerical features, and metadata
        """
        try:
            profile_id = profile.get('profile_id', str(uuid.uuid4()))
            
            # Generate textual description
            text_description = self._create_profile_description(profile)
            
            # Generate numerical features
            numerical_features = self._extract_numerical_features(profile)
            
            # Create metadata for filtering
            metadata = self._create_embedding_metadata(profile)
            
            # Generate embedding using text description
            # (Could be enhanced to combine with numerical features)
            embedding = self.embedding_model.encode(text_description).tolist()
            
            # Optionally enhance embedding with numerical features
            if numerical_features:
                enhanced_embedding = self._enhance_embedding_with_numerical(
                    embedding, numerical_features
                )
                embedding = enhanced_embedding
            
            return {
                'id': profile_id,
                'embedding': embedding,
                'document_text': text_description,
                'metadata': metadata,
                'numerical_features': numerical_features
            }
            
        except Exception as e:
            logger.error(f"Error generating embedding for profile: {str(e)}")
            return None
    
    def _create_profile_description(self, profile: Dict[str, Any]) -> str:
        """
        Create comprehensive textual description of ARGO profile
        for semantic embedding generation
        """
        try:
            parts = []
            
            # Basic profile information
            lat = profile.get('latitude', 0)
            lon = profile.get('longitude', 0)
            date_time = profile.get('date_time', '')
            ocean_basin = profile.get('ocean_basin', 'unknown')
            
            parts.append(f"Oceanographic profile from {ocean_basin}")
            parts.append(f"located at latitude {lat:.2f}, longitude {lon:.2f}")
            
            if date_time:
                parts.append(f"measured on {date_time}")
            
            # Measurement summary
            measurements = profile.get('measurements', [])
            if measurements:
                temp_values = [m.get('temperature') for m in measurements if m.get('temperature') is not None]
                sal_values = [m.get('salinity') for m in measurements if m.get('salinity') is not None]
                pres_values = [m.get('pressure') for m in measurements if m.get('pressure') is not None]
                
                if temp_values:
                    temp_range = f"temperature ranging from {min(temp_values):.1f} to {max(temp_values):.1f} degrees Celsius"
                    parts.append(temp_range)
                
                if sal_values:
                    sal_range = f"salinity from {min(sal_values):.1f} to {max(sal_values):.1f} PSU"
                    parts.append(sal_range)
                
                if pres_values:
                    depth_range = f"depth profile from {min(pres_values):.1f} to {max(pres_values):.1f} dbar"
                    parts.append(depth_range)
            
            # Derived parameters
            derived_params = profile.get('derived_parameters', {})
            if derived_params:
                if 'mixed_layer_depth' in derived_params:
                    mld = derived_params['mixed_layer_depth']
                    parts.append(f"mixed layer depth of {mld:.1f} meters")
                
                if 'thermocline_depth' in derived_params:
                    tcd = derived_params['thermocline_depth']
                    parts.append(f"thermocline at {tcd:.1f} meters")
                
                if 'dominant_water_mass' in derived_params:
                    water_mass = derived_params['dominant_water_mass']
                    parts.append(f"dominated by {water_mass}")
            
            # Quality control information
            qc_summary = profile.get('qc_summary', {})
            if qc_summary:
                qc_rate = qc_summary.get('qc_pass_rate', 0)
                parts.append(f"with {qc_rate:.1%} data quality")
            
            # Data mode and source
            data_mode = profile.get('data_mode', 'unknown')
            source_name = profile.get('processing_metadata', {}).get('source_name', 'unknown')
            parts.append(f"from {source_name} in {data_mode} mode")
            
            return ". ".join(parts) + "."
            
        except Exception as e:
            logger.warning(f"Error creating profile description: {e}")
            return f"Oceanographic profile {profile.get('profile_id', 'unknown')}"
    
    def _extract_numerical_features(self, profile: Dict[str, Any]) -> Dict[str, List[float]]:
        """
        Extract numerical features for enhanced embedding
        """
        try:
            features = {}
            
            # Basic profile coordinates and time
            features['coordinates'] = [
                float(profile.get('latitude', 0)),
                float(profile.get('longitude', 0))
            ]
            
            # Statistical summary of measurements
            measurements = profile.get('measurements', [])
            if measurements:
                for param in ['temperature', 'salinity', 'pressure', 'oxygen']:
                    values = [m.get(param) for m in measurements if m.get(param) is not None]
                    
                    if values:
                        # Statistical features
                        features[f'{param}_stats'] = [
                            np.mean(values),
                            np.std(values),
                            np.min(values),
                            np.max(values),
                            np.median(values)
                        ]
            
            # Derived parameter features
            derived_params = profile.get('derived_parameters', {})
            if derived_params:
                numerical_derived = []
                for key, value in derived_params.items():
                    if isinstance(value, (int, float)) and not np.isnan(value):
                        numerical_derived.append(value)
                
                if numerical_derived:
                    features['derived_parameters'] = numerical_derived
            
            return features
            
        except Exception as e:
            logger.warning(f"Error extracting numerical features: {e}")
            return {}
    
    def _create_embedding_metadata(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create metadata for filtering and hybrid search
        """
        try:
            metadata = {}
            
            # Basic identifiers
            metadata['profile_id'] = str(profile.get('profile_id', ''))
            metadata['float_id'] = str(profile.get('float_id', ''))
            metadata['cycle_number'] = int(profile.get('cycle_number', 0))
            
            # Geographical information
            metadata['latitude'] = float(profile.get('latitude', 0))
            metadata['longitude'] = float(profile.get('longitude', 0))
            metadata['ocean_basin'] = str(profile.get('ocean_basin', 'unknown'))
            
            # Temporal information
            date_time = profile.get('date_time', '')
            if date_time:
                try:
                    dt = datetime.fromisoformat(date_time.replace('Z', '+00:00'))
                    metadata['year'] = dt.year
                    metadata['month'] = dt.month
                    metadata['season'] = self._get_season(dt.month)
                    metadata['date_time'] = date_time
                except:
                    pass
            
            # Data characteristics
            metadata['data_mode'] = str(profile.get('data_mode', 'R'))
            
            # Measurement ranges
            measurements = profile.get('measurements', [])
            if measurements:
                temp_values = [m.get('temperature') for m in measurements if m.get('temperature') is not None]
                if temp_values:
                    metadata['temp_min'] = float(min(temp_values))
                    metadata['temp_max'] = float(max(temp_values))
                    metadata['temp_range'] = self._categorize_temperature_range(temp_values)
                
                pres_values = [m.get('pressure') for m in measurements if m.get('pressure') is not None]
                if pres_values:
                    metadata['max_depth'] = float(max(pres_values))
                    metadata['depth_category'] = self._categorize_depth(max(pres_values))
            
            # Water mass information
            derived_params = profile.get('derived_parameters', {})
            if derived_params and 'dominant_water_mass' in derived_params:
                metadata['water_mass'] = str(derived_params['dominant_water_mass'])
            
            # Quality information
            qc_summary = profile.get('qc_summary', {})
            if qc_summary:
                metadata['qc_pass_rate'] = float(qc_summary.get('qc_pass_rate', 0))
                metadata['qc_category'] = 'high' if qc_summary.get('qc_pass_rate', 0) > 0.9 else 'medium' if qc_summary.get('qc_pass_rate', 0) > 0.7 else 'low'
            
            # Processing metadata
            processing_meta = profile.get('processing_metadata', {})
            if processing_meta:
                metadata['source_name'] = str(processing_meta.get('source_name', 'unknown'))
                metadata['processed_at'] = str(processing_meta.get('processed_at', ''))
            
            return metadata
            
        except Exception as e:
            logger.warning(f"Error creating embedding metadata: {e}")
            return {'profile_id': str(profile.get('profile_id', 'unknown'))}
    
    def _enhance_embedding_with_numerical(self, text_embedding: List[float], 
                                         numerical_features: Dict[str, List[float]]) -> List[float]:
        """
        Enhance text embedding with normalized numerical features
        """
        try:
            enhanced = text_embedding.copy()
            
            # Normalize and append numerical features
            for feature_name, values in numerical_features.items():
                if feature_name == 'coordinates':
                    # Normalize coordinates to [-1, 1]
                    lat_norm = values[0] / 90.0  # latitude
                    lon_norm = values[1] / 180.0  # longitude
                    enhanced.extend([lat_norm, lon_norm])
                
                elif feature_name.endswith('_stats'):
                    param = feature_name.replace('_stats', '')
                    if param in self.embedding_config['numerical_scaling']:
                        min_val, max_val = self.embedding_config['numerical_scaling'][param]
                        normalized = [(v - min_val) / (max_val - min_val) for v in values]
                        enhanced.extend(normalized)
            
            return enhanced
            
        except Exception as e:
            logger.warning(f"Error enhancing embedding: {e}")
            return text_embedding
    
    def _get_season(self, month: int) -> str:
        """Get season from month"""
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        else:
            return 'autumn'
    
    def _categorize_temperature_range(self, temp_values: List[float]) -> str:
        """Categorize temperature range"""
        mean_temp = np.mean(temp_values)
        if mean_temp > 25:
            return 'tropical'
        elif mean_temp > 15:
            return 'temperate'
        elif mean_temp > 5:
            return 'cold'
        else:
            return 'polar'
    
    def _categorize_depth(self, max_pressure: float) -> str:
        """Categorize profile depth"""
        if max_pressure < 200:
            return 'shallow'
        elif max_pressure < 1000:
            return 'intermediate'
        elif max_pressure < 4000:
            return 'deep'
        else:
            return 'abyssal'
    
    async def semantic_search(self, query: str, n_results: int = 10, 
                             filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform semantic search on ARGO profiles
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Prepare where clause for filtering
            where_clause = {}
            if filters:
                for key, value in filters.items():
                    if isinstance(value, dict) and '$gte' in value or '$lte' in value:
                        # Handle range queries
                        where_clause[key] = value
                    else:
                        where_clause[key] = {"$eq": value}
            
            # Perform vector similarity search
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_clause if where_clause else None,
                include=['documents', 'metadatas', 'distances']
            )
            
            # Format results
            formatted_results = []
            if results['ids'] and results['ids'][0]:
                for i, profile_id in enumerate(results['ids'][0]):
                    formatted_results.append({
                        'profile_id': profile_id,
                        'similarity_score': 1 - results['distances'][0][i],  # Convert distance to similarity
                        'document': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i]
                    })
            
            return {
                'success': True,
                'query': query,
                'results': formatted_results,
                'total_results': len(formatted_results),
                'filters_applied': filters or {}
            }
            
        except Exception as e:
            logger.error(f"Error in semantic search: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'query': query,
                'results': []
            }
    
    def _get_measurement_range(self, values: List[float], var_type: str) -> str:
        """Get formatted range string for measurements"""
        if not values:
            return ""
        
        try:
            min_val = min(values)
            max_val = max(values)
            
            if var_type == 'temperature':
                return f"from {min_val:.1f}°C to {max_val:.1f}°C"
            elif var_type == 'salinity':
                return f"from {min_val:.2f} to {max_val:.2f} PSU"
            elif var_type == 'pressure':
                if max_val > min_val:
                    return f"surface to {max_val:.0f} dbar"
                else:
                    return f"{max_val:.0f} dbar"
            else:
                return f"from {min_val:.2f} to {max_val:.2f}"
                
        except Exception:
            return ""
    
    def add_profile_embedding(self, profile: Dict[str, Any], parquet_path: Optional[str] = None) -> bool:
        """Add profile embedding to vector database"""
        if not self.collection or not self.embedding_model:
            logger.warning("Vector database or embedding model not available")
            return False
        
        try:
            profile_id = profile.get('profile_id')
            if not profile_id:
                logger.error("Profile ID not found")
                return False
            
            # Generate summary
            summary = self.generate_profile_summary(profile)
            
            # Generate embedding
            embedding = self.embedding_model.encode(summary).tolist()
            
            # Prepare metadata
            metadata = {
                'profile_id': profile_id,
                'platform_id': profile.get('platform_id', ''),
                'cycle_number': profile.get('cycle_number', 0),
                'latitude': profile.get('latitude', 0.0),
                'longitude': profile.get('longitude', 0.0),
                'timestamp': profile.get('timestamp', datetime.utcnow()).isoformat(),
                'data_source': profile.get('data_source', ''),
                'has_temperature': bool(profile.get('temperature')),
                'has_salinity': bool(profile.get('salinity')),
                'has_oxygen': bool(profile.get('oxygen')),
                'has_nitrate': bool(profile.get('nitrate')),
                'has_chlorophyll': bool(profile.get('chlorophyll')),
                'parquet_path': parquet_path or ''
            }
            
            # Add to collection
            self.collection.add(
                embeddings=[embedding],
                documents=[summary],
                metadatas=[metadata],
                ids=[profile_id]
            )
            
            logger.debug(f"Added embedding for profile {profile_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding profile embedding: {str(e)}")
            return False
    
    def batch_add_profile_embeddings(self, profiles: List[Dict[str, Any]], parquet_paths: Optional[List[str]] = None) -> int:
        """Add multiple profile embeddings in batch"""
        if not self.collection or not self.embedding_model:
            logger.warning("Vector database or embedding model not available")
            return 0
        
        added_count = 0
        batch_size = 100
        
        for i in range(0, len(profiles), batch_size):
            batch_profiles = profiles[i:i + batch_size]
            batch_paths = parquet_paths[i:i + batch_size] if parquet_paths else [None] * len(batch_profiles)
            
            try:
                # Prepare batch data
                batch_ids = []
                batch_embeddings = []
                batch_documents = []
                batch_metadatas = []
                
                for profile, parquet_path in zip(batch_profiles, batch_paths):
                    profile_id = profile.get('profile_id')
                    if not profile_id:
                        continue
                    
                    # Skip if already exists
                    try:
                        existing = self.collection.get(ids=[profile_id])
                        if existing['ids']:
                            logger.debug(f"Profile {profile_id} already in vector database")
                            continue
                    except:
                        pass  # Profile doesn't exist, continue with addition
                    
                    # Generate summary and embedding
                    summary = self.generate_profile_summary(profile)
                    embedding = self.embedding_model.encode(summary).tolist()
                    
                    # Prepare metadata
                    metadata = {
                        'profile_id': profile_id,
                        'platform_id': profile.get('platform_id', ''),
                        'cycle_number': profile.get('cycle_number', 0),
                        'latitude': profile.get('latitude', 0.0),
                        'longitude': profile.get('longitude', 0.0),
                        'timestamp': profile.get('timestamp', datetime.utcnow()).isoformat(),
                        'data_source': profile.get('data_source', ''),
                        'has_temperature': bool(profile.get('temperature')),
                        'has_salinity': bool(profile.get('salinity')),
                        'has_oxygen': bool(profile.get('oxygen')),
                        'has_nitrate': bool(profile.get('nitrate')),
                        'has_chlorophyll': bool(profile.get('chlorophyll')),
                        'parquet_path': parquet_path or ''
                    }
                    
                    batch_ids.append(profile_id)
                    batch_embeddings.append(embedding)
                    batch_documents.append(summary)
                    batch_metadatas.append(metadata)
                
                # Add batch to collection
                if batch_ids:
                    self.collection.add(
                        embeddings=batch_embeddings,
                        documents=batch_documents,
                        metadatas=batch_metadatas,
                        ids=batch_ids
                    )
                    added_count += len(batch_ids)
                    logger.info(f"Added {len(batch_ids)} embeddings to vector database")
                
            except Exception as e:
                logger.error(f"Error adding batch embeddings: {str(e)}")
                continue
        
        logger.info(f"Total embeddings added: {added_count}")
        return added_count
    
    def semantic_search(self, query: str, n_results: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Perform semantic search for relevant profiles"""
        if not self.collection or not self.embedding_model:
            logger.warning("Vector database or embedding model not available")
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Prepare where clause for filtering
            where_clause = {}
            if filters:
                # Date range filter
                if 'start_date' in filters and 'end_date' in filters:
                    where_clause["timestamp"] = {
                        "$gte": filters['start_date'],
                        "$lte": filters['end_date']
                    }
                
                # Location filter (approximate)
                if 'latitude_min' in filters:
                    where_clause["latitude"] = {"$gte": filters['latitude_min']}
                if 'latitude_max' in filters:
                    if "latitude" not in where_clause:
                        where_clause["latitude"] = {}
                    where_clause["latitude"]["$lte"] = filters['latitude_max']
                
                # Variable availability filters
                if filters.get('has_oxygen'):
                    where_clause["has_oxygen"] = True
                if filters.get('has_nitrate'):
                    where_clause["has_nitrate"] = True
                if filters.get('has_chlorophyll'):
                    where_clause["has_chlorophyll"] = True
            
            # Perform search
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_clause if where_clause else None
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results['ids'][0])):
                result = {
                    'profile_id': results['ids'][0][i],
                    'similarity_score': 1 - results['distances'][0][i],  # Convert distance to similarity
                    'summary': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i]
                }
                formatted_results.append(result)
            
            logger.info(f"Semantic search returned {len(formatted_results)} results for query: {query[:50]}...")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in semantic search: {str(e)}")
            return []
    
    def get_similar_profiles(self, profile_id: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Find profiles similar to a given profile"""
        if not self.collection:
            return []
        
        try:
            # Get the profile's embedding
            profile_data = self.collection.get(
                ids=[profile_id],
                include=['embeddings', 'documents', 'metadatas']
            )
            
            if not profile_data['ids']:
                logger.warning(f"Profile {profile_id} not found in vector database")
                return []
            
            profile_embedding = profile_data['embeddings'][0]
            
            # Search for similar profiles (excluding the original)
            results = self.collection.query(
                query_embeddings=[profile_embedding],
                n_results=n_results + 1,  # +1 to account for the original profile
            )
            
            # Filter out the original profile and format results
            formatted_results = []
            for i in range(len(results['ids'][0])):
                result_id = results['ids'][0][i]
                if result_id != profile_id:  # Skip the original profile
                    result = {
                        'profile_id': result_id,
                        'similarity_score': 1 - results['distances'][0][i],
                        'summary': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i]
                    }
                    formatted_results.append(result)
                    
                    if len(formatted_results) >= n_results:
                        break
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error finding similar profiles: {str(e)}")
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector collection"""
        if not self.collection:
            return {"error": "Vector database not available"}
        
        try:
            # Get collection count
            count_result = self.collection.count()
            
            # Get sample of metadata to analyze distribution
            sample_data = self.collection.get(
                limit=1000,
                include=['metadatas']
            )
            
            # Analyze metadata
            data_sources = {}
            has_bgc_vars = {'oxygen': 0, 'nitrate': 0, 'chlorophyll': 0}
            
            for metadata in sample_data.get('metadatas', []):
                # Count data sources
                source = metadata.get('data_source', 'unknown')
                data_sources[source] = data_sources.get(source, 0) + 1
                
                # Count BGC variables
                for var in has_bgc_vars.keys():
                    if metadata.get(f'has_{var}', False):
                        has_bgc_vars[var] += 1
            
            return {
                'total_profiles': count_result,
                'embedding_dimension': self.embedding_dimension,
                'model_name': self.model_name,
                'data_sources': data_sources,
                'bgc_variables': has_bgc_vars,
                'collection_name': self.collection_name
            }
            
        except Exception as e:
            logger.error(f"Error getting collection stats: {str(e)}")
            return {"error": str(e)}

class ArgoRAGSystem:
    """RAG (Retrieval-Augmented Generation) system for ARGO data queries"""
    
    def __init__(self):
        self.vector_db = ArgoVectorDatabase()
        self.query_templates = self._load_query_templates()
    
    def _load_query_templates(self) -> Dict[str, str]:
        """Load query templates for different types of questions"""
        return {
            'location_search': "ARGO float profiles near {location} in {ocean} ocean",
            'temporal_search': "ARGO profiles collected in {time_period} showing {variables}",
            'variable_search': "ARGO profiles with {variable} measurements from {region}",
            'comparison_search': "ARGO profiles comparing {var1} and {var2} in {region}",
            'bgc_search': "Biogeochemical ARGO profiles with {bgc_variables} from {location}",
            'quality_search': "High quality ARGO {variable} profiles from {region} {time_period}",
            'float_search': "ARGO float {float_id} profiles and trajectory",
            'trend_search': "ARGO {variable} trends and changes in {region} over {time_period}"
        }
    
    def process_natural_language_query(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Process natural language query and return relevant profiles"""
        try:
            # Analyze query to determine type and extract parameters
            query_analysis = self._analyze_query(query)
            
            # Extract filters from query
            filters = self._extract_filters_from_query(query)
            
            # Perform semantic search
            search_results = self.vector_db.semantic_search(
                query=query,
                n_results=max_results,
                filters=filters
            )
            
            # Format response
            response = {
                'query': query,
                'query_type': query_analysis['type'],
                'parameters': query_analysis['parameters'],
                'filters': filters,
                'results': search_results,
                'total_results': len(search_results)
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                'query': query,
                'error': str(e),
                'results': []
            }
    
    def _analyze_query(self, query: str) -> Dict[str, Any]:
        """Analyze query to determine type and extract parameters"""
        query_lower = query.lower()
        
        # Location-based queries
        location_keywords = ['near', 'around', 'close to', 'in the vicinity', 'latitude', 'longitude']
        if any(keyword in query_lower for keyword in location_keywords):
            return {
                'type': 'location_search',
                'parameters': self._extract_location_params(query)
            }
        
        # Time-based queries
        time_keywords = ['month', 'year', 'recent', 'latest', 'since', 'between', 'during']
        if any(keyword in query_lower for keyword in time_keywords):
            return {
                'type': 'temporal_search',
                'parameters': self._extract_temporal_params(query)
            }
        
        # Variable-specific queries
        variable_keywords = ['temperature', 'salinity', 'oxygen', 'nitrate', 'chlorophyll', 'ph']
        if any(keyword in query_lower for keyword in variable_keywords):
            return {
                'type': 'variable_search',
                'parameters': self._extract_variable_params(query)
            }
        
        # BGC queries
        bgc_keywords = ['biogeochemical', 'bgc', 'oxygen', 'nitrate', 'chlorophyll', 'ph']
        if any(keyword in query_lower for keyword in bgc_keywords):
            return {
                'type': 'bgc_search',
                'parameters': self._extract_bgc_params(query)
            }
        
        # Float-specific queries
        if 'float' in query_lower and any(char.isdigit() for char in query):
            return {
                'type': 'float_search',
                'parameters': self._extract_float_params(query)
            }
        
        # Comparison queries
        comparison_keywords = ['compare', 'versus', 'vs', 'against', 'relationship']
        if any(keyword in query_lower for keyword in comparison_keywords):
            return {
                'type': 'comparison_search',
                'parameters': self._extract_comparison_params(query)
            }
        
        # Default to general search
        return {
            'type': 'general_search',
            'parameters': {}
        }
    
    def _extract_filters_from_query(self, query: str) -> Dict[str, Any]:
        """Extract filters from natural language query"""
        filters = {}
        query_lower = query.lower()
        
        # Extract date ranges
        import re
        
        # Look for years (2020, 2021, etc.)
        years = re.findall(r'\b(19|20)\d{2}\b', query)
        if years:
            year = int(years[-1])  # Use the last mentioned year
            filters['start_date'] = f"{year}-01-01T00:00:00"
            filters['end_date'] = f"{year}-12-31T23:59:59"
        
        # Look for months
        months = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12,
            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
            'may': 5, 'jun': 6, 'jul': 7, 'aug': 8,
            'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
        }
        
        for month_name, month_num in months.items():
            if month_name in query_lower:
                if 'start_date' not in filters:
                    # Default to current year if no year specified
                    year = datetime.now().year
                    filters['start_date'] = f"{year}-{month_num:02d}-01T00:00:00"
                    filters['end_date'] = f"{year}-{month_num:02d}-28T23:59:59"
                break
        
        # Look for BGC variable requirements
        if 'oxygen' in query_lower:
            filters['has_oxygen'] = True
        if 'nitrate' in query_lower:
            filters['has_nitrate'] = True
        if 'chlorophyll' in query_lower:
            filters['has_chlorophyll'] = True
        
        return filters
    
    def _extract_location_params(self, query: str) -> Dict[str, Any]:
        """Extract location parameters from query"""
        import re
        
        params = {}
        
        # Look for latitude/longitude coordinates
        lat_pattern = r'(?:lat|latitude)[\s:]*([+-]?\d+\.?\d*)'
        lon_pattern = r'(?:lon|longitude)[\s:]*([+-]?\d+\.?\d*)'
        
        lat_match = re.search(lat_pattern, query.lower())
        lon_match = re.search(lon_pattern, query.lower())
        
        if lat_match:
            params['latitude'] = float(lat_match.group(1))
        if lon_match:
            params['longitude'] = float(lon_match.group(1))
        
        # Look for ocean names
        oceans = ['indian', 'pacific', 'atlantic', 'southern', 'arctic']
        for ocean in oceans:
            if ocean in query.lower():
                params['ocean'] = ocean
                break
        
        return params
    
    def _extract_temporal_params(self, query: str) -> Dict[str, Any]:
        """Extract temporal parameters from query"""
        params = {}
        
        # This would be expanded with more sophisticated date parsing
        if 'recent' in query.lower() or 'latest' in query.lower():
            params['time_range'] = 'recent'
        elif 'last month' in query.lower():
            params['time_range'] = 'last_month'
        elif 'last year' in query.lower():
            params['time_range'] = 'last_year'
        
        return params
    
    def _extract_variable_params(self, query: str) -> Dict[str, Any]:
        """Extract variable parameters from query"""
        params = {}
        
        variables = ['temperature', 'salinity', 'pressure', 'oxygen', 'nitrate', 'chlorophyll', 'ph']
        found_vars = [var for var in variables if var in query.lower()]
        
        if found_vars:
            params['variables'] = found_vars
        
        return params
    
    def _extract_bgc_params(self, query: str) -> Dict[str, Any]:
        """Extract biogeochemical parameters from query"""
        params = {}
        
        bgc_vars = ['oxygen', 'nitrate', 'chlorophyll', 'ph']
        found_vars = [var for var in bgc_vars if var in query.lower()]
        
        if found_vars:
            params['bgc_variables'] = found_vars
        
        return params
    
    def _extract_float_params(self, query: str) -> Dict[str, Any]:
        """Extract float parameters from query"""
        import re
        
        params = {}
        
        # Look for float numbers
        float_pattern = r'\b(\d{7})\b'  # ARGO floats typically have 7-digit IDs
        matches = re.findall(float_pattern, query)
        
        if matches:
            params['float_id'] = matches[0]
        
        return params
    
    def _extract_comparison_params(self, query: str) -> Dict[str, Any]:
        """Extract comparison parameters from query"""
        params = {}
        
        variables = ['temperature', 'salinity', 'oxygen', 'nitrate', 'chlorophyll', 'ph']
        found_vars = [var for var in variables if var in query.lower()]
        
        if len(found_vars) >= 2:
            params['var1'] = found_vars[0]
            params['var2'] = found_vars[1]
        
        return params

# Usage example
async def main():
    """Example usage of the vector database and RAG system"""
    
    # Initialize systems
    vector_db = ArgoVectorDatabase()
    rag_system = ArgoRAGSystem()
    
    # Example profile data (would normally come from data ingestion)
    sample_profile = {
        'profile_id': '1234567_001',
        'platform_id': '1234567',
        'cycle_number': 1,
        'latitude': 20.5,
        'longitude': 65.2,
        'timestamp': datetime.now(),
        'temperature': [25.1, 24.8, 24.5, 23.9, 23.2],
        'salinity': [35.1, 35.2, 35.3, 35.4, 35.5],
        'pressure': [0, 10, 20, 30, 40],
        'oxygen': [220, 215, 210, 205, 200],
        'data_source': 'example_source'
    }
    
    # Add profile to vector database
    if vector_db.add_profile_embedding(sample_profile):
        print("Profile added to vector database")
    
# Convenience functions for direct use
async def initialize_vector_database(collection_name: str = "argo_profiles") -> ArgoVectorDatabase:
    """Initialize and return ARGO vector database instance"""
    try:
        vdb = ArgoVectorDatabase(collection_name=collection_name)
        logger.info(f"Vector database initialized successfully")
        return vdb
    except Exception as e:
        logger.error(f"Failed to initialize vector database: {e}")
        raise

async def add_profiles_to_vector_db(profiles: List[Dict[str, Any]], 
                                   collection_name: str = "argo_profiles") -> Dict[str, Any]:
    """Add ARGO profiles to vector database"""
    try:
        vdb = await initialize_vector_database(collection_name)
        result = await vdb.add_profile_embeddings(profiles)
        return result
    except Exception as e:
        logger.error(f"Failed to add profiles to vector database: {e}")
        return {
            'success': False,
            'error': str(e),
            'processed_profiles': 0
        }

async def search_similar_profiles(query: str, filters: Optional[Dict[str, Any]] = None,
                                 n_results: int = 10, collection_name: str = "argo_profiles") -> Dict[str, Any]:
    """Search for similar ARGO profiles using semantic search"""
    try:
        vdb = await initialize_vector_database(collection_name)
        
        if filters:
            result = await vdb.hybrid_search(query, filters, n_results)
        else:
            result = await vdb.semantic_search(query, n_results)
        
        return result
    except Exception as e:
        logger.error(f"Failed to search profiles: {e}")
        return {
            'success': False,
            'error': str(e),
            'results': []
        }


if __name__ == "__main__":
    # Test the vector database system
    async def test_vector_database():
        """Test vector database functionality"""
        print("Testing ARGO Vector Database...")
        
        # Sample profile data for testing
        test_profiles = [
            {
                "profile_id": "test_001",
                "float_id": "test_float_001",
                "latitude": 45.5,
                "longitude": -30.2,
                "ocean_basin": "North Atlantic",
                "date_time": "2024-01-15T12:00:00",
                "measurements": [
                    {"temperature": 15.2, "salinity": 35.1, "pressure": 10.0},
                    {"temperature": 10.5, "salinity": 35.0, "pressure": 100.0},
                    {"temperature": 4.2, "salinity": 34.8, "pressure": 500.0}
                ],
                "derived_parameters": {
                    "mixed_layer_depth": 50.0,
                    "dominant_water_mass": "North Atlantic Central Water"
                },
                "qc_summary": {"qc_pass_rate": 0.95}
            }
        ]
        
        # Initialize database
        vdb = await initialize_vector_database("test_collection")
        
        # Add test profiles
        add_result = await vdb.add_profile_embeddings(test_profiles)
        print(f"Add result: {add_result}")
        
        # Test semantic search
        search_result = await vdb.semantic_search("North Atlantic temperature profile")
        print(f"Search result: {search_result}")
        
        # Get collection stats
        stats = await vdb.get_collection_stats()
        print(f"Collection stats: {stats}")
    
    # Run test
    asyncio.run(test_vector_database())