# FloatChat ARGO API 🌊🇮🇳

Interactive API for querying Indian Ocean ARGO float data with LLM-powered responses.

## Features

- **Real Indian Ocean ARGO Data**: 35 floats and profiles across 4 regional areas
- **LLM Integration**: Groq-powered oceanographic expert responses
- **Regional Focus**: Arabian Sea, Bay of Bengal, Central & Southern Indian Ocean
- **RESTful API**: FastAPI with automatic documentation
- **Thunder Client Tests**: Pre-configured API test collection

## Quick Start

### 1. Set up Groq API Key (Optional)
```powershell
# Get a free API key from https://console.groq.com/keys
$env:GROQ_API_KEY = "your-groq-api-key-here"
```

### 2. Start the API Server
```powershell
python start_argo_api.py
```

### 3. Access the API
- **API Server**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/` | GET | API information and status |
| `/health` | GET | Health check and service status |
| `/chat` | POST | Interactive LLM chat with ARGO data |
| `/argo/summary` | GET | Summary of ARGO data in database |
| `/argo/data` | POST | Query ARGO float and profile data |

### Chat Endpoint
**POST /chat**

Interactive chat with oceanographic expert using real ARGO data context.

**Request Body:**
```json
{
  "message": "What are the temperature conditions in the Arabian Sea?",
  "include_data": true,
  "max_profiles": 5
}
```

**Response:**
```json
{
  "response": "Based on the current ARGO data from the Arabian Sea...",
  "argo_data_summary": {
    "profiles_count": 10,
    "target_region": "Arabian_Sea",
    "sample_profiles": [...]
  },
  "query_timestamp": "2025-09-26T12:30:00"
}
```

### Data Query Endpoint
**POST /argo/data**

Query ARGO float and profile data with filtering options.

**Request Body:**
```json
{
  "region": "Arabian_Sea",
  "max_results": 10,
  "date_range_days": 30
}
```

## Testing with Thunder Client

### 1. Install Thunder Client Extension
- Open VS Code
- Install "Thunder Client" extension
- Open Thunder Client tab

### 2. Import Test Collection
- Click "Import" in Thunder Client
- Select `thunder-tests/thunderclient.json`
- Run the pre-configured tests

### 3. Sample Test Queries

#### Basic Health Check
```http
GET http://localhost:8000/health
```

#### Chat with ARGO Data
```http
POST http://localhost:8000/chat
Content-Type: application/json

{
  "message": "How does salinity vary in the Bay of Bengal?",
  "include_data": true,
  "max_profiles": 5
}
```

#### Regional Data Query
```http
POST http://localhost:8000/argo/data
Content-Type: application/json

{
  "region": "Central_Indian",
  "max_results": 5
}
```

## Sample Questions to Ask

### Temperature Analysis
- "What are the surface temperatures in the Arabian Sea?"
- "How does the thermocline vary across Indian Ocean regions?"
- "Compare temperature profiles between Arabian Sea and Bay of Bengal"

### Salinity Patterns  
- "Why is Bay of Bengal salinity lower than Arabian Sea?"
- "Explain the salinity gradient in the Central Indian Ocean"
- "How do monsoons affect Indian Ocean salinity?"

### Regional Comparisons
- "Compare all four Indian Ocean regions oceanographically"
- "What makes the Southern Indian Ocean different?"
- "Describe the unique characteristics of each region"

### Technical Queries
- "How deep do ARGO floats sample?"
- "What parameters do ARGO floats measure?"
- "Show me recent profile data from INCOIS floats"

## Regional Data Coverage

### Arabian Sea (10 profiles)
- **Temperature**: 25-30°C (high surface temps)
- **Salinity**: 35.5-36.5 psu (high salinity)
- **Characteristics**: Warm, highly saline waters

### Bay of Bengal (8 profiles)  
- **Temperature**: 26-30°C (warm waters)
- **Salinity**: 32-35 psu (lower due to river discharge)
- **Characteristics**: Fresher waters, monsoon influenced

### Central Indian Ocean (14 profiles)
- **Temperature**: 26-29°C (equatorial conditions)  
- **Salinity**: 34.5-35.5 psu (typical oceanic)
- **Characteristics**: Equatorial dynamics, consistent temps

### Southern Indian Ocean (3 profiles)
- **Temperature**: 15-20°C (cooler subtropical)
- **Salinity**: 34-35 psu (subtropical characteristics)  
- **Characteristics**: Cooler waters, subtropical convergence

## Error Handling

The API includes comprehensive error handling:

- **503 Service Unavailable**: Database connection issues
- **500 Internal Server Error**: Processing errors
- **422 Validation Error**: Invalid request parameters

## Development Notes

### Dependencies
- FastAPI: Web framework
- Uvicorn: ASGI server
- Groq: LLM integration
- Supabase: Database connection

### Data Source
- Based on IFREMER ARGO patterns
- 35 realistic Indian Ocean profiles
- INCOIS data center integration
- Real oceanographic conditions

## Next Steps

1. **Test the API** with Thunder Client
2. **Try different chat queries** to explore the data
3. **Analyze regional patterns** using the data endpoints  
4. **Extend with more regions** or real-time data sources

Happy exploring the Indian Ocean! 🌊🇮🇳