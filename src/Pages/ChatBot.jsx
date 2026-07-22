import React, { useState, useRef, useEffect } from 'react';
import { IoSend, IoWater } from "react-icons/io5";
import { FaWater, FaMapMarkerAlt, FaCalendarAlt, FaChartLine, FaGlobe } from "react-icons/fa";
import { MdScience } from "react-icons/md";
import { TbTemperature, TbDroplet, TbRuler } from "react-icons/tb";

const API_BASE_URL = 'http://localhost:8000';

export const ChatBot = () => {
  const [messages, setMessages] = useState([
    {
      type: 'bot',
      content: "🌊 Hello! I'm FloatChat, your AI oceanographer specializing in Indian Ocean ARGO data. Ask me about temperature profiles, salinity patterns, or specific regions like Arabian Sea, Bay of Bengal, or Central Indian Ocean!",
      timestamp: new Date().toISOString()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [apiHealth, setApiHealth] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check API health on component mount
  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      const health = await response.json();
      setApiHealth(health);
    } catch (error) {
      console.error('API Health Check Failed:', error);
      setApiHealth({ status: 'error', error: 'API unavailable' });
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = {
      type: 'user',
      content: input,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: input,
          include_data: true,
          max_profiles: 5
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      
      const botMessage = {
        type: 'bot',
        content: data.response,
        argoData: data.argo_data_summary,
        timestamp: data.query_timestamp
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('API Error:', error);
      const errorMessage = {
        type: 'bot',
        content: `🚨 Sorry, I encountered an error: ${error.message}. Please make sure the ARGO API server is running on localhost:8000.`,
        timestamp: new Date().toISOString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatRegionName = (region) => {
    const regionMap = {
      'Arabian_Sea': 'Arabian Sea',
      'Bay_of_Bengal': 'Bay of Bengal',
      'Central_Indian': 'Central Indian Ocean',
      'Southern_Indian': 'Southern Indian Ocean'
    };
    return regionMap[region] || region;
  };

  const getRegionEmoji = (region) => {
    const emojiMap = {
      'Arabian_Sea': '🏜️',
      'Bay_of_Bengal': '🌀',
      'Central_Indian': '🌊',
      'Southern_Indian': '🧊'
    };
    return emojiMap[region] || '🌊';
  };

  const ArgoDataCard = ({ argoData }) => {
    if (!argoData || argoData.error) return null;

    return (
      <div className="mt-4 bg-gradient-to-br from-cyan-500/20 to-blue-600/20 backdrop-blur-lg rounded-xl p-4 border border-cyan-300/30">
        <div className="flex items-center gap-2 mb-3">
          <MdScience className="text-cyan-300 text-lg" />
          <h3 className="text-cyan-200 font-semibold">ARGO Data Context</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3">
          <div className="flex items-center gap-2">
            <FaChartLine className="text-blue-300" />
            <span className="text-white/80">Profiles: </span>
            <span className="text-cyan-300 font-medium">{argoData.profiles_count || 0}</span>
          </div>
          
          {argoData.target_region && (
            <div className="flex items-center gap-2">
              <FaGlobe className="text-green-300" />
              <span className="text-white/80">Region: </span>
              <span className="text-green-300 font-medium">
                {getRegionEmoji(argoData.target_region)} {formatRegionName(argoData.target_region)}
              </span>
            </div>
          )}
        </div>

        {argoData.sample_profiles && argoData.sample_profiles.length > 0 && (
          <div className="space-y-3">
            <h4 className="text-cyan-200 font-medium text-sm">Sample Profiles:</h4>
            <div className="grid gap-3">
              {argoData.sample_profiles.slice(0, 3).map((profile, index) => (
                <div key={index} className="bg-white/10 rounded-lg p-3 border border-white/20">
                  <div className="grid grid-cols-1 lg:grid-cols-3 gap-2 text-sm">
                    <div className="flex items-center gap-1">
                      <FaMapMarkerAlt className="text-orange-300 text-xs" />
                      <span className="text-white/70">Location:</span>
                      <span className="text-orange-300 font-mono text-xs">{profile.location}</span>
                    </div>
                    
                    {profile.surface_temperature && (
                      <div className="flex items-center gap-1">
                        <TbTemperature className="text-red-300 text-xs" />
                        <span className="text-white/70">Temp:</span>
                        <span className="text-red-300 font-medium">{profile.surface_temperature}°C</span>
                      </div>
                    )}
                    
                    {profile.max_depth && (
                      <div className="flex items-center gap-1">
                        <TbRuler className="text-blue-300 text-xs" />
                        <span className="text-white/70">Depth:</span>
                        <span className="text-blue-300 font-medium">{profile.max_depth}m</span>
                      </div>
                    )}
                  </div>
                  
                  <div className="mt-2 flex items-center gap-1">
                    <FaCalendarAlt className="text-purple-300 text-xs" />
                    <span className="text-purple-300 text-xs font-mono">
                      {profile.date ? new Date(profile.date).toLocaleDateString() : 'N/A'}
                    </span>
                    <span className="text-white/50 text-xs ml-2">ID: {profile.id}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  };

  const QuickQuestions = () => {
    const questions = [
      "What are temperature conditions in Arabian Sea?",
      "Show me salinity data from Bay of Bengal",
      "Compare Arabian Sea vs Bay of Bengal conditions",
      "What's the thermocline depth in Central Indian Ocean?"
    ];

    return (
      <div className="mb-4">
        <p className="text-cyan-200 text-sm mb-2">Quick questions to try:</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {questions.map((question, index) => (
            <button
              key={index}
              onClick={() => setInput(question)}
              className="text-left bg-white/10 hover:bg-white/20 backdrop-blur-sm border border-cyan-300/30 rounded-lg p-2 text-sm text-white/80 hover:text-white transition-all duration-200 hover:border-cyan-300/50"
            >
              💡 {question}
            </button>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-cyan-900">
      {/* Animated Ocean Background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute inset-0 opacity-20">
          <div className="h-full w-full bg-gradient-to-t from-blue-600/20 to-transparent"></div>
        </div>
        
        <div className="absolute inset-0">
          {Array.from({ length: 20 }, (_, i) => (
            <div
              key={i}
              className="absolute w-2 h-2 bg-cyan-300/30 rounded-full animate-pulse"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 5}s`,
                animationDuration: `${3 + Math.random() * 4}s`
              }}
            ></div>
          ))}
        </div>
      </div>

      <div className="container mx-auto h-screen max-w-6xl px-4 py-6 relative flex flex-col">
        {/* Header with API Status */}
        <div className="bg-gradient-to-r from-cyan-500/20 to-blue-600/20 backdrop-blur-xl rounded-2xl p-4 border border-cyan-300/30 mb-4 shadow-2xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="relative">
                <FaWater className="text-3xl text-cyan-300 drop-shadow-lg" />
                <div className="absolute inset-0 text-3xl text-cyan-300 animate-pulse opacity-50">
                  <FaWater />
                </div>
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-300 to-blue-300 bg-clip-text text-transparent">
                  FloatChat ARGO
                </h1>
                <p className="text-cyan-200/80 text-sm">Indian Ocean Data Explorer</p>
              </div>
            </div>
            
            {/* API Status */}
            <div className="flex items-center gap-2">
              <div className={`w-3 h-3 rounded-full ${apiHealth?.status === 'healthy' ? 'bg-green-400' : 'bg-red-400'} animate-pulse`}></div>
              <span className="text-white/80 text-sm">
                {apiHealth?.status === 'healthy' ? 'API Connected' : 'API Offline'}
              </span>
              {apiHealth?.llm && (
                <div className={`ml-2 px-2 py-1 rounded-full text-xs ${
                  apiHealth.llm === 'available' ? 'bg-green-500/20 text-green-300' : 'bg-red-500/20 text-red-300'
                }`}>
                  LLM {apiHealth.llm}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Messages Container */}
        <div className="flex-1 bg-black/20 backdrop-blur-sm rounded-2xl border border-white/10 overflow-hidden shadow-2xl">
          <div className="h-full overflow-y-auto p-6 space-y-6 no-scrollbar">
            {messages.length === 1 && <QuickQuestions />}
            
            {messages.map((message, index) => (
              <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'} animate-fadeIn`}>
                <div className={`max-w-[85%] ${message.type === 'user' ? 'order-2' : 'order-1'}`}>
                  <div className={`p-4 rounded-2xl shadow-lg ${
                    message.type === 'user' 
                      ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-tr-sm' 
                      : message.isError
                      ? 'bg-gradient-to-r from-red-500/20 to-red-600/20 text-red-200 border border-red-400/30 rounded-tl-sm'
                      : 'bg-gradient-to-r from-slate-700/50 to-slate-600/50 text-white border border-white/20 rounded-tl-sm backdrop-blur-lg'
                  }`}>
                    <div className="whitespace-pre-wrap leading-relaxed">
                      {message.content}
                    </div>
                    
                    {message.argoData && <ArgoDataCard argoData={message.argoData} />}
                    
                    <div className="flex justify-between items-center mt-2 pt-2 border-t border-white/20">
                      <div className={`text-xs ${message.type === 'user' ? 'text-white/70' : 'text-white/50'}`}>
                        {new Date(message.timestamp).toLocaleTimeString()}
                      </div>
                      {message.type === 'bot' && !message.isError && (
                        <div className="flex items-center gap-1 text-xs text-cyan-300">
                          <MdScience />
                          ARGO AI
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gradient-to-r from-slate-700/50 to-slate-600/50 border border-white/20 backdrop-blur-lg text-white p-4 rounded-2xl rounded-tl-sm max-w-[85%]">
                  <div className="flex items-center gap-2">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-cyan-300 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-cyan-300 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-cyan-300 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                    <span className="text-cyan-200">Analyzing oceanographic data...</span>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <form onSubmit={handleSend} className="mt-4 bg-gradient-to-r from-slate-800/80 to-slate-700/80 backdrop-blur-xl rounded-2xl p-4 border border-white/20 shadow-2xl">
          <div className="flex gap-3">
            <div className="relative flex-1">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about ocean temperatures, salinity, or specific regions..."
                disabled={isLoading}
                className="w-full bg-white/10 text-white placeholder-white/50 rounded-xl px-4 py-3 pl-12 pr-4 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:bg-white/15 transition-all duration-200 border border-white/20"
              />
              <IoWater className="absolute left-4 top-1/2 transform -translate-y-1/2 text-cyan-300" />
            </div>
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 disabled:from-gray-600 disabled:to-gray-700 text-white p-3 rounded-xl transition-all duration-200 shadow-lg hover:shadow-cyan-500/25 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <IoSend size={20} />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};