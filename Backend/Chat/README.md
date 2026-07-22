# FloatChat ARGO System# FloatChat ARGO Backend System



## 🌊 AI-Powered Oceanographic Data Analysis PlatformA comprehensive AI-powered backend system for processing and analyzing ARGO oceanographic float data with conversational AI capabilities.



FloatChat is a comprehensive system for analyzing ARGO oceanographic data using advanced AI and machine learning techniques. It combines real-time data ingestion from multiple international sources, vector-based semantic search, and conversational AI to provide intelligent insights into oceanographic patterns.## Overview



## 🚀 FeaturesThis system provides:

- Real-time ARGO float data ingestion from multiple global sources

### Core Capabilities- Advanced data processing and quality control

- **Multi-Source Data Ingestion**: Automated ingestion from 11+ international ARGO data centers- Vector embeddings for semantic search

- **Advanced Preprocessing**: Quality control filtering, derived parameter calculations, water mass identification- RAG (Retrieval Augmented Generation) system

- **Vector Database**: ChromaDB with SentenceTransformers for semantic search and RAG- Conversational AI interface for oceanographic queries

- **Conversational AI**: Groq LLM integration with comprehensive scientific analysis capabilities- RESTful API endpoints

- **Background Automation**: Scheduled tasks for data updates, maintenance, and optimization- Background scheduling for automated updates

- **REST API**: Comprehensive FastAPI endpoints for all system operations

## Architecture

### Data Sources

- NOAA Global Marine Argo Atlas### Core Components

- Euro-Argo Data Centre

- China Argo Real-time Data Center1. **Data Ingestion** (`services/data_ingestion.py`)

- Australian ARGO Data Centre   - Multi-source ARGO data fetching

- Coriolis ARGO Data Centre (France)   - NetCDF file processing

- UK Met Office Argo Data Centre   - Quality control filtering

- Canadian Argo Data Centre   - Async HTTP operations

- German Argo Data Centre

- India National Institute of Ocean Technology2. **Data Storage** (`services/data_storage.py`)

- Brazil Marine Hydrography Center   - PostgreSQL database management

- Japan Agency for Marine-Earth Science and Technology   - Parquet file storage

   - Data preprocessing and validation

## 📋 Prerequisites   - Efficient partitioning strategies



### Required Software3. **Vector Database** (`services/vector_database.py`)

- Python 3.8+   - ChromaDB integration

- PostgreSQL 12+ (or Supabase account)   - Semantic embeddings generation

- Git   - Similarity search capabilities

   - RAG system implementation

### Required API Keys

- **Supabase**: Database and authentication4. **Conversational AI** (`services/conversational_ai.py`)

- **Groq**: AI/LLM services   - Multi-LLM provider support (Groq, OpenAI)

   - Context-aware responses

### Python Dependencies   - Scientific query processing

```bash   - Chat session management

# Core framework

fastapi>=0.104.05. **FastAPI Endpoints** (`api/main.py`)

uvicorn[standard]>=0.24.0   - RESTful API interface

   - Real-time chat processing

# Database & Storage   - Data visualization endpoints

supabase>=1.2.0   - System administration tools

psycopg2-binary>=2.9.7

6. **Background Scheduler** (`services/scheduler.py`)

# AI & ML   - Automated data ingestion

groq>=0.4.0   - Periodic vector database updates

sentence-transformers>=2.2.2   - System maintenance tasks

chromadb>=0.4.15   - Health monitoring



# Data Processing### Data Sources

pandas>=2.1.0

numpy>=1.24.0The system integrates with 11+ ARGO data sources:

netCDF4>=1.6.4- NOAA NCEI Global Ocean Data Portal

xarray>=2023.8.0- INCOIS Indian Ocean Data

- UCSD SIO Argo Program

# Scheduling & Background Tasks- IFREMER Global Data Centre

apscheduler>=3.10.4- BGC-Argo Program

- Australia CSIRO Marine Data

# HTTP & Async- Coriolis Operational Oceanography

aiohttp>=3.8.5- And more...

aiofiles>=23.2.0

## Installation

# Utilities

python-dotenv>=1.0.0### Prerequisites

python-multipart>=0.0.6

pydantic>=2.4.0- Python 3.8+

```- PostgreSQL with PostGIS extension

- 8GB+ RAM (recommended)

## 🛠 Installation- 50GB+ disk space



### 1. Clone the Repository### Dependencies

```bash

git clone <repository-url>```bash

cd FloatChat/Backend/Chatpip install -r requirements.txt

``````



### 2. Create Virtual Environment### Environment Setup

```bash

python -m venv venvCreate a `.env` file:

source venv/bin/activate  # On Windows: venv\Scripts\activate

``````env

# Database

### 3. Install DependenciesDATABASE_URL=postgresql://username:password@localhost:5432/floatchat

```bashPOSTGRES_USER=your_username

pip install -r requirements.txtPOSTGRES_PASSWORD=your_password

```POSTGRES_DB=floatchat



### 4. Environment Setup# LLM APIs

Create a `.env` file in the `Backend/Chat` directory:GROQ_API_KEY=your_groq_api_key

OPENAI_API_KEY=your_openai_api_key

```env

# Supabase Configuration# Application

SUPABASE_URL=your_supabase_project_urlENVIRONMENT=development

SUPABASE_ANON_KEY=your_supabase_anon_keySECRET_KEY=your_secret_key

SUPABASE_SERVICE_KEY=your_supabase_service_role_keyLOG_LEVEL=INFO

```

# Groq API Configuration

GROQ_API_KEY=your_groq_api_key### Database Setup



# Optional: System Configuration1. Install PostgreSQL and PostGIS

ARGO_DATA_UPDATE_INTERVAL=24  # hours2. Create database and user

VECTOR_DB_REFRESH_INTERVAL=12  # hours3. Run migrations:

CLEANUP_INTERVAL=168  # hours (weekly)

``````python

from models.database import init_database

### 5. Database Setupimport asyncio



#### Option A: Using Supabase (Recommended)asyncio.run(init_database())

1. Create a new Supabase project```

2. Copy your project URL and API keys to `.env`

3. Execute the SQL schema in Supabase SQL Editor:## Usage

```bash

# Copy contents of supabase_schema.sql and run in Supabase SQL Editor### Standalone Application

```

```bash

#### Option B: Local PostgreSQLpython main.py

1. Install PostgreSQL locally```

2. Create database: `createdb floatchat_argo`

3. Update connection string in `supabase_config.py`### FastAPI Server

4. Run schema: `psql -d floatchat_argo -f supabase_schema.sql`

```bash

## 🚦 Quick Startuvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

```

### 1. System Initialization

Run the system initialization to set up all services and validate the installation:### API Endpoints



```bash#### Chat Interface

python system_initialization.py- `POST /chat` - Process chat messages

```- `GET /chat/sessions/{session_id}` - Get chat session history

- `DELETE /chat/sessions/{session_id}` - Delete chat session

This will:

- Validate database connection and schema#### Data Queries

- Initialize all services (data storage, AI, vector DB)- `GET /data/profiles` - Search ARGO profiles

- Set up default data sources- `GET /data/floats` - List available floats

- Run integration tests- `GET /data/regions` - Get regional statistics

- Generate a comprehensive system report- `POST /data/export` - Export data in various formats



### 2. Start the System#### System Management

Launch the complete FloatChat system:- `GET /admin/health` - System health check

- `GET /admin/stats` - System statistics

```bash- `POST /admin/maintenance` - Trigger maintenance tasks

# Production mode- `GET /admin/jobs` - Background job status

python startup.py

### Configuration

# Development mode with auto-reload

python startup.py --devEdit `config.py` to customize:

- Data source endpoints

# Custom configuration- Processing parameters

python startup.py --host 0.0.0.0 --port 8000 --log-level debug- LLM configurations

```- Storage settings

- Scheduling intervals

### 3. Access the System

- **API Documentation**: http://localhost:8000/docs## Data Processing Pipeline

- **Health Check**: http://localhost:8000/health

- **System Status**: http://localhost:8000/1. **Ingestion**: Fetch NetCDF files from ARGO sources

2. **Quality Control**: Filter profiles using QC flags

## 📡 API Endpoints3. **Storage**: Save to PostgreSQL and Parquet files

4. **Embedding**: Generate vector embeddings for profiles

### Core Endpoints5. **Indexing**: Store embeddings in ChromaDB

- `GET /` - System status and information6. **Query Processing**: Semantic search and RAG responses

- `GET /health` - Health check with service status

- `GET /docs` - Interactive API documentation## Features



### Chat & AI### Scientific Capabilities

- `POST /chat` - Send messages to the AI system- Temperature, salinity, pressure profile analysis

- `GET /chat/sessions` - List chat sessions- Biogeochemical parameter processing (BGC-ARGO)

- `DELETE /chat/sessions/{session_id}` - Delete chat session- Geographic and temporal filtering

- Quality control flag interpretation

### Data Operations- Ocean region classification

- `POST /ingest` - Trigger data ingestion

- `GET /search` - Search oceanographic data### AI Features

- `GET /profiles` - Get ARGO profile data- Natural language query processing

- `GET /floats` - Get ARGO float information- Scientific context understanding

- Multi-source data integration

### Administration- Conversational memory

- `GET /admin/scheduler/status` - Get scheduler status- Adaptive response generation

- `GET /admin/system/stats` - System statistics

- `POST /admin/maintenance` - Trigger maintenance tasks### Performance

- Async processing for scalability

## 💬 Using the Chat System- Efficient data partitioning

- Vector similarity search

### Example Requests- Caching mechanisms

- Background task scheduling

#### General Inquiry

```bash## Monitoring and Maintenance

curl -X POST "http://localhost:8000/chat" \

     -H "Content-Type: application/json" \### Health Checks

     -d '{- Database connectivity

       "message": "What is ARGO and how does it work?",- API endpoint availability

       "session_id": "user123",- Data source accessibility

       "conversation_type": "general_inquiry"- Vector database status

     }'- Background job monitoring

```

### Automated Tasks

#### Data Analysis- Daily data ingestion

```bash- Weekly database cleanup

curl -X POST "http://localhost:8000/chat" \- Monthly vector index optimization

     -H "Content-Type: application/json" \- System health reporting

     -d '{

       "message": "Show me temperature trends in the North Atlantic",### Logging

       "session_id": "user123", - Comprehensive logging to files and console

       "conversation_type": "data_analysis"- Error tracking and debugging

     }'- Performance metrics

```- User interaction logs



#### Scientific Research## API Documentation

```bash

curl -X POST "http://localhost:8000/chat" \Once the server is running, visit:

     -H "Content-Type: application/json" \- Swagger UI: `http://localhost:8000/docs`

     -d '{- ReDoc: `http://localhost:8000/redoc`

       "message": "Analyze water mass characteristics in the Pacific Ocean",

       "session_id": "user123",## Development

       "conversation_type": "scientific_research"

     }'### Running Tests

``````bash

pytest tests/

## 🔧 Configuration```



### System Configuration### Code Quality

Main configuration options in `config.py`:```bash

flake8 .

```pythonblack .

# Data update frequenciesmypy .

DATA_UPDATE_INTERVAL = 24  # hours```

VECTOR_REFRESH_INTERVAL = 12  # hours

CLEANUP_INTERVAL = 168  # hours### Environment Variables

- `ENVIRONMENT`: development/staging/production

# Processing limits- `LOG_LEVEL`: DEBUG/INFO/WARNING/ERROR

MAX_PROFILES_PER_BATCH = 1000- `MAX_WORKERS`: Number of async workers

MAX_CONCURRENT_DOWNLOADS = 10- `CACHE_TTL`: Cache time-to-live in seconds



# AI Configuration## Production Deployment

DEFAULT_AI_TEMPERATURE = 0.1

MAX_CONTEXT_LENGTH = 8000### Docker

``````dockerfile

# Example Dockerfile structure

### Scheduler ConfigurationFROM python:3.11-slim

Background tasks are automatically configured but can be customized:WORKDIR /app

COPY requirements.txt .

- **Daily Data Ingestion**: 2:00 AM UTCRUN pip install -r requirements.txt

- **Hourly Session Cleanup**: Every hourCOPY . .

- **Weekly Vector DB Optimization**: Sundays at 3:00 AM UTCCMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

- **Daily Health Checks**: Every 30 minutes```



## 📊 Monitoring & Maintenance### System Requirements

- 4+ CPU cores

### Health Monitoring- 16GB+ RAM

The system provides comprehensive health monitoring:- 100GB+ SSD storage

- PostgreSQL 13+

```bash- Redis (optional, for caching)

# Check overall system health

curl http://localhost:8000/health### Security

- API key authentication

# Get detailed scheduler status  - Rate limiting

curl http://localhost:8000/admin/scheduler/status- Input validation

- SQL injection prevention

# View system statistics- CORS configuration

curl http://localhost:8000/admin/system/stats

```## Troubleshooting



### Log Files### Common Issues

System logs are stored in the `logs/` directory:

- `system_initialization.log` - Setup and initialization logs1. **Database Connection Errors**

- `scheduler.log` - Background task execution logs   - Check PostgreSQL service status

- `api.log` - FastAPI request/response logs   - Verify connection string

- `health_YYYYMMDD.json` - Daily health check data   - Ensure PostGIS extension is installed



### Manual Maintenance2. **LLM API Errors**

Trigger manual maintenance tasks:   - Validate API keys

   - Check rate limits

```bash   - Monitor token usage

# Trigger data ingestion

curl -X POST http://localhost:8000/ingest3. **Memory Issues**

   - Adjust batch sizes

# Run system maintenance   - Enable garbage collection

curl -X POST http://localhost:8000/admin/maintenance   - Monitor system resources

```

4. **Data Ingestion Failures**

## 🧪 Testing   - Check internet connectivity

   - Verify data source endpoints

### Run System Tests   - Review error logs

```bash

# Full system initialization test### Performance Optimization

python system_initialization.py

1. **Database**

# API endpoint tests     - Create proper indexes

python -m pytest tests/ -v   - Optimize query patterns

   - Use connection pooling

# Integration tests

python -m pytest tests/integration/ -v2. **Vector Database**

```   - Adjust embedding dimensions

   - Optimize collection size

### Performance Testing   - Use efficient similarity metrics

```bash

# Load test the API3. **API**

python tests/load_test.py   - Enable response caching

   - Implement request batching

# Vector database performance   - Use async processing

python tests/vector_db_performance.py

```## Contributing



## 🔍 Troubleshooting1. Fork the repository

2. Create a feature branch

### Common Issues3. Make your changes

4. Add tests

#### Database Connection Failed5. Submit a pull request

- Verify Supabase credentials in `.env`

- Check network connectivity## License

- Ensure Supabase project is active

This project is licensed under the MIT License - see the LICENSE file for details.

#### AI Service Not Responding

- Verify Groq API key in `.env`## Support

- Check API rate limits

- Review Groq service statusFor support, please contact the development team or create an issue in the repository.



#### Data Ingestion Errors## Acknowledgments

- Check internet connectivity

- Verify ARGO data source availability- ARGO Program for oceanographic data

- Review ingestion logs in `logs/`- Open-source community for libraries

- Scientific computing ecosystem

#### Vector Database Issues- AI/ML research community
- Check ChromaDB installation
- Verify sufficient disk space
- Review vector database logs

### Debug Mode
Run the system in debug mode for detailed logging:

```bash
python startup.py --dev --log-level debug
```

### Getting Help
1. Check the logs in the `logs/` directory
2. Review the system health endpoint: `/health`
3. Run the system initialization script for diagnostics
4. Check the API documentation at `/docs`

## 📚 Architecture

### System Components
```
┌─────────────────────┐
│   FastAPI Server    │  ← REST API endpoints
└─────────┬───────────┘
          │
┌─────────┴───────────┐
│  Service Layer      │
├─────────────────────┤
│ • Data Ingestion    │  ← Multi-source ARGO data
│ • Data Storage      │  ← Supabase + preprocessing  
│ • Vector Database   │  ← ChromaDB + embeddings
│ • Conversational AI │  ← Groq LLM + RAG
│ • Scheduler Service │  ← Background automation
└─────────┬───────────┘
          │
┌─────────┴───────────┐
│  Data Layer         │
├─────────────────────┤
│ • Supabase/PostgreSQL│  ← Structured data
│ • ChromaDB          │  ← Vector embeddings
│ • File System       │  ← NetCDF files & cache
└─────────────────────┘
```

### Data Flow
1. **Ingestion**: Multi-source ARGO data → NetCDF processing → Quality control
2. **Storage**: Structured data → Supabase, Vector embeddings → ChromaDB
3. **Query**: User question → Vector search → Context retrieval → AI response
4. **Automation**: Scheduled tasks → Data updates → System maintenance

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Install development dependencies: `pip install -r requirements-dev.txt`
4. Run tests: `python -m pytest`
5. Submit pull request

### Code Standards
- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write comprehensive docstrings
- Include unit tests for new features
- Update documentation for API changes

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- ARGO Program and international data centers
- Supabase for managed database services
- Groq for AI/LLM capabilities
- ChromaDB for vector database technology
- The oceanographic research community

---

**FloatChat ARGO System** - Transforming oceanographic data analysis with AI