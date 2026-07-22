import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic Models for API
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"
    language: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    language: str
    session_id: str
    timestamp: str
    success: bool

class PlatformInfoResponse(BaseModel):
    platform_info: Dict
    supported_languages: Dict
    success: bool

class LanguagesResponse(BaseModel):
    supported_languages: Dict
    success: bool

class HistoryResponse(BaseModel):
    history: List[Dict]
    session_id: str
    success: bool

class HealthResponse(BaseModel):
    status: str
    platform: str
    developer: str
    timestamp: str
    success: bool

@dataclass
class Message:
    """Data class for chat messages""" 
    role: str
    content: str
    timestamp: datetime
    language: str = "en"
    session_id: str = ""

class FloatChatAssistant:
    """Personal Assistant for FloatChat - Ocean Intelligence Platform"""
    
    def __init__(self, groq_api_key: str):
        """Initialize the FloatChat Assistant"""
        self.client = Groq(api_key=groq_api_key)
        
        # 🔄 UPDATED: Latest supported Groq models (December 2024)
        # Trying the most current models available
        self.models = [
            "llama-3.1-8b-instant",      # Primary - fast and reliable
            "llama-3.2-1b-preview",      # Secondary - lightweight
            "llama-3.2-3b-preview",      # Tertiary - medium size
            "gemma-7b-it",               # Fallback - Google's model
            "mixtral-8x7b-32768"         # Last resort - might still work
        ]
        
        self.current_model = self.models[0]  # Start with primary
        self.sessions = {}  # Store conversation sessions
        
        # Supported Indian languages only
        self.supported_languages = {
            "hi": "हिंदी (Hindi)",
            "ta": "தமிழ் (Tamil)",
            "te": "తెలుగు (Telugu)",
            "kn": "ಕನ್ನಡ (Kannada)",
            "en": "English"  # Keep English as base language
        }
        
        # Ocean-specific knowledge base
        self.ocean_knowledge = {
            "marine_navigation": {
                "topics": ["GPS navigation", "weather routing", "cargo optimization", "fishing zones", "coast guard operations"],
                "description": "AI-powered navigation system for fishers, cargo ships, and coast guard"
            },
            "coastal_livelihood": {
                "topics": ["sustainable fisheries", "aquaculture", "eco-tourism", "community development"],
                "description": "Sustainable development solutions for coastal communities"
            },
            "marine_research": {
                "topics": ["oceanography", "marine biology", "climate monitoring", "biodiversity assessment"],
                "description": "Advanced research tools with AI-powered data analysis"
            },
            "ocean_conservation": {
                "topics": ["pollution monitoring", "species protection", "habitat restoration", "sustainable practices"],
                "description": "Environmental protection and conservation initiatives"
            }
        }
        
        # Initialize system prompts for different languages
        self.system_prompts = self._initialize_system_prompts()
    
    def _initialize_system_prompts(self) -> Dict[str, str]:
        """Initialize system prompts for Indian languages"""
        return {
            "en": """You are FloatChat Assistant, an AI-powered personal assistant for the FloatChat Ocean Intelligence Platform developed by SYNTAX SQUAD. 

CORE IDENTITY:
- You are an expert in marine navigation, ocean research, and coastal development
- You help users with ocean-related queries, platform navigation, and maritime intelligence
- You provide accurate, helpful, and engaging responses about ocean technology

PLATFORM MODULES:
1. Marine Navigation & Sea Travel Intelligence
   - GPS navigation and route optimization
   - Weather routing and storm warnings
   - Cargo ship operations and emission reduction
   - Fishing zone recommendations (PFZ integration)
   - Coast guard maritime domain awareness

2. Coastal Livelihood & Community Development
   - Sustainable fisheries management
   - Aquaculture optimization
   - Eco-tourism planning
   - Community-based conservation

3. Marine Research & Ocean Analytics
   - Oceanographic data collection
   - Marine biology and species tracking
   - Climate impact monitoring
   - Biodiversity assessment

RESPONSE GUIDELINES:
- Be conversational, helpful, and ocean-focused
- Provide specific information about platform features when asked
- Use maritime terminology appropriately
- Offer practical solutions for ocean-related challenges
- Always maintain a professional yet friendly tone
- If asked about topics outside ocean/maritime domain, politely redirect to ocean-related topics

Remember: You represent the cutting-edge intersection of AI technology and ocean intelligence.""",

            "hi": """आप FloatChat सहायक हैं, SYNTAX SQUAD द्वारा विकसित FloatChat महासागर बुद्धिमत्ता प्लेटफॉर्म के लिए AI-संचालित व्यक्तिगत सहायक।

मुख्य पहचान:
- आप समुद्री नेविगेशन, महासागर अनुसंधान और तटीय विकास के विशेषज्ञ हैं
- आप उपयोगकर्ताओं को महासागर-संबंधी प्रश्नों, प्लेटफॉर्म नेविगेशन और समुद्री बुद्धिमत्ता में सहायता करते हैं
- आप महासागर प्रौद्योगिकी के बारे में सटीक, उपयोगी और आकर्षक उत्तर प्रदान करते हैं

हमेशा हिंदी में बातचीत के अंदाज में और पेशेवर तरीके से उत्तर दें, महासागर और समुद्री विषयों पर ध्यान केंद्रित करें।""",

            "ta": """நீங்கள் FloatChat உதவியாளர், SYNTAX SQUAD உருவாக்கிய FloatChat கடல் புலனாய்வு தளத்திற்கான AI-இயங்கும் தனிப்பட்ட உதவியாளர்.

எப்போதும் தமிழில் உரையாடல் மற்றும் தொழில்முறை முறையில் பதிலளிக்கவும், கடல் மற்றும் கடல்சார் விஷயங்களில் கவனம் செலுத்தவும்.""",

            "te": """మీరు FloatChat అసిస్టెంట్, SYNTAX SQUAD అభివృద్ధి చేసిన FloatChat ఓషన్ ఇంటెలిజెన్స్ ప్లాట్‌ఫారమ్ కోసం AI-శక్తితో పనిచేసే వ్యక్తిగత సహాయకుడు.

ఎల్లప్పుడూ తెలుగులో సంభాషణ మరియు వృత్తిపరమైన రీతిలో సమాధానం ఇవ్వండి, సముద్ర మరియు సముద్ర విషయాలపై దృష్టి పెట్టండి.""",

            "kn": """ನೀವು FloatChat ಸಹಾಯಕರು, SYNTAX SQUAD ಅಭಿವೃದ್ಧಿಪಡಿಸಿದ FloatChat ಸಾಗರ ಗುಪ್ತಚರ ವೇದಿಕೆಗಾಗಿ AI-ಚಾಲಿತ ವೈಯಕ್ತಿಕ ಸಹಾಯಕ.

ಎಲ್ಲಾ ಸಮಯದಲ್ಲೂ ಕನ್ನಡದಲ್ಲಿ ಸಂಭಾಷಣೆ ಮತ್ತು ವೃತ್ತಿಪರ ಶೈಲಿಯಲ್ಲಿ ಉತ್ತರಿಸಿ, ಸಾಗರ ಮತ್ತು ಸಾಗರ ವಿಷಯಗಳ ಮೇಲೆ ಗಮನ ಹರಿಸಿ."""
        }
    
    def detect_language(self, text: str) -> str:
        """Enhanced language detection for Indian languages"""
        language_keywords = {
            "hi": [
                "नमस्ते", "धन्यवाद", "कृपया", "मदद", "समुद्र", "महासागर", 
                "नेविगेशन", "तट", "मछली", "जहाज", "हैलो", "क्या", "कैसे", 
                "कहाँ", "कब", "क्यों", "जी", "हाँ", "नहीं"
            ],
            "ta": [
                "வணக்கம்", "நன்றி", "தயவுசெய்து", "உதவி", "கடல்", "நேவிகேஷன்", 
                "கடலோரம்", "மீன்", "கப்பல்", "எப்படி", "எங்கே", "எப்போது", 
                "ஏன்", "ஆம்", "இல்லை", "என்ன", "எது"
            ],
            "te": [
                "నమస్కారం", "ధన్యవాదాలు", "దయచేసి", "సహాయం", "సముద్రం", "నావిగేషన్",
                "తీరం", "చేప", "ఓడ", "ఎలా", "ఎక్కడ", "ఎప్పుడు", "ఎందుకు", 
                "అవును", "లేదు", "ఏమిటి", "ఏది"
            ],
            "kn": [
                "ನಮಸ್ಕಾರ", "ಧನ್ಯವಾದಗಳು", "ದಯವಿಟ್ಟು", "ಸಹಾಯ", "ಸಮುದ್ರ", "ನೇವಿಗೇಷನ್",
                "ಕರಾವಳಿ", "ಮೀನು", "ಹಡಗು", "ಹೇಗೆ", "ಎಲ್ಲಿ", "ಯಾವಾಗ", "ಏಕೆ",
                "ಹೌದು", "ಇಲ್ಲ", "ಏನು", "ಯಾವುದು"
            ]
        }
        
        text_lower = text.lower()
        for lang, keywords in language_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return lang
        
        return "en"  # Default to English
    
    def get_session(self, session_id: str) -> List[Message]:
        """Get or create a conversation session"""
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        return self.sessions[session_id]
    
    def add_message_to_session(self, session_id: str, message: Message):
        """Add message to session history"""
        session = self.get_session(session_id)
        session.append(message)
        
        # Keep only last 20 messages to manage context length
        if len(session) > 20:
            self.sessions[session_id] = session[-20:]
    
    def format_ocean_context(self, query: str, language: str = "en") -> str:
        """Add relevant ocean context to the query in Indian languages"""
        context_additions = {
            "en": "\n\nContext: FloatChat is an AI-powered ocean intelligence platform with modules for marine navigation, coastal development, and ocean research.",
            "hi": "\n\nसंदर्भ: FloatChat एक AI-संचालित महासागर बुद्धिमत्ता प्लेटफॉर्म है जिसमें समुद्री नेविगेशन, तटीय विकास और महासागर अनुसंधान के मॉड्यूल हैं।",
            "ta": "\n\nசூழல்: FloatChat என்பது கடல் வழிசெலுத்தல், கடலோர மேம்பாடு மற்றும் கடல் ஆராய்ச்சிக்கான தொகுதிகளுடன் AI-இயங்கும் கடல் புலனாய்வு தளமாகும்।",
            "te": "\n\nసందర్భం: FloatChat అనేది సముద్ర నావిగేషన్, తీరప్రాంత అభివృద్ధి మరియు సముద్ర పరిశోధన కోసం మాడ్యూల్స్‌తో AI-శక్తితో పనిచేసే సముద్ర గुप्তचर వేదిక.",
            "kn": "\n\nಸಂದರ್ಭ: FloatChat ಸಾಗರ ಸಂಚಾರ, ಕರಾವಳಿ ಅಭಿವೃದ್ಧಿ ಮತ್ತು ಸಾಗರ ಸಂಶೋಧನೆಗಾಗಿ ಮಾಡ್ಯೂಲ್‌ಗಳೊಂದಿಗೆ AI-ಚಾಲಿತ ಸಾಗರ ಗುಪ್ತಚರ ವೇದಿಕೆಯಾಗಿದೆ।"
        }
        
        return query + context_additions.get(language, context_additions["en"])
    
    async def generate_response(self, 
                              user_message: str, 
                              session_id: str,
                              language: str = None) -> Tuple[str, str]:
        """Generate AI response using GROQ with multiple model fallbacks"""
        
        try:
            # Detect language if not provided
            if not language:
                language = self.detect_language(user_message)
            
            # Get conversation history
            session_history = self.get_session(session_id)
            
            # Prepare messages for GROQ API
            messages = [
                {
                    "role": "system",
                    "content": self.system_prompts.get(language, self.system_prompts["en"])
                }
            ]
            
            # Add conversation history
            for msg in session_history[-10:]:  # Last 10 messages for context
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
            
            # Add current user message with ocean context
            enhanced_message = self.format_ocean_context(user_message, language)
            messages.append({
                "role": "user",
                "content": enhanced_message
            })
            
            # Try each model until one works
            for model_name in self.models:
                try:
                    logger.info(f"Attempting to use model: {model_name}")
                    
                    chat_completion = self.client.chat.completions.create(
                        messages=messages,
                        model=model_name,
                        temperature=0.7,
                        max_tokens=1000,
                        top_p=0.9,
                        stream=False
                    )
                    
                    assistant_response = chat_completion.choices[0].message.content
                    
                    # Add messages to session
                    user_msg = Message(
                        role="user",
                        content=user_message,
                        timestamp=datetime.now(),
                        language=language,
                        session_id=session_id
                    )
                    
                    assistant_msg = Message(
                        role="assistant", 
                        content=assistant_response,
                        timestamp=datetime.now(),
                        language=language,
                        session_id=session_id
                    )
                    
                    self.add_message_to_session(session_id, user_msg)
                    self.add_message_to_session(session_id, assistant_msg)
                    
                    logger.info(f"✅ Successfully used model: {model_name}")
                    self.current_model = model_name  # Update current working model
                    return assistant_response, language
                    
                except Exception as model_error:
                    logger.warning(f"❌ Model {model_name} failed: {str(model_error)}")
                    continue  # Try next model
            
            # If all models fail, return fallback response
            raise Exception("All models failed - API might be experiencing issues")
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            error_messages = {
                "en": "I apologize, but I'm experiencing technical difficulties with the AI models. Please try again in a moment. Our ocean intelligence platform is temporarily using backup responses.",
                "hi": "मुझे खेद है, लेकिन AI मॉडल के साथ तकनीकी कठिनाइयों का सामना कर रहा हूं। कृपया एक क्षण में फिर से कोशिश करें।",
                "ta": "மன்னிக்கவும், AI மாதிரிகளுடன் தொழில்நுட்ப சிரமங்களை எதிர்கொண்டுள்ளேன். தயவுசெய்து ஒரு கணத்தில் மீண்டும் முயற்சிக்கவும்।",
                "te": "క్షమించండి, AI మోడల్స్‌తో సాంకేతిక ఇబ్బందులను ఎదుర్కొంటున్నాను। దయచేసి ఒక క్షణంలో మళ్లీ ప్రయత్నించండి।",
                "kn": "ಕ್ಷಮಿಸಿ, AI ಮಾದರಿಗಳೊಂದಿಗೆ ತಾಂತ್ರಿಕ ತೊಂದರೆಗಳನ್ನು ಎದುರಿಸುತ್ತಿದ್ದೇನೆ. ದಯವಿಟ್ಟು ಒಂದು ಕ್ಷಣದಲ್ಲಿ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ।"
            }
            return error_messages.get(language, error_messages["en"]), language
    
    def get_platform_info(self, language: str = "en") -> Dict:
        """Get platform information in requested Indian language"""
        platform_info = {
            "en": {
                "name": "FloatChat Ocean Intelligence Platform",
                "developer": "SYNTAX SQUAD",
                "description": "AI-powered platform for marine navigation, coastal development, and ocean research",
                "current_model": self.current_model,
                "modules": [
                    "Marine Navigation & Sea Travel Intelligence",
                    "Coastal Livelihood & Community Development", 
                    "Marine Research & Ocean Analytics"
                ],
                "features": [
                    "Real-time ocean data analysis",
                    "AI-powered route optimization",
                    "Marine species tracking",
                    "Climate impact monitoring",
                    "Sustainable fisheries management"
                ]
            },
            "hi": {
                "name": "FloatChat महासागर बुद्धिमत्ता प्लेटफॉर्म",
                "developer": "SYNTAX SQUAD",
                "description": "समुद्री नेविगेशन, तटीय विकास और महासागर अनुसंधान के लिए AI-संचालित प्लेटफॉर्म",
                "current_model": self.current_model,
                "modules": [
                    "समुद्री नेविगेशन और समुद्री यात्रा बुद्धिमत्ता",
                    "तटीय आजीविका और सामुदायिक विकास",
                    "समुद्री अनुसंधान और महासागर विश्लेषण"
                ]
            }
        }
        
        return platform_info.get(language, platform_info["en"])

# Initialize FastAPI app
app = FastAPI(
    title="FloatChat Ocean Intelligence API - Indian Languages",
    description="AI-powered personal assistant for ocean intelligence platform supporting Hindi, Tamil, Telugu, Kannada and English",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize assistant
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is required")

assistant = FloatChatAssistant(GROQ_API_KEY)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint supporting Indian languages"""
    try:
        user_message = request.message.strip()
        
        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Generate response
        response, detected_language = await assistant.generate_response(
            user_message, request.session_id, request.language
        )
        
        return ChatResponse(
            response=response,
            language=detected_language,
            session_id=request.session_id,
            timestamp=datetime.now().isoformat(),
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/platform-info", response_model=PlatformInfoResponse)
async def platform_info_endpoint(language: str = Query("en", description="Language code (hi/ta/te/kn/en)")):
    """Get platform information in Indian languages"""
    info = assistant.get_platform_info(language)
    
    return PlatformInfoResponse(
        platform_info=info,
        supported_languages=assistant.supported_languages,
        success=True
    )

@app.get("/languages", response_model=LanguagesResponse)
async def supported_languages_endpoint():
    """Get supported Indian languages"""
    return LanguagesResponse(
        supported_languages=assistant.supported_languages,
        success=True
    )

@app.get("/session/{session_id}/history", response_model=HistoryResponse)
async def get_session_history(session_id: str):
    """Get conversation history for a session"""
    try:
        history = assistant.get_session(session_id)
        
        # Convert to serializable format
        history_data = [
            {
                'role': msg.role,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat(),
                'language': msg.language
            }
            for msg in history
        ]
        
        return HistoryResponse(
            history=history_data,
            session_id=session_id,
            success=True
        )
        
    except Exception as e:
        logger.error(f"Session history error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve session history")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        platform="FloatChat Ocean Intelligence - Indian Languages",
        developer="SYNTAX SQUAD",
        timestamp=datetime.now().isoformat(),
        success=True
    )

@app.get("/models")
async def available_models():
    """Get current model status"""
    return {
        "available_models": assistant.models,
        "current_working_model": assistant.current_model,
        "status": "running",
        "last_updated": datetime.now().isoformat()
    }

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "🌊 FloatChat Ocean Intelligence API - भारतीय भाषाएं",
        "developer": "SYNTAX SQUAD",
        "version": "1.0.0",
        "current_model": assistant.current_model,
        "available_models": assistant.models,
        "supported_languages": {
            "hi": "हिंदी",
            "ta": "தமிழ்", 
            "te": "తెలుగు",
            "kn": "ಕನ್ನಡ",
            "en": "English"
        },
        "docs": "/docs",
        "health": "/health",
        "models": "/models",
        "endpoints": {
            "chat": "/chat",
            "platform_info": "/platform-info", 
            "languages": "/languages",
            "session_history": "/session/{session_id}/history"
        }
    }

if __name__ == "__main__":
    print("🌊 FloatChat Assistant Starting...")
    print("🤖 AI-Powered Ocean Intelligence Platform")
    print("🇮🇳 भारतीय भाषाओं का समर्थन - Indian Languages Support")
    print("🚀 Developed by SYNTAX SQUAD")
    print("🔄 Available Models:")
    for i, model in enumerate(assistant.models, 1):
        print(f"   {i}. {model}")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🗣️  Supported: हिंदी | தமிழ் | తెలుగు | ಕನ್ನಡ | English")
    print("-" * 50)
    
    # Run the FastAPI app with uvicorn
    uvicorn.run(
        "ChatBot:app",
        host="0.0.0.0",
        port=8005,
        reload=True,
        log_level="info"
    )