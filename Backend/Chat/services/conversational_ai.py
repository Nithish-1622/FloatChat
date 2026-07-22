"""
Conversational AI Service for ARGO Data Analysis
Simple, working version with Groq API integration
"""
import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import os
from dataclasses import dataclass
from enum import Enum
import hashlib

# LLM and API imports
try:
    from groq import AsyncGroq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    AsyncGroq = None

logger = logging.getLogger(__name__)

class ConversationType(Enum):
    """Types of conversations supported"""
    GENERAL_INQUIRY = "general_inquiry"
    DATA_ANALYSIS = "data_analysis" 
    SCIENTIFIC_RESEARCH = "scientific_research"
    EDUCATION = "education"
    TECHNICAL_SUPPORT = "technical_support"

@dataclass
class ConversationContext:
    """Represents the context of an ongoing conversation"""
    session_id: str
    user_id: Optional[str]
    conversation_type: ConversationType
    start_time: datetime
    last_activity: datetime
    message_count: int
    conversation_history: List[Dict[str, Any]]
    context_data: Dict[str, Any]
    metadata: Dict[str, Any]

class ArgoConversationalAI:
    """
    Comprehensive Conversational AI System for ARGO Data
    Simple, working implementation with Groq API integration
    """
    
    def __init__(
        self, 
        groq_api_key: Optional[str] = None,
        vector_db: Optional[Any] = None,
        model_name: str = "llama-3.1-70b-versatile",
        temperature: float = 0.1,
        max_tokens: int = 4000,
        context_window: int = 8000
    ):
        """Initialize the Conversational AI system"""
        # Initialize Groq client
        self.groq_api_key = groq_api_key or os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            logger.warning("Groq API key not found. LLM functionality will be limited.")
            self.groq_client = None
        else:
            try:
                self.groq_client = AsyncGroq(api_key=self.groq_api_key)
                logger.info("Groq client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
                self.groq_client = None
        
        # Initialize vector database
        self.vector_db = vector_db
        
        # Conversation management
        self.active_sessions = {}  # session_id -> ConversationContext
        self.session_timeout = timedelta(hours=2)
        
        # LLM configuration
        self.llm_config = {
            'model': model_name,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'context_window': context_window
        }
        
        # System prompts for different conversation types
        self.system_prompts = {
            'general_inquiry': """You are FloatChat, an AI assistant specialized in ARGO oceanographic data analysis. 
            You provide helpful, accurate information about ARGO floats, oceanographic measurements, and marine science. 
            Be conversational, educational, and precise in your responses.""",
            
            'data_analysis': """You are FloatChat, an expert oceanographic data analyst. Help users understand patterns, 
            trends, and insights from ARGO float data. Provide scientific interpretations of temperature, salinity, 
            and pressure measurements. Use technical language when appropriate but explain complex concepts clearly.""",
            
            'scientific_research': """You are FloatChat, a scientific research assistant specializing in physical oceanography. 
            Help researchers analyze ARGO data for publications, hypothesis testing, and discovery. Provide detailed 
            scientific analysis, cite relevant oceanographic principles, and suggest research methodologies.""",
            
            'education': """You are FloatChat, an educational AI focused on teaching about oceanography and ARGO floats. 
            Explain concepts at an appropriate level, use analogies, and encourage learning. Make complex ocean science 
            accessible and engaging for students and curious learners.""",
            
            'technical_support': """You are FloatChat, a technical support assistant for ARGO data systems. 
            Help users with data access, processing workflows, quality control procedures, and technical issues. 
            Provide step-by-step guidance and troubleshooting assistance."""
        }
        
        logger.info("ArgoConversationalAI initialized successfully")
    
    async def process_query(
        self,
        query: str,
        session_id: Optional[str] = None,
        conversation_type: str = "general_inquiry",
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a user query and return a comprehensive response
        
        Args:
            query: User's question or message
            session_id: Unique session identifier for conversation continuity
            conversation_type: Type of conversation (general, analysis, research, etc.)
            context: Additional context data
            user_id: User identifier
        
        Returns:
            Dict containing response, session info, and metadata
        """
        start_time = datetime.utcnow()
        
        try:
            # Generate session ID if not provided
            if not session_id:
                session_id = self._generate_session_id(query)
            
            # Get or create conversation context
            context_obj = self._get_or_create_context(
                session_id, user_id, conversation_type, context
            )
            
            # Clean up expired sessions
            self._cleanup_expired_sessions()
            
            # Retrieve relevant data using vector database (if available)
            relevant_data = {}
            if self.vector_db:
                try:
                    relevant_data = await self._retrieve_relevant_data(query, conversation_type)
                except Exception as e:
                    logger.warning(f"Vector database retrieval failed: {e}")
            
            # Generate AI response
            response_text = await self._generate_response(
                query, 
                context_obj,
                relevant_data,
                conversation_type
            )
            
            # Update conversation context
            self._update_conversation_context(context_obj, query, response_text)
            
            # Calculate processing time
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return {
                'success': True,
                'session_id': session_id,
                'response': response_text,
                'conversation_type': conversation_type,
                'relevant_profiles_count': len(relevant_data.get('profiles', [])),
                'processing_time': processing_time,
                'metadata': {
                    'message_count': context_obj.message_count,
                    'session_duration': (datetime.utcnow() - context_obj.start_time).total_seconds(),
                    'model_used': self.llm_config['model'],
                    'vector_search_performed': bool(self.vector_db),
                    'context_data_available': bool(relevant_data)
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing user query: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'response': "I apologize, but I encountered an error while processing your query. Please try again.",
                'session_id': session_id or 'error_session'
            }
    
    def _generate_session_id(self, query: str) -> str:
        """Generate unique session ID"""
        timestamp = datetime.utcnow().isoformat()
        combined = f"{timestamp}_{query[:50]}"
        return hashlib.md5(combined.encode()).hexdigest()[:16]
    
    def _get_or_create_context(
        self, 
        session_id: str, 
        user_id: Optional[str], 
        conversation_type: str,
        context: Optional[Dict[str, Any]]
    ) -> ConversationContext:
        """Get existing or create new conversation context"""
        if session_id in self.active_sessions:
            context_obj = self.active_sessions[session_id]
            context_obj.last_activity = datetime.utcnow()
            return context_obj
        
        # Create new context
        context_obj = ConversationContext(
            session_id=session_id,
            user_id=user_id,
            conversation_type=ConversationType(conversation_type),
            start_time=datetime.utcnow(),
            last_activity=datetime.utcnow(),
            message_count=0,
            conversation_history=[],
            context_data=context or {},
            metadata={}
        )
        
        self.active_sessions[session_id] = context_obj
        return context_obj
    
    def _cleanup_expired_sessions(self):
        """Remove expired conversation sessions"""
        current_time = datetime.utcnow()
        expired_sessions = [
            session_id for session_id, context in self.active_sessions.items()
            if current_time - context.last_activity > self.session_timeout
        ]
        
        for session_id in expired_sessions:
            del self.active_sessions[session_id]
            logger.debug(f"Removed expired session: {session_id}")
    
    async def _retrieve_relevant_data(self, query: str, conversation_type: str) -> Dict[str, Any]:
        """Retrieve relevant data from vector database"""
        if not self.vector_db:
            return {}
        
        try:
            # Perform semantic search
            search_results = await self.vector_db.search_similar_profiles(
                query, 
                limit=5,
                conversation_type=conversation_type
            )
            
            return {
                'profiles': search_results.get('results', []),
                'search_query': query,
                'total_matches': search_results.get('total', 0)
            }
        except Exception as e:
            logger.error(f"Error retrieving relevant data: {e}")
            return {}
    
    async def _generate_response(
        self,
        query: str,
        context: ConversationContext,
        relevant_data: Dict[str, Any],
        conversation_type: str
    ) -> str:
        """Generate AI response using Groq"""
        if not self.groq_client:
            return self._generate_mock_response(query, conversation_type)
        
        try:
            # Prepare system prompt
            system_prompt = self.system_prompts.get(
                conversation_type, 
                self.system_prompts['general_inquiry']
            )
            
            # Build context from relevant data
            context_text = self._build_context_text(relevant_data)
            
            # Prepare messages
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add recent conversation history
            for entry in context.conversation_history[-3:]:  # Last 3 exchanges
                messages.append({"role": "user", "content": entry.get("query", "")})
                messages.append({"role": "assistant", "content": entry.get("response", "")})
            
            # Add current query with context
            if context_text:
                enhanced_query = f"Based on this ARGO data:\n\n{context_text}\n\nUser question: {query}"
            else:
                enhanced_query = query
            
            messages.append({"role": "user", "content": enhanced_query})
            
            # Generate response
            completion = await self.groq_client.chat.completions.create(
                model=self.llm_config['model'],
                messages=messages,
                temperature=self.llm_config['temperature'],
                max_tokens=self.llm_config['max_tokens']
            )
            
            return completion.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating Groq response: {e}")
            return self._generate_mock_response(query, conversation_type)
    
    def _build_context_text(self, relevant_data: Dict[str, Any]) -> str:
        """Build context text from relevant data"""
        if not relevant_data or not relevant_data.get('profiles'):
            return ""
        
        context_parts = []
        for profile in relevant_data['profiles'][:3]:  # Top 3 relevant profiles
            profile_info = f"Profile {profile.get('profile_id', 'Unknown')}: "
            profile_info += f"Location: {profile.get('latitude', 'N/A')}, {profile.get('longitude', 'N/A')} "
            profile_info += f"Date: {profile.get('date_time', 'N/A')} "
            
            if 'measurements' in profile:
                measurements = profile['measurements']
                if isinstance(measurements, (list, dict)):
                    profile_info += f"Measurements: {str(measurements)[:200]}..."
            
            context_parts.append(profile_info)
        
        return "\n\n".join(context_parts)
    
    def _update_conversation_context(
        self, 
        context: ConversationContext, 
        query: str, 
        response: str
    ):
        """Update conversation context with new exchange"""
        context.message_count += 1
        context.last_activity = datetime.utcnow()
        
        # Add to conversation history
        context.conversation_history.append({
            'query': query,
            'response': response,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # Keep only recent history to manage memory
        if len(context.conversation_history) > 10:
            context.conversation_history = context.conversation_history[-10:]
    
    def _generate_mock_response(self, query: str, conversation_type: str) -> str:
        """Generate mock response when LLM is not available"""
        mock_responses = {
            'general_inquiry': f"Thank you for your question about ARGO data: '{query}'. I would provide detailed information about oceanographic measurements, but the AI service is currently unavailable.",
            'data_analysis': f"I would analyze the ARGO data patterns related to your query: '{query}', but the AI analysis service is currently unavailable.",
            'scientific_research': f"For your research question: '{query}', I would provide scientific analysis of ARGO measurements, but the AI service is currently unavailable.",
            'education': f"Great question! I would explain the oceanographic concepts related to '{query}' in an educational way, but the AI service is currently unavailable.",
            'technical_support': f"I would help you with the technical issue: '{query}', but the AI support service is currently unavailable."
        }
        
        return mock_responses.get(conversation_type, mock_responses['general_inquiry'])
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a conversation session"""
        if session_id not in self.active_sessions:
            return None
        
        context = self.active_sessions[session_id]
        return {
            'session_id': session_id,
            'user_id': context.user_id,
            'conversation_type': context.conversation_type.value,
            'start_time': context.start_time.isoformat(),
            'last_activity': context.last_activity.isoformat(),
            'message_count': context.message_count,
            'session_duration': (datetime.utcnow() - context.start_time).total_seconds()
        }
    
    def list_active_sessions(self) -> List[Dict[str, Any]]:
        """List all active conversation sessions"""
        return [
            self.get_session_info(session_id) 
            for session_id in self.active_sessions.keys()
        ]
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a conversation session"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            logger.info(f"Deleted session: {session_id}")
            return True
        return False

# Test function
async def test_conversational_ai():
    """Test the conversational AI system"""
    ai = ArgoConversationalAI()
    
    # Test query
    response = await ai.process_query(
        "What is ARGO and how does it work?",
        conversation_type="general_inquiry"
    )
    
    print(f"Response: {response}")

if __name__ == "__main__":
    asyncio.run(test_conversational_ai())