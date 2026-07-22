from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # Add this import
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import requests
import asyncio
import os
from dotenv import load_dotenv
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Ocean News API",
    description="REST API for fetching ocean-related news and facts",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware - THIS IS THE IMPORTANT ADDITION!
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # React dev server (backup)
        "http://127.0.0.1:5173",  # Alternative localhost format
        "http://127.0.0.1:3000"   # Alternative localhost format
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

class OceanTopic(str, Enum):
    ALL = "all"
    MARINE_BIOLOGY = "marine_biology"
    OCEAN_POLLUTION = "ocean_pollution"
    SEA_LEVEL_RISE = "sea_level_rise"
    CORAL_REEFS = "coral_reefs"
    DEEP_SEA = "deep_sea"
    MARINE_CONSERVATION = "marine_conservation"
    OCEANOGRAPHY = "oceanography"
    OCEAN_CLIMATE = "ocean_climate"
    OCEAN_TECHNOLOGY = "ocean_technology"

class NewsArticle(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    urlToImage: Optional[str] = None
    publishedAt: str
    source: Dict[str, Any]
    content: Optional[str] = None
    ocean_relevance_score: float = Field(ge=0.0, le=100.0)
    ocean_topics: List[str] = []

class OceanNewsResponse(BaseModel):
    status: str
    totalResults: int
    articles: List[NewsArticle]
    query_info: Dict[str, Any]
    fetched_at: str

class OceanNewsFilter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"
        
        # More inclusive ocean keywords
        self.ocean_keywords = {
            'primary': ['ocean', 'marine', 'sea', 'water', 'coastal', 'maritime', 'aquatic', 'oceanographic'],
            'secondary': ['underwater', 'deep sea', 'surface', 'tide', 'wave', 'current', 'salt water'],
            'biology': ['fish', 'whale', 'dolphin', 'shark', 'coral', 'algae', 'plankton', 'marine life'],
            'research': ['study', 'research', 'scientist', 'data', 'monitoring', 'observation', 'discovery'],
            'climate': ['climate', 'warming', 'temperature', 'ice', 'level', 'acidification'],
            'technology': ['sensor', 'buoy', 'float', 'satellite', 'instrument', 'monitoring'],
            'floatchat': ['temperature', 'thermal', 'monitoring', 'sensor', 'buoy', 'float', 'argo', 'deployment'],
            'exclude': [
                'ocean city', 'ocean drive', 'ocean view hotel', 'ocean county', 
                'casino', 'restaurant menu', 'hotel booking', 'real estate listing'
            ]
        }
        
        # Simplified topic queries for more results
        self.topic_queries = {
            OceanTopic.ALL: '''
                (ocean OR marine OR sea OR "deep sea" OR oceanographic OR coastal OR maritime) 
                NOT (casino OR "hotel booking" OR "real estate" OR "restaurant menu")
            ''',
            OceanTopic.MARINE_BIOLOGY: '''
                (marine OR ocean OR sea) AND (biology OR life OR species OR fish OR whale OR coral OR ecosystem)
                NOT (casino OR hotel OR tourism)
            ''',
            OceanTopic.OCEAN_POLLUTION: '''
                (ocean OR marine OR sea) AND (pollution OR plastic OR waste OR spill OR contamination)
                NOT (hotel OR casino)
            ''',
            OceanTopic.SEA_LEVEL_RISE: '''
                ("sea level" OR "ocean level" OR "rising sea" OR "coastal flooding")
                NOT (hotel OR casino)
            ''',
            OceanTopic.CORAL_REEFS: '''
                (coral OR reef) AND (ocean OR marine OR sea)
                NOT (resort OR hotel OR diving OR tourism)
            ''',
            OceanTopic.DEEP_SEA: '''
                ("deep sea" OR "deep ocean" OR "ocean floor" OR "ocean depth")
                NOT (movie OR game OR fiction)
            ''',
            OceanTopic.MARINE_CONSERVATION: '''
                (marine OR ocean OR sea) AND (conservation OR protection OR sanctuary OR preservation)
                NOT (tourism OR hotel)
            ''',
            OceanTopic.OCEAN_TECHNOLOGY: '''
                (ocean OR marine OR sea) AND (technology OR sensor OR buoy OR float OR monitoring OR instrument)
                NOT (game OR entertainment)
            ''',
            OceanTopic.OCEANOGRAPHY: '''
                (oceanography OR "ocean science" OR "marine research" OR "ocean data")
                NOT (university OR course)
            ''',
            OceanTopic.OCEAN_CLIMATE: '''
                (ocean OR marine OR sea) AND (climate OR temperature OR warming OR acidification)
                NOT (vacation OR travel)
            '''
        }

    async def fetch_ocean_news(
        self, 
        topic: OceanTopic = OceanTopic.ALL,
        days_back: int = 7,
        max_articles: int = 100,
        sources: Optional[str] = None,
        exclude_terms: Optional[str] = None,
        focus_floatchat: bool = True
    ) -> Dict[str, Any]:
        
        # Build query
        base_query = self.topic_queries.get(topic, self.topic_queries[OceanTopic.ALL])
        
        # Add user exclusions
        if exclude_terms:
            exclude_list = [term.strip() for term in exclude_terms.split(",")]
            exclude_query = " NOT (" + " OR ".join(f'"{term}"' for term in exclude_list) + ")"
            base_query += exclude_query
        
        from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        params = {
            'apiKey': self.api_key,
            'q': base_query,
            'from': from_date,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': min(max_articles, 100),
            'searchIn': 'title,description'
        }
        
        # Use broader sources for more articles
        if not sources:
            params['domains'] = "bbc.co.uk,reuters.com,cnn.com,nationalgeographic.com,sciencedaily.com,theguardian.com,washingtonpost.com,nytimes.com"
        elif sources:
            params['domains'] = sources
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get('articles', [])
            
            logger.info(f"Raw articles fetched: {len(articles)}")
            
            # More lenient filtering and scoring
            validated_articles = await self._validate_and_score_articles_lenient(articles, topic, focus_floatchat)
            
            logger.info(f"Articles after validation: {len(validated_articles)}")
            
            return {
                'status': 'ok',
                'totalResults': len(validated_articles),
                'articles': validated_articles,
                'query_info': {
                    'topic': topic,
                    'query_used': base_query,
                    'days_back': days_back,
                    'sources_filter': sources or "multiple_sources",
                    'exclude_terms': exclude_terms,
                    'floatchat_focused': focus_floatchat,
                    'raw_articles_count': len(articles)
                },
                'fetched_at': datetime.now().isoformat()
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"News API request failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"News API request failed: {str(e)}")

    async def _validate_and_score_articles_lenient(self, articles: List[Dict], topic: OceanTopic, focus_floatchat: bool = True) -> List[Dict]:
        validated_articles = []
        
        for article in articles:
            title = article.get('title', '').lower()
            description = article.get('description', '').lower() if article.get('description') else ''
            
            # More lenient ocean content validation
            has_ocean_content = self._validate_ocean_content_lenient(title, description)
            has_excluded_content = self._has_excluded_content_strict(title, description)
            
            # Lower threshold for more articles
            min_score = 3.0 if focus_floatchat else 2.0
            
            if has_ocean_content and not has_excluded_content:
                # Calculate score with more lenient criteria
                score = self._calculate_lenient_relevance_score(title, description, focus_floatchat)
                
                if score >= min_score:
                    # Identify topics using the correct method name
                    ocean_topics = self._identify_ocean_topics_broad(title, description)  # Fixed method name
                    
                    # Add metadata using the correct method name
                    floatchat_metadata = self._extract_floatchat_metadata_lenient(title, description)  # Fixed method name
                    
                    article_data = {
                        **article,
                        'ocean_relevance_score': round(score, 2),
                        'ocean_topics': ocean_topics,
                        'floatchat_relevance': floatchat_metadata
                    }
                    validated_articles.append(article_data)
        
        # Sort by relevance score (highest first)
        validated_articles.sort(key=lambda x: x['ocean_relevance_score'], reverse=True)
        
        # Ensure we have at least some articles by being more inclusive
        if len(validated_articles) < 5:
            logger.warning(f"Only {len(validated_articles)} articles found, adding more with lower criteria")
            # Add more articles with even lower standards
            for article in articles:
                if len(validated_articles) >= 15:
                    break
                    
                title = article.get('title', '').lower()
                description = article.get('description', '').lower() if article.get('description') else ''
                
                # Very basic ocean check
                basic_ocean_terms = ['ocean', 'marine', 'sea', 'water', 'fish', 'whale', 'coral', 'coast']
                has_basic_ocean = any(term in title + description for term in basic_ocean_terms)
                has_bad_content = any(term in title + description for term in ['casino', 'hotel booking', 'restaurant menu'])
                
                if has_basic_ocean and not has_bad_content:
                    # Check if not already added
                    if not any(existing['url'] == article['url'] for existing in validated_articles):
                        article_data = {
                            **article,
                            'ocean_relevance_score': 2.0,
                            'ocean_topics': ['General Ocean'],
                            'floatchat_relevance': {'urgency_level': 'low', 'data_type': []}
                        }
                        validated_articles.append(article_data)
        
        return validated_articles

    def _validate_ocean_content_lenient(self, title: str, description: str) -> bool:
        text = title + " " + description
        
        # More inclusive ocean keywords
        ocean_terms = [
            'ocean', 'marine', 'sea', 'water', 'aquatic', 'maritime', 'coastal',
            'fish', 'whale', 'dolphin', 'shark', 'coral', 'reef', 'tide',
            'wave', 'current', 'deep', 'surface', 'underwater', 'saltwater'
        ]
        
        # Just need one ocean term
        return any(term in text for term in ocean_terms)

    def _has_excluded_content_strict(self, title: str, description: str) -> bool:
        text = title + " " + description
        
        # Only exclude obvious non-ocean content
        strict_excludes = [
            'casino', 'hotel booking', 'restaurant menu', 'real estate listing',
            'vacation package', 'cruise deal', 'beach resort', 'spa treatment'
        ]
        
        return any(exclude in text for exclude in strict_excludes)

    def _calculate_lenient_relevance_score(self, title: str, description: str, focus_floatchat: bool) -> float:
        text = title + " " + description
        score = 0.0
        
        # Basic ocean terms (medium weight)
        primary_matches = sum(3 for keyword in self.ocean_keywords['primary'] if keyword in text)
        secondary_matches = sum(2 for keyword in self.ocean_keywords['secondary'] if keyword in text)
        biology_matches = sum(2 for keyword in self.ocean_keywords['biology'] if keyword in text)
        
        # Research terms (low weight)
        research_matches = sum(1 for keyword in self.ocean_keywords['research'] if keyword in text)
        
        # Title bonus
        title_bonus = 5 if any(keyword in title for keyword in self.ocean_keywords['primary']) else 0
        
        # FloatChat bonus (if enabled)
        floatchat_bonus = 0
        if focus_floatchat:
            floatchat_bonus = sum(3 for term in self.ocean_keywords['floatchat'] if term in text)
        
        total_score = primary_matches + secondary_matches + biology_matches + research_matches + title_bonus + floatchat_bonus
        
        # Ensure minimum score for any ocean content
        if any(term in text for term in ['ocean', 'marine', 'sea']):
            total_score = max(total_score, 3.0)
        
        return min(total_score, 100.0)

    def _identify_ocean_topics_broad(self, title: str, description: str) -> List[str]:
        """Identify ocean topics with broader criteria"""
        text = title + " " + description
        topics = []
        
        # Broader topic identification
        topic_keywords = {
            'Marine Life': ['fish', 'whale', 'dolphin', 'shark', 'marine life', 'sea life'],
            'Ocean Environment': ['ocean', 'sea', 'marine environment', 'water'],
            'Climate & Weather': ['climate', 'weather', 'temperature', 'warming', 'storm'],
            'Research & Science': ['research', 'study', 'scientist', 'discovery', 'data'],
            'Conservation': ['conservation', 'protection', 'preservation', 'endangered'],
            'Technology': ['technology', 'sensor', 'monitoring', 'instrument', 'satellite'],
            'Pollution': ['pollution', 'plastic', 'waste', 'contamination', 'spill'],
            'Coastal': ['coastal', 'shore', 'beach', 'tide', 'wave'],
            'FloatChat Relevant': ['temperature', 'buoy', 'float', 'monitoring', 'data', 'sensor']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text for keyword in keywords):
                topics.append(topic)
        
        return topics if topics else ['General Ocean']

    def _extract_floatchat_metadata_lenient(self, title: str, description: str) -> Dict[str, Any]:
        """Extract FloatChat-relevant metadata with lenient criteria"""
        text = title + " " + description
        
        metadata = {
            'has_temperature_data': any(temp in text for temp in ['temperature', 'thermal', 'warm', 'cold', 'heat']),
            'has_location_data': any(loc in text for loc in ['location', 'region', 'area', 'coast', 'waters']),
            'has_monitoring_equipment': any(eq in text for eq in ['sensor', 'buoy', 'float', 'instrument', 'satellite', 'monitoring']),
            'urgency_level': 'low',
            'data_type': []
        }
        
        # Simpler urgency detection
        if any(keyword in text for keyword in ['emergency', 'crisis', 'extreme', 'record']):
            metadata['urgency_level'] = 'high'
        elif any(keyword in text for keyword in ['unusual', 'significant', 'major']):
            metadata['urgency_level'] = 'medium'
        
        # Broader data type identification
        if any(keyword in text for keyword in ['temperature', 'thermal', 'warm', 'cold']):
            metadata['data_type'].append('temperature')
        if any(keyword in text for keyword in ['depth', 'deep', 'surface']):
            metadata['data_type'].append('depth')
        if any(keyword in text for keyword in ['current', 'flow', 'circulation']):
            metadata['data_type'].append('current')
        if any(keyword in text for keyword in ['salinity', 'salt']):
            metadata['data_type'].append('salinity')
        
        return metadata

    # Keep your existing methods for backward compatibility
    def _calculate_ocean_relevance_score(self, title: str, description: str, content: str) -> float:
        """Legacy method - redirects to lenient version"""
        return self._calculate_lenient_relevance_score(title, description, True)

    def _identify_ocean_topics(self, title: str, description: str, content: str) -> List[str]:
        """Legacy method - redirects to broad version"""
        return self._identify_ocean_topics_broad(title, description)

    def _extract_floatchat_metadata(self, title: str, description: str, content: str) -> Dict[str, Any]:
        """Legacy method - redirects to lenient version"""
        return self._extract_floatchat_metadata_lenient(title, description)
        
# Initialize the news filter
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
if not NEWS_API_KEY:
    logger.warning("NEWS_API_KEY not found in environment variables")

ocean_filter = OceanNewsFilter(NEWS_API_KEY) if NEWS_API_KEY else None

# API Endpoints
@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint returning API information"""
    return {
        "message": "Ocean News API",
        "version": "1.0.0",
        "documentation": "/docs",
        "cors_enabled": "true",  # Added CORS status
        "allowed_origins": ["http://localhost:5173", "http://localhost:3000"],
        "endpoints": {
            "ocean_news": "/ocean-news",
            "ocean_topics": "/ocean-topics",
            "latest_ocean_news": "/ocean-news/latest",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    api_status = "configured" if NEWS_API_KEY else "missing_api_key"
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "api_key_status": api_status,
        "cors_enabled": True,  # Added CORS status
        "allowed_origins": ["http://localhost:5173", "http://localhost:3000"]
    }

@app.get("/ocean-news", response_model=OceanNewsResponse)
async def get_ocean_news(
    topic: OceanTopic = Query(default=OceanTopic.ALL, description="Ocean topic to filter news"),
    days_back: int = Query(default=7, ge=1, le=30, description="Number of days to look back for news"),
    max_articles: int = Query(default=50, ge=1, le=100, description="Maximum number of articles to return"),
    sources: Optional[str] = Query(default=None, description="Comma-separated list of news source domains"),
    exclude_terms: Optional[str] = Query(default=None, description="Comma-separated terms to exclude"),
    min_relevance_score: float = Query(default=10.0, ge=0.0, le=100.0, description="Minimum ocean relevance score"),
    floatchat_focus: bool = Query(default=True, description="Focus on FloatChat project relevant content")
):
    """
    Fetch ocean-related news articles with FloatChat project focus
    
    Enhanced for oceanographic monitoring, temperature anomalies, and float deployments
    """
    if not ocean_filter:
        raise HTTPException(status_code=500, detail="News API key not configured")
    
    try:
        logger.info(f"Fetching FloatChat-focused ocean news for topic: {topic.value}")
        
        result = await ocean_filter.fetch_ocean_news(
            topic=topic,
            days_back=days_back,
            max_articles=max_articles,
            sources=sources,
            exclude_terms=exclude_terms,
            focus_floatchat=floatchat_focus
        )
        
        # Filter by minimum relevance score
        filtered_articles = [
            article for article in result['articles'] 
            if article['ocean_relevance_score'] >= min_relevance_score
        ]
        
        result['articles'] = filtered_articles
        result['totalResults'] = len(filtered_articles)
        
        logger.info(f"Successfully returned {len(filtered_articles)} FloatChat-relevant articles")
        
        return result
        
    except Exception as e:
        logger.error(f"Error fetching ocean news: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching ocean news: {str(e)}")

@app.get("/ocean-news/latest")
async def get_latest_ocean_news(
    limit: int = Query(default=10, ge=1, le=50, description="Number of latest articles to return")
):
    """Get the latest ocean news articles (past 24 hours)"""
    if not ocean_filter:
        raise HTTPException(status_code=500, detail="News API key not configured")
    
    result = await ocean_filter.fetch_ocean_news(
        topic=OceanTopic.ALL,
        days_back=1,
        max_articles=limit
    )
    
    return {
        "latest_ocean_news": result['articles'][:limit],
        "fetched_at": result['fetched_at'],
        "count": min(len(result['articles']), limit)
    }

@app.get("/ocean-topics")
async def get_available_ocean_topics():
    """Get all available ocean topic categories"""
    return {
        "available_topics": [
            {"value": topic.value, "label": topic.value.replace("_", " ").title()}
            for topic in OceanTopic
        ],
        "topic_descriptions": {
            "all": "All ocean-related news",
            "marine_biology": "Marine life, species, and biological research",
            "ocean_pollution": "Ocean contamination, plastic pollution, and cleanup efforts",
            "sea_level_rise": "Rising sea levels and coastal impact",
            "coral_reefs": "Coral reef health, bleaching, and restoration",
            "deep_sea": "Deep sea exploration and discoveries",
            "marine_conservation": "Ocean protection and conservation efforts",
            "oceanography": "Ocean science and research",
            "ocean_climate": "Ocean climate change and environmental impact"
        }
    }

@app.get("/ocean-news/by-topic/{topic}")
async def get_ocean_news_by_topic(
    topic: OceanTopic,
    limit: int = Query(default=20, ge=1, le=50)
):
    """Get ocean news for a specific topic"""
    if not ocean_filter:
        raise HTTPException(status_code=500, detail="News API key not configured")
    
    result = await ocean_filter.fetch_ocean_news(
        topic=topic,
        days_back=7,
        max_articles=limit
    )
    
    return {
        "topic": topic.value,
        "articles": result['articles'],
        "total_found": result['totalResults'],
        "query_info": result['query_info']
    }

@app.get("/ocean-news/high-relevance")
async def get_high_relevance_ocean_news(
    min_score: float = Query(default=15.0, ge=10.0, le=50.0, description="Minimum relevance score for high-quality articles"),
    days_back: int = Query(default=7, ge=1, le=14)
):
    """Get only high-relevance ocean news articles"""
    if not ocean_filter:
        raise HTTPException(status_code=500, detail="News API key not configured")
    
    result = await ocean_filter.fetch_ocean_news(
        topic=OceanTopic.ALL,
        days_back=days_back,
        max_articles=100
    )
    
    high_relevance_articles = [
        article for article in result['articles']
        if article['ocean_relevance_score'] >= min_score
    ]
    
    return {
        "high_relevance_articles": high_relevance_articles,
        "min_relevance_score": min_score,
        "total_high_relevance": len(high_relevance_articles),
        "total_articles_scanned": result['totalResults']
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url)
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
