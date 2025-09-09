import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import FloatChatLogo from '../assets/FloatChat.png';
import SyntaxSquadLogo from '../assets/SyntaxSquad.png';

export const Launch = () => {
  const navigate = useNavigate();
  const [showIntro, setShowIntro] = useState(true);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    // Progress animation - exactly 5 seconds
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          return 100;
        }
        return prev + 2; // 2% every 100ms = 5 seconds total
      });
    }, 100);

    // Auto-navigate after exactly 5 seconds
    const navigationTimer = setTimeout(() => {
      setShowIntro(false);
      setTimeout(() => navigate('/dashboard'), 500);
    }, 5000);

    return () => {
      clearInterval(progressInterval);
      clearTimeout(navigationTimer);
    };
  }, [navigate]);

  return (
    <AnimatePresence>
      {showIntro && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.5 }}
          className="fixed inset-0 bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800 flex items-center justify-center overflow-hidden"
        >
          {/* Premium Background Pattern - Removed whitish backgrounds */}
          <div className="absolute inset-0 opacity-20">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(6,182,212,0.1)_0%,transparent_50%)]"></div>
            <div className="absolute inset-0 bg-[conic-gradient(from_0deg_at_50%_50%,rgba(6,182,212,0.1)_0deg,transparent_60deg,rgba(59,130,246,0.1)_120deg,transparent_180deg)]"></div>
          </div>

          {/* Floating Particles */}
          <div className="absolute inset-0 overflow-hidden">
            {[...Array(15)].map((_, i) => (
              <motion.div
                key={i}
                className="absolute w-1 h-1 bg-cyan-400/30 rounded-full"
                animate={{
                  y: [-100, window.innerHeight + 100],
                  x: [Math.random() * window.innerWidth, Math.random() * window.innerWidth],
                  opacity: [0, 0.6, 0],
                }}
                transition={{
                  duration: 6 + Math.random() * 3,
                  repeat: Infinity,
                  delay: Math.random() * 5,
                  ease: "linear"
                }}
                style={{
                  left: `${Math.random() * 100}%`,
                  top: '-10px',
                }}
              />
            ))}
          </div>

          {/* Main Content Container */}
          <div className="relative z-10 text-center h-full flex flex-col justify-between py-16">
            
            {/* Top Section - Logos and Title */}
            <div className="flex-1 flex flex-col justify-center">
              
              {/* Dual Logo Section - Enhanced Visibility */}
              <motion.div
                initial={{ scale: 0.8, opacity: 0, y: 30 }}
                animate={{ scale: 1, opacity: 1, y: 0 }}
                transition={{ duration: 1, ease: "easeOut" }}
                className="mb-8"
              >
                <div className="flex items-center justify-center gap-12 mb-4">
                  {/* FloatChat Logo */}
                  <motion.div 
                    className="relative"
                    whileHover={{ scale: 1.05 }}
                    transition={{ duration: 0.3 }}
                  >
                    {/* Enhanced Background */}
                    <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 rounded-2xl blur-2xl scale-150 animate-pulse"></div>
                    <div className="absolute inset-0 bg-slate-800/80 backdrop-blur-sm rounded-2xl border border-cyan-500/30 shadow-2xl shadow-cyan-500/20"></div>
                    
                    {/* Logo Container */}
                    <div className="relative p-6 rounded-2xl bg-gradient-to-br from-slate-800/90 to-slate-900/90 border border-cyan-400/20 backdrop-blur-sm">
                      <img
                        src={FloatChatLogo}
                        alt="FloatChat Logo"
                        className="w-24 h-24 md:w-32 md:h-32 lg:w-40 lg:h-40 filter brightness-125 contrast-110 drop-shadow-2xl relative z-10"
                      />
                      
                      {/* Glow Effect */}
                      <div className="absolute inset-0 bg-gradient-to-r from-cyan-400/10 to-blue-400/10 rounded-2xl animate-pulse"></div>
                    </div>
                    
                    {/* Label */}
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 1.2 }}
                      className="text-center mt-3"
                    >
                      <p className="text-sm text-cyan-300 font-poppins font-medium">FloatChat</p>
                    </motion.div>
                  </motion.div>

                  {/* Enhanced Separator */}
                  <div className="flex flex-col items-center">
                    <div className="w-0.5 h-20 md:h-24 bg-gradient-to-b from-transparent via-cyan-400/60 to-transparent"></div>
                    <div className="w-8 h-0.5 bg-gradient-to-r from-transparent via-cyan-400/60 to-transparent my-2"></div>
                    <div className="w-0.5 h-20 md:h-24 bg-gradient-to-b from-transparent via-blue-400/60 to-transparent"></div>
                  </div>

                  {/* SyntaxSquad Logo */}
                  <motion.div 
                    className="relative"
                    whileHover={{ scale: 1.05 }}
                    transition={{ duration: 0.3 }}
                  >
                    {/* Enhanced Background */}
                    <div className="absolute inset-0 bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-2xl blur-2xl scale-150 animate-pulse"></div>
                    <div className="absolute inset-0 bg-slate-800/80 backdrop-blur-sm rounded-2xl border border-blue-500/30 shadow-2xl shadow-blue-500/20"></div>
                    
                    {/* Logo Container */}
                    <div className="relative p-6 rounded-2xl bg-gradient-to-br from-slate-800/90 to-slate-900/90 border border-blue-400/20 backdrop-blur-sm">
                      <img
                        src={SyntaxSquadLogo}
                        alt="SyntaxSquad Logo"
                        className="w-24 h-24 md:w-32 md:h-32 lg:w-40 lg:h-40 filter brightness-125 contrast-110 drop-shadow-2xl relative z-10"
                      />
                      
                      {/* Glow Effect */}
                      <div className="absolute inset-0 bg-gradient-to-r from-blue-400/10 to-purple-400/10 rounded-2xl animate-pulse"></div>
                    </div>
                    
                    {/* Label */}
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 1.6, duration:1 }}
                      className="text-center mt-3"
                    >
                      <p className="text-sm text-blue-300 font-poppins font-medium">Syntax Squad</p>
                    </motion.div>
                  </motion.div>
                </div>
                
                {/* Partnership  Text */}
                <motion.div
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 1.6, duration: 1 }}
                  className="text-center mt-6"
                >
                 
                  <div className="w-16 h-0.5 bg-gradient-to-r from-transparent via-slate-400/50 to-transparent mx-auto mt-2"></div>
                </motion.div>
              </motion.div>

              {/* Brand Name - Crystal Clear */}
              <motion.div
                initial={{ y: 50, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 1, delay: 0.3, ease: "easeOut" }}
                className="mb-6"
              >
                <h1 className="text-6xl md:text-7xl lg:text-8xl font-bold font-poppins tracking-tight">
                  <span className="bg-gradient-to-r from-white via-cyan-100 to-blue-100 bg-clip-text text-transparent drop-shadow-[0_2px_10px_rgba(6,182,212,0.3)]">
                    FloatChat
                  </span>
                </h1>
                
                {/* Elegant Underline */}
                <motion.div
                  initial={{ scaleX: 0 }}
                  animate={{ scaleX: 1 }}
                  transition={{ duration: 0.8, delay: 0.8 }}
                  className="w-32 h-0.5 bg-gradient-to-r from-cyan-400 to-blue-400 mx-auto mt-4 rounded-full"
                />
              </motion.div>

              {/* Tagline */}
              <motion.div
                initial={{ y: 30, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.8, delay: 0.6 }}
                className="mb-8"
              >
                <p className="text-xl md:text-2xl text-slate-300 font-light font-poppins max-w-2xl mx-auto">
                  AI-Powered Ocean Data Discovery
                </p>
                <p className="text-lg text-cyan-400/80 font-poppins mt-2">
                  & Visualization Platform
                </p>
                <p className="text-sm text-slate-400/80 font-poppins mt-3">
                  Developed by SYNTAX SQUAD
                </p>
              </motion.div>
            </div>

            {/* Bottom Section - Progress Bar */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ duration: 0.6, delay: 1 }}
              className="w-full max-w-md mx-auto"
            >
              <div className="relative">
                {/* Progress Track */}
                <div className="w-full h-1 bg-slate-700/50 rounded-full backdrop-blur-sm border border-slate-600/30 overflow-hidden">
                  {/* Progress Fill */}
                  <motion.div
                    className="h-full bg-gradient-to-r from-cyan-400 via-blue-400 to-cyan-500 rounded-full relative"
                    style={{ width: `${progress}%` }}
                    transition={{ duration: 0.1 }}
                  >
                    {/* Shine Effect */}
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent rounded-full"></div>
                  </motion.div>
                </div>
                
                {/* Progress Info */}
                <div className="flex justify-between items-center mt-3">
                  <motion.span 
                    className="text-sm text-slate-400 font-poppins"
                    animate={{ opacity: [0.5, 1, 0.5] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    Loading Experience
                  </motion.span>
                  <span className="text-sm text-cyan-400 font-poppins font-medium">
                    {progress}%
                  </span>
                </div>
              </div>

              {/* Version Info */}
              <div className="mt-6">
                <p className="text-xs text-slate-500 font-poppins tracking-wider text-center">
                  Version 1.0 • Powered by SYNTAX SQUAD
                </p>
              </div>
            </motion.div>
          </div>

          {/* Elegant Corner Accents */}
          <div className="absolute top-8 left-8 w-16 h-16 border-l-2 border-t-2 border-cyan-500/30 rounded-tl-lg"></div>
          <div className="absolute top-8 right-8 w-16 h-16 border-r-2 border-t-2 border-cyan-500/30 rounded-tr-lg"></div>
          <div className="absolute bottom-8 left-8 w-16 h-16 border-l-2 border-b-2 border-cyan-500/30 rounded-bl-lg"></div>
          <div className="absolute bottom-8 right-8 w-16 h-16 border-r-2 border-b-2 border-cyan-500/30 rounded-br-lg"></div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
