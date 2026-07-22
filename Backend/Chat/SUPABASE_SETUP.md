# FloatChat Supabase Migration Guide

This guide helps you migrate from PostgreSQL to Supabase for your FloatChat ARGO system.

## Prerequisites

✅ **Completed Steps:**
- [x] Supabase Python client installed
- [x] Environment variables configured
- [x] Supabase configuration module created
- [x] Database models updated
- [x] API endpoints updated

## 🚀 Next Steps: Complete Supabase Setup

### Step 1: Create Supabase Project

1. **Go to Supabase Dashboard:**
   - Visit [https://supabase.com](https://supabase.com)
   - Sign up or log in to your account
   - Click "New Project"

2. **Project Configuration:**
   - **Organization:** Select or create organization
   - **Name:** `FloatChat-ARGO`
   - **Database Password:** Create a strong password (save this!)
   - **Region:** Choose closest to your users
   - **Pricing Plan:** Start with Free tier

3. **Wait for Setup:** Project creation takes 2-3 minutes

### Step 2: Get Your Project Credentials

1. **Go to Settings > API:**
   - Find your **Project URL** (starts with `https://`)
   - Find your **anon public key** (starts with `eyJ...`)
   - Find your **service_role secret key** (starts with `eyJ...`)

2. **Update Your `.env` File:**
   ```bash
   # Replace these with your actual Supabase credentials
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

### Step 3: Create Database Schema

1. **Go to SQL Editor in Supabase Dashboard:**
   - Click "SQL Editor" in the left sidebar
   - Click "New Query"

2. **Execute Schema Creation:**
   - Copy the entire contents of `supabase_schema.sql`
   - Paste into the SQL Editor
   - Click "Run" to execute

3. **Verify Tables Created:**
   - Go to "Table Editor"
   - You should see tables: `argo_floats`, `argo_profiles`, `chat_sessions`, etc.

### Step 4: Test Supabase Connection

Run the API server and test the Supabase connection:

```bash
# Activate your Python environment
cd k:\F\FloatChat\Backend\Chat

# Run the API server
python simple_api.py
```

Then test the connection:
```bash
# Open another terminal and test
curl http://localhost:8000/admin/supabase_test
```

Expected successful response:
```json
{
    "success": true,
    "message": "Supabase connection successful",
    "storage_service_available": true,
    "storage_stats": {
        "storage_type": "supabase",
        "total_floats": 0,
        "total_profiles": 0
    }
}
```

## 📊 Database Schema Overview

### Core Tables Created:

1. **`argo_floats`** - Float metadata and deployment info
2. **`argo_profiles`** - Individual profile measurements  
3. **`chat_sessions`** - User chat sessions
4. **`chat_messages`** - Chat conversation history
5. **`data_processing_jobs`** - Background job tracking
6. **`data_sources`** - External data source configuration
7. **`vector_embeddings`** - RAG system embeddings

### Key Features:
- ✅ **UUID Primary Keys** for all tables
- ✅ **Automatic timestamps** (created_at, updated_at)
- ✅ **JSONB columns** for flexible metadata storage
- ✅ **Proper indexing** for performance
- ✅ **Row Level Security (RLS)** enabled
- ✅ **Foreign key constraints** for data integrity

## 🔧 API Endpoints Updated

Your API now supports Supabase with fallback to mock data:

- **`GET /health`** - Health check with Supabase status
- **`POST /chat`** - Enhanced chat with database integration
- **`POST /data/search_profiles`** - Search profiles with filters
- **`GET /data/float/{float_id}`** - Get float information
- **`GET /data/stats`** - Database statistics
- **`GET /admin/supabase_test`** - Test Supabase connection

## 🧪 Testing Your Setup

### 1. Test Health Check
```bash
curl http://localhost:8000/health
```

### 2. Test Chat Function
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about ARGO floats"}'
```

### 3. Test Data Search
```bash
curl -X POST http://localhost:8000/data/search_profiles \
  -H "Content-Type: application/json" \
  -d '{"limit": 10}'
```

### 4. Test Storage Stats
```bash
curl http://localhost:8000/data/stats
```

## 📈 Migration Benefits

### What You've Gained:

✅ **Managed Database:** No more PostgreSQL maintenance  
✅ **Real-time Features:** Built-in subscriptions and webhooks  
✅ **Automatic Backups:** Enterprise-grade data protection  
✅ **Global CDN:** Fast data access worldwide  
✅ **Built-in Auth:** Ready for user authentication  
✅ **API Auto-generation:** REST and GraphQL APIs  
✅ **Dashboard:** Visual database management  
✅ **Scalability:** Automatic scaling based on usage  

### Graceful Fallbacks:
- ✅ **Mock Data:** System works even if Supabase is unavailable
- ✅ **Error Handling:** Comprehensive error management
- ✅ **Logging:** Detailed logging for debugging

## 🚨 Troubleshooting

### Connection Issues:
1. **Check Environment Variables:** Ensure `.env` file has correct values
2. **Verify Project Status:** Check Supabase dashboard for project health
3. **Test API Keys:** Use SQL Editor to test permissions
4. **Check Network:** Ensure no firewall blocking requests

### Schema Issues:
1. **Run Schema Again:** SQL Editor allows re-running schema creation
2. **Check Logs:** View logs in Supabase dashboard
3. **Verify Permissions:** Ensure service role has proper permissions

### API Issues:
1. **Check Logs:** View Python server logs for errors
2. **Test Connection:** Use `/admin/supabase_test` endpoint
3. **Verify Installation:** Ensure `supabase` package is installed

## 🎯 What's Next?

1. **Load Sample Data:** Add some test ARGO profiles to your database
2. **Configure Real-time:** Set up subscriptions for live updates
3. **Add Authentication:** Implement user login/signup
4. **Deploy to Production:** Deploy both API and database to cloud
5. **Monitor Performance:** Set up alerts and monitoring

## 💡 Tips

- **Start Small:** Test with a few profiles first
- **Monitor Usage:** Keep track of database row count on free tier
- **Backup Strategy:** Export important data regularly
- **Security:** Never commit actual API keys to version control

---

**Your FloatChat system is now ready for Supabase! 🎉**

The migration provides a solid foundation for scaling your ARGO data processing system with enterprise-grade database capabilities.