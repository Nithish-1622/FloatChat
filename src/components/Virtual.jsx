import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  FaRobot, 
  FaTimes, 
  FaPaperPlane, 
  FaMicrophone, 
  FaLanguage,
  FaMinus,
  FaExpand,
  FaTrash,
  FaDownload
} from 'react-icons/fa';
import img1 from '../assets/FloatChat.png';

const Virtual = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [sessionId] = useState(() => `session_${Date.now()}`);
  const [isTyping, setIsTyping] = useState(false);
  const [supportedLanguages, setSupportedLanguages] = useState({});
  
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // API Base URL
  const API_BASE_URL = 'http://localhost:8000';

  // Supported languages with native names
  const languageOptions = {
    'en': 'English',
    'hi': 'हिंदी (Hindi)',
    'ta': 'தமிழ் (Tamil)',
    'te': 'తెలుగు (Telugu)',
    'kn': 'ಕನ್ನಡ (Kannada)'
  };

  // Initialize with welcome message
  useEffect(() => {
    const welcomeMessages = {
      'en': "🌊 Hello! I'm FloatChat Assistant. I'm here to help you with ocean intelligence, marine navigation, and coastal development. How can I assist you today?",
      'hi': "🌊 नमस्ते! मैं FloatChat सहायक हूं। मैं आपको महासागर बुद्धिमत्ता, समुद्री नेविगेशन और तटीय विकास में मदद करने के लिए यहां हूं। आज मैं आपकी कैसे सहायता कर सकता हूं?",
      'ta': "🌊 வணக்கம்! நான் FloatChat உதவியாளர். கடல் புலனாய்வு, கடல் வழிசெலுத்தல் மற்றும் கடலோர மேம்பாட்டில் உங்களுக்கு உதவ நான் இங்கே இருக்கிறேன். இன்று நான் உங்களுக்கு எப்படி உதவ முடியும்?",
      'te': "🌊 నమస్కారం! నేను FloatChat సహాయకుడిని. సముద్ర గుప్తచర, సముద్ర నావిగేషన్ మరియు తీరప్రాంత అభివృద్ధిలో మీకు సహాయం చేయడానికి నేను ఇక్కడ ఉన్నాను. ఈరోజు నేను మీకు ఎలా సహాయం చేయగలను?",
      'kn': "🌊 ನಮಸ್ಕಾರ! ನಾನು FloatChat ಸಹಾಯಕ. ಸಾಗರ ಗುಪ್ತಚರ, ಸಾಗರ ಸಂಚಾರ ಮತ್ತು ಕರಾವಳಿ ಅಭಿವೃದ್ಧಿಯಲ್ಲಿ ನಿಮಗೆ ಸಹಾಯ ಮಾಡಲು ನಾನು ಇಲ್ಲಿದ್ದೇನೆ. ಇಂದು ನಾನು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?"
    };

    if (messages.length === 0) {
      setMessages([{
        id: Date.now(),
        text: welcomeMessages[selectedLanguage] || welcomeMessages['en'],
        sender: 'bot',
        timestamp: new Date(),
        language: selectedLanguage
      }]);
    }
  }, [selectedLanguage]);

  // Fetch supported languages on component mount
  useEffect(() => {
    fetchSupportedLanguages();
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchSupportedLanguages = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/languages`);
      const data = await response.json();
      if (data.success) {
        setSupportedLanguages(data.supported_languages);
      }
    } catch (error) {
      console.error('Error fetching languages:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date(),
      language: selectedLanguage
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setIsTyping(true);

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          session_id: sessionId,
          language: selectedLanguage
        })
      });

      const data = await response.json();

      if (data.success) {
        const botMessage = {
          id: Date.now() + 1,
          text: data.response,
          sender: 'bot',
          timestamp: new Date(),
          language: data.language
        };

        // Simulate typing delay
        setTimeout(() => {
          setMessages(prev => [...prev, botMessage]);
          setIsTyping(false);
          setIsLoading(false);
        }, 1000);
      } else {
        throw new Error(data.error || 'Failed to send message');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      
      const errorMessage = {
        id: Date.now() + 1,
        text: "I apologize, but I'm having trouble connecting to the server. Please try again in a moment.",
        sender: 'bot',
        timestamp: new Date(),
        language: selectedLanguage,
        isError: true
      };

      setTimeout(() => {
        setMessages(prev => [...prev, errorMessage]);
        setIsTyping(false);
        setIsLoading(false);
      }, 1000);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([{
      id: Date.now(),
      text: "🌊 Chat cleared! How can I help you with ocean intelligence today?",
      sender: 'bot',
      timestamp: new Date(),
      language: selectedLanguage
    }]);
  };

  const exportChat = () => {
    const chatData = messages.map(msg => ({
      timestamp: msg.timestamp.toISOString(),
      sender: msg.sender,
      message: msg.text,
      language: msg.language
    }));

    const blob = new Blob([JSON.stringify(chatData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `floatchat-conversation-${sessionId}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const formatTime = (date) => {
    return new Intl.DateTimeFormat('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    }).format(date);
  };

  return (
    <>
      {/* Floating Chat Button */}
      <AnimatePresence>
        {!isOpen && (
          <motion.button
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            exit={{ scale: 0, rotate: 180 }}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => setIsOpen(true)}
            className="fixed bottom-24 right-6 w-16 h-16 bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-full shadow-2xl hover:shadow-cyan-500/25 transition-all duration-300 z-50 flex items-center justify-center group"
          >
            <FaRobot className="text-2xl group-hover:scale-110 transition-transform" />
            
            {/* Notification Badge */}
            <motion.div
              className="absolute -top-2 -right-2 w-6 h-6 bg-red-500 rounded-full flex items-center justify-center text-xs font-bold"
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              AI
            </motion.div>

            {/* Pulse Animation */}
            <motion.div
              className="absolute inset-0 bg-cyan-400/30 rounded-full"
              animate={{
                scale: [1, 1.5, 1],
                opacity: [0.3, 0, 0.3],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
              }}
            />
          </motion.button>
        )}
      </AnimatePresence>

      {/* Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ x: 400, y: 100, opacity: 0 }}
            animate={{ 
              x: 0, 
              y: 0, 
              opacity: 1,
              height: isMinimized ? '60px' : '600px'
            }}
            exit={{ x: 400, y: 100, opacity: 0 }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="fixed bottom-6 right-6 w-96 bg-slate-900/95 backdrop-blur-xl rounded-2xl shadow-2xl border border-slate-700/50 z-50 overflow-hidden"
          >
            {/* Chat Header */}
            <div className="flex items-center justify-between p-4 bg-gradient-to-r from-cyan-600 to-blue-600 text-white">
              <div className="flex items-center space-x-3">
                <img src={img1} alt="FloatChat" className="w-8 h-8 rounded-full" />
                <div>
                  <h3 className="font-semibold text-sm">FloatChat Assistant</h3>
                  <p className="text-xs text-cyan-100">Ocean Intelligence AI</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                {/* Language Selector */}
                <select
                  value={selectedLanguage}
                  onChange={(e) => setSelectedLanguage(e.target.value)}
                  className="bg-white/20 text-white text-xs rounded px-2 py-1 border-none outline-none"
                >
                  {Object.entries(languageOptions).map(([code, name]) => (
                    <option key={code} value={code} className="bg-slate-800 text-white">
                      {name}
                    </option>
                  ))}
                </select>

                {/* Control Buttons */}
                <button
                  onClick={() => setIsMinimized(!isMinimized)}
                  className="p-1 hover:bg-white/20 rounded transition-colors"
                >
                  {isMinimized ? <FaExpand className="text-xs" /> : <FaMinus className="text-xs" />}
                </button>
                
                <button
                  onClick={clearChat}
                  className="p-1 hover:bg-white/20 rounded transition-colors"
                  title="Clear Chat"
                >
                  <FaTrash className="text-xs" />
                </button>
                
                <button
                  onClick={exportChat}
                  className="p-1 hover:bg-white/20 rounded transition-colors"
                  title="Export Chat"
                >
                  <FaDownload className="text-xs" />
                </button>
                
                <button
                  onClick={() => setIsOpen(false)}
                  className="p-1 hover:bg-white/20 rounded transition-colors"
                >
                  <FaTimes className="text-xs" />
                </button>
              </div>
            </div>

            {/* Chat Messages */}
            {!isMinimized && (
              <div className="h-96 overflow-y-auto p-4 space-y-4 scrollbar-thin scrollbar-thumb-slate-600 scrollbar-track-slate-800">
                {messages.map((message) => (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-2xl ${
                      message.sender === 'user'
                        ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white'
                        : message.isError
                        ? 'bg-red-900/50 text-red-200 border border-red-500/30'
                        : 'bg-slate-800 text-slate-200 border border-slate-700/50'
                    }`}>
                      <p className="text-sm whitespace-pre-wrap">{message.text}</p>
                      <p className={`text-xs mt-1 ${
                        message.sender === 'user' ? 'text-cyan-100' : 'text-slate-500'
                      }`}>
                        {formatTime(message.timestamp)}
                      </p>
                    </div>
                  </motion.div>
                ))}

                {/* Typing Indicator */}
                {isTyping && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex justify-start"
                  >
                    <div className="bg-slate-800 text-slate-200 px-4 py-2 rounded-2xl border border-slate-700/50">
                      <div className="flex space-x-1">
                        <motion.div
                          className="w-2 h-2 bg-cyan-400 rounded-full"
                          animate={{ y: [0, -5, 0] }}
                          transition={{ duration: 0.6, repeat: Infinity, delay: 0 }}
                        />
                        <motion.div
                          className="w-2 h-2 bg-cyan-400 rounded-full"
                          animate={{ y: [0, -5, 0] }}
                          transition={{ duration: 0.6, repeat: Infinity, delay: 0.2 }}
                        />
                        <motion.div
                          className="w-2 h-2 bg-cyan-400 rounded-full"
                          animate={{ y: [0, -5, 0] }}
                          transition={{ duration: 0.6, repeat: Infinity, delay: 0.4 }}
                        />
                      </div>
                    </div>
                  </motion.div>
                )}
                
                <div ref={messagesEndRef} />
              </div>
            )}

            {/* Chat Input */}
            {!isMinimized && (
              <div className="p-4 border-t border-slate-700/50 bg-slate-800/50">
                <div className="flex items-center space-x-2">
                  <div className="flex-1 relative">
                    <textarea
                      ref={inputRef}
                      value={inputMessage}
                      onChange={(e) => setInputMessage(e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder={
                        selectedLanguage === 'hi' ? 'अपना संदेश लिखें...' :
                        selectedLanguage === 'ta' ? 'உங்கள் செய்தியை எழுதுங்கள்...' :
                        selectedLanguage === 'te' ? 'మీ సందేశాన్ని రాయండి...' :
                        selectedLanguage === 'kn' ? 'ನಿಮ್ಮ ಸಂದೇಶವನ್ನು ಬರೆಯಿರಿ...' :
                        'Type your message...'
                      }
                      className="w-full bg-slate-700/50 text-white placeholder-slate-400 rounded-xl px-4 py-2 text-sm border border-slate-600/50 focus:border-cyan-400 focus:outline-none resize-none max-h-20"
                      rows="1"
                      disabled={isLoading}
                    />
                  </div>
                  
                  <motion.button
                    onClick={sendMessage}
                    disabled={isLoading || !inputMessage.trim()}
                    className="p-2 bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-xl hover:from-cyan-400 hover:to-blue-400 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    {isLoading ? (
                      <motion.div
                        animate={{ rotate: 360 }}
                        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                        className="w-4 h-4 border-2 border-white border-t-transparent rounded-full"
                      />
                    ) : (
                      <FaPaperPlane className="text-sm" />
                    )}
                  </motion.button>
                </div>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default Virtual;