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
          {/* Enhanced Background Patterns */}
          <div className="absolute inset-0 opacity-20">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(6,182,212,0.1)_0%,transparent_50%)]"></div>
            <div className="absolute inset-0 bg-[conic-gradient(from_0deg_at_50%_50%,rgba(6,182,212,0.1)_0deg,transparent_60deg,rgba(59,130,246,0.1)_120deg,transparent_180deg)]"></div>
          </div>

          {/* Animated Geometric Shapes */}
          <div className="absolute inset-0 overflow-hidden">
            {/* Large rotating circles */}
            <motion.div
              className="absolute top-1/4 left-1/4 w-96 h-96 rounded-full border border-cyan-400/10"
              animate={{ rotate: 360 }}
              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
            />
            <motion.div
              className="absolute bottom-1/4 right-1/4 w-80 h-80 rounded-full border border-blue-400/10"
              animate={{ rotate: -360 }}
              transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
            />
            
            {/* Floating hexagons */}
            {[...Array(8)].map((_, i) => (
              <motion.div
                key={`hex-${i}`}
                className="absolute w-12 h-12 border border-cyan-300/20"
                style={{
                  clipPath: 'polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%)',
                  left: `${Math.random() * 100}%`,
                  top: `${Math.random() * 100}%`,
                }}
                animate={{
                  y: [-20, 20, -20],
                  rotate: [0, 180, 360],
                  opacity: [0.2, 0.5, 0.2],
                }}
                transition={{
                  duration: 4 + Math.random() * 2,
                  repeat: Infinity,
                  delay: Math.random() * 2,
                }}
              />
            ))}
          </div>

          {/* Enhanced Floating Particles with Multiple Types */}
          <div className="absolute inset-0 overflow-hidden">
            {/* Small particles */}
            {[...Array(25)].map((_, i) => (
              <motion.div
                key={`particle-${i}`}
                className="absolute w-1 h-1 bg-cyan-400/40 rounded-full"
                animate={{
                  y: [-100, window.innerHeight + 100],
                  x: [
                    Math.random() * window.innerWidth, 
                    Math.random() * window.innerWidth
                  ],
                  opacity: [0, 0.8, 0],
                }}
                transition={{
                  duration: 8 + Math.random() * 4,
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

            {/* Medium bubbles */}
            {[...Array(12)].map((_, i) => (
              <motion.div
                key={`bubble-${i}`}
                className="absolute w-3 h-3 bg-blue-400/20 rounded-full border border-blue-400/30"
                animate={{
                  y: [window.innerHeight + 50, -100],
                  x: [
                    Math.random() * window.innerWidth,
                    Math.random() * window.innerWidth
                  ],
                  scale: [0.5, 1.2, 0.5],
                  opacity: [0, 0.6, 0],
                }}
                transition={{
                  duration: 10 + Math.random() * 5,
                  repeat: Infinity,
                  delay: Math.random() * 8,
                  ease: "easeInOut"
                }}
                style={{
                  left: `${Math.random() * 100}%`,
                  bottom: '-50px',
                }}
              />
            ))}

            {/* Large orbs */}
            {[...Array(6)].map((_, i) => (
              <motion.div
                key={`orb-${i}`}
                className="absolute w-8 h-8 bg-gradient-to-br from-cyan-400/10 to-blue-400/10 rounded-full blur-sm"
                animate={{
                  x: [0, 100, -50, 0],
                  y: [0, -80, 40, 0],
                  scale: [1, 1.5, 0.8, 1],
                  opacity: [0.3, 0.6, 0.2, 0.3],
                }}
                transition={{
                  duration: 15 + Math.random() * 5,
                  repeat: Infinity,
                  delay: Math.random() * 10,
                }}
                style={{
                  left: `${Math.random() * 100}%`,
                  top: `${Math.random() * 100}%`,
                }}
              />
            ))}
          </div>

          {/* Flowing Wave Animation */}
          <div className="absolute inset-0 overflow-hidden opacity-30">
            <motion.div
              className="absolute w-full h-full"
              animate={{
                backgroundPosition: ['0% 0%', '100% 100%'],
              }}
              transition={{
                duration: 20,
                repeat: Infinity,
                ease: "linear"
              }}
              style={{
                background: `
                  radial-gradient(circle at 20% 80%, rgba(6,182,212,0.1) 0%, transparent 50%),
                  radial-gradient(circle at 80% 20%, rgba(59,130,246,0.1) 0%, transparent 50%),
                  radial-gradient(circle at 40% 40%, rgba(167,243,208,0.05) 0%, transparent 50%)
                `,
                backgroundSize: '200% 200%',
              }}
            />
          </div>

          {/* Pulsing Grid Lines */}
          <div className="absolute inset-0 overflow-hidden opacity-10">
            <motion.div
              className="absolute inset-0"
              animate={{
                opacity: [0.05, 0.15, 0.05],
              }}
              transition={{
                duration: 4,
                repeat: Infinity,
                ease: "easeInOut"
              }}
              style={{
                backgroundImage: `
                  linear-gradient(rgba(6,182,212,0.5) 1px, transparent 1px),
                  linear-gradient(90deg, rgba(6,182,212,0.5) 1px, transparent 1px)
                `,
                backgroundSize: '100px 100px',
              }}
            />
          </div>

          {/* Shooting Stars */}
          <div className="absolute inset-0 overflow-hidden">
            {[...Array(4)].map((_, i) => (
              <motion.div
                key={`star-${i}`}
                className="absolute w-1 h-20 bg-gradient-to-b from-cyan-400/80 via-cyan-400/40 to-transparent"
                style={{
                  left: `${Math.random() * 100}%`,
                  top: `${Math.random() * 50}%`,
                  transform: 'rotate(45deg)',
                }}
                animate={{
                  x: [-100, window.innerWidth + 100],
                  opacity: [0, 1, 0],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  delay: i * 3 + Math.random() * 2,
                  ease: "easeOut"
                }}
              />
            ))}
          </div>

          {/* DNA Helix Animation */}
          <div className="absolute inset-0 overflow-hidden opacity-20">
            <motion.div
              className="absolute top-1/2 left-1/2 w-2 h-full origin-center"
              animate={{ rotate: 360 }}
              transition={{ duration: 30, repeat: Infinity, ease: "linear" }}
              style={{ transform: 'translate(-50%, -50%)' }}
            >
              {[...Array(20)].map((_, i) => (
                <div
                  key={`dna-${i}`}
                  className="absolute w-1 h-1 bg-cyan-400/30 rounded-full"
                  style={{
                    left: Math.sin((i * Math.PI) / 10) * 150 + 'px',
                    top: i * 30 + 'px',
                  }}
                />
              ))}
            </motion.div>
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
                <div className="flex items-center justify-center gap-8 mb-4">
                  {/* FloatChat Logo - Enhanced Visibility */}
                  <motion.div 
                    className="relative"
                    animate={{ 
                      y: [0, -10, 0],
                      boxShadow: [
                        '0 0 20px rgba(6,182,212,0.3)',
                        '0 0 40px rgba(6,182,212,0.5)',
                        '0 0 20px rgba(6,182,212,0.3)'
                      ]
                    }}
                    transition={{ duration: 3, repeat: Infinity }}
                  >
                    {/* Background container for better visibility */}
                    <div className="absolute inset-0 bg-black/15 backdrop-blur-sm rounded-2xl border border-white/20 shadow-2xl scale-110"></div>
                    <div className="relative bg-black/10 backdrop-blur-md rounded-2xl p-4 border border-cyan-300/30">
                      <img
                        src={FloatChatLogo}
                        alt="FloatChat Logo"
                        className="w-20 h-20 md:w-28 md:h-28 lg:w-32 lg:h-32 filter brightness-150 contrast-125 saturate-110 drop-shadow-2xl relative z-10"
                      />
                    </div>
                  </motion.div>

                  {/* Enhanced Separator with Animation */}
                  <motion.div 
                    className="relative"
                    animate={{ 
                      scaleY: [1, 1.2, 1],
                      opacity: [0.7, 1, 0.7]
                    }}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    <div className="w-0.5 h-16 md:h-20 bg-gradient-to-b from-transparent via-cyan-300/70 to-transparent"></div>
                    <motion.div 
                      className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-2 h-2 bg-cyan-400 rounded-full shadow-lg"
                      animate={{ 
                        scale: [1, 1.5, 1],
                        boxShadow: [
                          '0 0 10px rgba(6,182,212,0.5)',
                          '0 0 20px rgba(6,182,212,0.8)',
                          '0 0 10px rgba(6,182,212,0.5)'
                        ]
                      }}
                      transition={{ duration: 2, repeat: Infinity }}
                    />
                  </motion.div>

                  {/* SyntaxSquad Logo - Enhanced Visibility */}
                  <motion.div 
                    className="relative"
                    animate={{ 
                      y: [0, -10, 0],
                      boxShadow: [
                        '0 0 20px rgba(147,51,234,0.3)',
                        '0 0 40px rgba(147,51,234,0.5)',
                        '0 0 20px rgba(147,51,234,0.3)'
                      ]
                    }}
                    transition={{ duration: 3, repeat: Infinity, delay: 1.5 }}
                  >
                    {/* Background container for better visibility */}
                    <div className="absolute inset-0 bg-black/15 backdrop-blur-sm rounded-2xl border border-white/20 shadow-2xl scale-110"></div>
                    <div className="relative bg-black/10 backdrop-blur-md rounded-2xl p-4 border border-purple-300/30">
                      <img
                        src={SyntaxSquadLogo}
                        alt="SyntaxSquad Logo"
                        className="w-20 h-20 md:w-28 md:h-28 lg:w-32 lg:h-32 filter brightness-150 contrast-125 saturate-110 drop-shadow-2xl relative z-10"
                      />
                    </div>
                  </motion.div>
                </div>
              </motion.div>

              {/* Brand Name - Crystal Clear with Text Animation */}
              <motion.div
                initial={{ y: 50, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 1, delay: 0.3, ease: "easeOut" }}
                className="mb-6"
              >
                <motion.h1 
                  className="text-6xl md:text-7xl lg:text-8xl font-bold font-poppins tracking-tight"
                  animate={{
                    textShadow: [
                      '0 0 20px rgba(6,182,212,0.3)',
                      '0 0 40px rgba(6,182,212,0.6)',
                      '0 0 20px rgba(6,182,212,0.3)'
                    ]
                  }}
                  transition={{ duration: 4, repeat: Infinity }}
                >
                  <span className="bg-gradient-to-r from-white via-cyan-100 to-blue-100 bg-clip-text text-transparent drop-shadow-[0_2px_10px_rgba(6,182,212,0.3)]">
                    FloatChat
                  </span>
                </motion.h1>
                
                {/* Elegant Underline with Animation */}
                <motion.div
                  initial={{ scaleX: 0 }}
                  animate={{ scaleX: 1 }}
                  transition={{ duration: 0.8, delay: 0.8 }}
                  className="relative w-32 h-0.5 mx-auto mt-4 rounded-full overflow-hidden"
                >
                  <motion.div
                    className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-blue-400"
                    animate={{
                      x: ['-100%', '100%'],
                    }}
                    transition={{
                      duration: 3,
                      repeat: Infinity,
                      ease: "easeInOut"
                    }}
                  />
                </motion.div>
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

            {/* Bottom Section - Enhanced Progress Bar */}
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
                    {/* Enhanced Shine Effect */}
                    <motion.div 
                      className="absolute inset-0 bg-gradient-to-r from-transparent via-white/50 to-transparent rounded-full"
                      animate={{
                        x: ['-100%', '200%'],
                      }}
                      transition={{
                        duration: 2,
                        repeat: Infinity,
                        ease: "easeInOut"
                      }}
                    />
                  </motion.div>
                </div>
                
                {/* Progress Info */}
                <div className="flex justify-between items-center mt-3">
                  <motion.span 
                    className="text-sm text-slate-400 font-poppins"
                    animate={{ 
                      opacity: [0.5, 1, 0.5],
                      color: ['rgb(148, 163, 184)', 'rgb(103, 232, 249)', 'rgb(148, 163, 184)']
                    }}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    Loading Experience
                  </motion.span>
                  <motion.span 
                    className="text-sm text-cyan-400 font-poppins font-medium"
                    animate={{ 
                      scale: progress > 50 ? [1, 1.1, 1] : 1
                    }}
                    transition={{ duration: 0.5 }}
                  >
                    {progress}%
                  </motion.span>
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

          {/* Enhanced Corner Accents with Animation */}
          {[
            { position: 'top-8 left-8', rotation: 0 },
            { position: 'top-8 right-8', rotation: 90 },
            { position: 'bottom-8 left-8', rotation: 270 },
            { position: 'bottom-8 right-8', rotation: 180 }
          ].map((corner, index) => (
            <motion.div
              key={index}
              className={`absolute ${corner.position} w-16 h-16`}
              style={{ rotate: corner.rotation }}
              animate={{
                opacity: [0.3, 0.8, 0.3],
                scale: [1, 1.1, 1],
              }}
              transition={{
                duration: 3,
                repeat: Infinity,
                delay: index * 0.5,
              }}
            >
              <div className="w-full h-full border-l-2 border-t-2 border-cyan-500/30 rounded-tl-lg" />
            </motion.div>
          ))}
        </motion.div>
      )}
    </AnimatePresence>
  );
};
