#!/usr/bin/env python3
"""
FloatChat ARGO API Startup Script
Sets up environment and starts the API server
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Setup environment variables and paths"""
    print("🌊 FloatChat ARGO API Startup")
    print("=" * 40)
    
    # Check if GROQ API key is set
    if not os.environ.get("GROQ_API_KEY"):
        print("⚠️ GROQ_API_KEY not found in environment variables")
        print("\nTo enable LLM responses, set your Groq API key:")
        print("PowerShell: $env:GROQ_API_KEY='your-key-here'")
        print("Bash: export GROQ_API_KEY='your-key-here'")
        print("\nGet a free key from: https://console.groq.com/keys")
        print("\nContinuing without LLM (data queries will still work)...")
    else:
        print("✅ GROQ API key found")
    
    # Add current directory to Python path
    current_dir = Path(__file__).parent
    if str(current_dir) not in sys.path:
        sys.path.append(str(current_dir))
    
    return True

def start_api_server():
    """Start the FastAPI server"""
    import uvicorn
    
    print("\n🚀 Starting FloatChat ARGO API Server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("📖 API docs will be at: http://localhost:8000/docs")
    print("🧪 Thunder Client tests available in thunder-tests/ folder")
    print("\n🇮🇳 Ready to serve Indian Ocean ARGO data!")
    print("Press Ctrl+C to stop the server\n")
    
    # Import and run the FastAPI app
    from argo_llm_api import app
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

def main():
    """Main startup function"""
    try:
        if setup_environment():
            start_api_server()
    except KeyboardInterrupt:
        print("\n\n👋 FloatChat ARGO API stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()