import React, { useState } from 'react';
import { IoSend } from "react-icons/io5";
import { FaWater } from "react-icons/fa";

export const ChatBot = () => {
  const [messages, setMessages] = useState([
    {
      type: 'bot',
      content: "Hello! I'm OceanBot. Ask me anything about marine life, ocean data, or marine ecosystems!"
    }
  ]);
  const [input, setInput] = useState('');

  const handleSend = (e) => {
    e.preventDefault();
    if (input.trim()) {
      setMessages([...messages, 
        { type: 'user', content: input },
        { type: 'bot', content: 'Processing your ocean-related query...' }
      ]);
      setInput('');
    }
  };

  return (
    <div className="relative h-screen bg-gradient-to-b from-blue-900 via-blue-600 to-blue-400">
      {/* Wave Animation */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute bottom-0 left-0 right-0 h-20 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNDQwIDMyMCI+PHBhdGggZmlsbD0icmdiYSgyNTUsMjU1LDI1NSwwLjEpIiBkPSJNMCwyMDBzNTQ4LjMtMTQwLDcyMCwwLDE0NDAsMCwxNDQwLDBWMEgwWiIvPjwvc3ZnPg==')] animate-wave"></div>
      </div>

      {/* Chat Container */}
      <div className="container mx-auto h-full max-w-4xl px-4 py-8 relative">
        {/* Header */}
        <div className="bg-white/10 backdrop-blur-lg rounded-t-2xl p-4 border-b border-white/20">
          <div className="flex items-center gap-3">
            <FaWater className="text-2xl text-cyan-300" />
            <h1 className="text-white text-xl font-semibold">OceanBot</h1>
          </div>
        </div>

        {/* Messages Area */}
        <div className="bg-white/5 backdrop-blur-sm h-[calc(100vh-12rem)] overflow-y-auto p-4 space-y-4">
          {messages.map((message, index) => (
            <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[80%] p-3 rounded-2xl ${
                message.type === 'user' 
                  ? 'bg-cyan-500 text-white rounded-tr-none' 
                  : 'bg-white/10 text-white rounded-tl-none'
              }`}>
                {message.content}
              </div>
            </div>
          ))}
        </div>

        {/* Input Area */}
        <form onSubmit={handleSend} className="bg-white/10 backdrop-blur-lg rounded-b-2xl p-4 border-t border-white/20">
          <div className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about the ocean..."
              className="flex-1 bg-white/5 text-white placeholder-white/50 rounded-xl px-4 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-400"
            />
            <button
              type="submit"
              className="bg-cyan-500 hover:bg-cyan-600 text-white p-2 rounded-xl transition-colors"
            >
              <IoSend size={24} />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
