import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import water from '../Assets/water.mp4'
import { useNavigate } from 'react-router-dom'
import { FaRobot, FaArrowRight, FaWater, FaFish, FaLeaf, FaBookOpen, FaEnvelope } from 'react-icons/fa'
import img1 from '../assets/FloatChat.png'
export const Dashboard = () => {
  const navigate = useNavigate();
  const [scrolled, setScrolled] = useState(false);

  const handleAsk = () => {
    navigate('/chatbot');
  }

  // Handle scroll effect for navbar
  useEffect(() => {
    const handleScroll = () => {
      const isScrolled = window.scrollY > 50;
      setScrolled(isScrolled);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navItems = [
    { name: 'About Us', href: '#about', icon: FaWater },
    { name: 'Inhabitants', href: '#inhabitants', icon: FaFish },
    { name: 'Ecosystems', href: '#ecosystems', icon: FaLeaf },
    { name: 'Blogs', href: '#blogs', icon: FaBookOpen },
    { name: 'Contacts', href: '#contacts', icon: FaEnvelope },
  ];

  return (
    <>
      {/* Enhanced Navigation Bar with Fixed Position and Blur Effect */}
      <motion.nav
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
          scrolled 
            ? 'bg-slate-900/20 backdrop-blur-xl border-b border-white/10 shadow-lg shadow-black/5' 
            : 'bg-slate-900/10 backdrop-blur-sm'
        }`}
        style={{
          backdropFilter: scrolled ? 'blur(20px) saturate(180%)' : 'blur(10px)',
          WebkitBackdropFilter: scrolled ? 'blur(20px) saturate(180%)' : 'blur(10px)',
        }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16 lg:h-20">
            
            {/* Enhanced Logo Section */}
            <motion.div 
              className="flex items-center space-x-3 cursor-pointer"
              whileHover={{ scale: 1.05 }}
              transition={{ duration: 0.2 }}
              onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
            >
              <div className="relative">
                {/* Main Logo Icon */}
                <motion.div
                  className="relative z-10"
                  whileHover={{ rotate: 360 }}
                  transition={{ duration: 0.6 }}
                >
                 
                </motion.div>
                
                <img src={img1} alt="Logo" className="w-8 h-8 lg:w-10 lg:h-10 bg-amber-50 " />
                {/* Pulsing Glow Effect */}
                <motion.div
                  className="absolute inset-0 text-2xl lg:text-3xl text-cyan-400"
                  animate={{
                    opacity: [0, 0.3, 0],
                    scale: [1, 1.3, 1],
                  }}
                  transition={{
                    duration: 3,
                    repeat: Infinity,
                    ease: "easeInOut"
                  }}
                >
                  
                </motion.div>
                
                {/* Background Glow */}
                <div className="absolute inset-0 bg-cyan-400/20 rounded-full blur-md transform scale-150 opacity-50"></div>
              </div>
              
              <div className="flex flex-col">
                <h1 className="text-white text-xl lg:text-2xl font-bold font-poppins tracking-tight drop-shadow-lg">
                  FloatChat
                </h1>
                <motion.div
                  className="h-0.5 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: '100%' }}
                  transition={{ duration: 1, delay: 0.5 }}
                />
              </div>
            </motion.div>

            {/* Navigation Menu */}
            <ul className="flex items-center space-x-1">
              {navItems.map((item, index) => (
                <motion.li
                  key={item.name}
                  initial={{ opacity: 0, y: -20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <motion.a
                    href={item.href}
                    className={`group relative flex items-center space-x-2 px-4 py-2 rounded-full transition-all duration-300 font-poppins text-sm font-medium ${
                      scrolled 
                        ? 'text-white/90 hover:text-white hover:bg-white/10' 
                        : 'text-slate-200 hover:text-white hover:bg-white/5'
                    }`}
                    whileHover={{ scale: 1.05, y: -2 }}
                  >
                    {/* Icon with Animation */}
                    <motion.div
                      whileHover={{ rotate: 360, scale: 1.2 }}
                      transition={{ duration: 0.3 }}
                    >
                      <item.icon className="text-sm group-hover:text-cyan-400 transition-colors duration-300" />
                    </motion.div>
                    
                    <span className="relative z-10">{item.name}</span>
                    
                    {/* Enhanced Hover Effect */}
                    <motion.div
                      className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                    />
                    
                    {/* Bottom Indicator */}
                    <motion.div
                      className="absolute -bottom-1 left-1/2 transform -translate-x-1/2 w-1 h-1 bg-cyan-400 rounded-full scale-0 group-hover:scale-100 transition-transform duration-300"
                    />
                  </motion.a>
                </motion.li>
              ))}
            </ul>

            {/* Enhanced CTA Button */}
            <motion.button
              onClick={handleAsk}
              className={`relative inline-flex items-center justify-center px-6 py-2.5 font-poppins text-sm font-medium text-white rounded-full overflow-hidden shadow-lg transition-all duration-300 group ${
                scrolled 
                  ? 'bg-gradient-to-r from-cyan-500/90 to-blue-500/90 hover:from-cyan-400 hover:to-blue-400 shadow-cyan-500/20' 
                  : 'bg-gradient-to-r from-cyan-500/80 to-blue-500/80 hover:from-cyan-500 hover:to-blue-500'
              }`}
              whileHover={{ 
                scale: 1.05,
                boxShadow: '0 10px 25px rgba(6,182,212,0.3)'
              }}
              whileTap={{ scale: 0.95 }}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.8 }}
            >
              {/* Button Background Animation */}
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-blue-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
              />
              
              {/* Button Content */}
              <span className="relative z-10 font-medium">Explore Now</span>
              <motion.div
                className="relative z-10 ml-2"
                animate={{ x: [0, 3, 0] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                <FaArrowRight className="text-xs" />
              </motion.div>
              
              {/* Shine Effect */}
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent skew-x-12 opacity-0 group-hover:opacity-100"
                animate={{
                  x: ['-100%', '100%'],
                }}
                transition={{
                  duration: 0.6,
                  repeat: Infinity,
                  repeatDelay: 2,
                }}
              />
            </motion.button>
          </div>
        </div>
      </motion.nav>

      {/* Hero Section */}
      <div className="relative w-full min-h-screen bg-slate-900">
        {/* Video Background */}
        <video
          className="absolute top-0 left-0 w-full h-full object-cover"
          autoPlay
          loop
          muted
        >
          <source src={water} type="video/mp4" />
        </video>

        {/* Enhanced Gradient Overlay */}
        <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-b from-slate-900/80 via-slate-900/60 to-slate-900/90"></div>
        
        {/* Additional Overlay for Better Text Readability */}
        <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-r from-slate-900/40 via-transparent to-slate-900/40"></div>

        {/* Content Section */}
        <div className="absolute top-0 left-0 w-full h-full flex flex-col items-center justify-center z-10 px-4">
          <motion.div 
            className="space-y-8 text-center max-w-4xl"
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, delay: 0.5 }}
          >
            {/* Main Title */}
            <motion.div 
              className="space-y-4"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, delay: 0.7 }}
            >
              <h1 className="text-white text-4xl md:text-6xl lg:text-7xl font-bold font-poppins tracking-tight leading-tight">
                <motion.span
                  className="block"
                  animate={{
                    textShadow: [
                      '0 0 20px rgba(6,182,212,0.3)',
                      '0 0 40px rgba(6,182,212,0.5)',
                      '0 0 20px rgba(6,182,212,0.3)'
                    ]
                  }}
                  transition={{ duration: 4, repeat: Infinity }}
                >
                  Dive Into the Wonders
                </motion.span>
                <motion.span 
                  className="block bg-gradient-to-r from-cyan-400 via-blue-400 to-cyan-500 bg-clip-text text-transparent"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8, delay: 1 }}
                >
                  of the Ocean
                </motion.span>
              </h1>
            </motion.div>

            {/* Description */}
            <motion.p 
              className="text-slate-300 text-lg md:text-xl lg:text-2xl font-light max-w-3xl mx-auto leading-relaxed"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.9 }}
            >
              Explore vibrant ecosystems, uncover the mysteries of ocean life, and connect 
              with a community passionate about preserving our blue planet
            </motion.p>

            {/* CTA Button */}
            <motion.div 
              className="pt-6"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 1.1 }}
            >
              <motion.button 
                onClick={handleAsk}
                className="group relative inline-flex items-center justify-center px-10 py-4 font-poppins text-lg font-medium text-white bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full overflow-hidden shadow-2xl transition-all duration-300"
                whileHover={{ 
                  scale: 1.05,
                  boxShadow: '0 25px 50px rgba(6,182,212,0.25)'
                }}
                whileTap={{ scale: 0.95 }}
              >
                <motion.div
                  className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-blue-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                />
                <span className="relative z-10">Start Exploring</span>
                <motion.div
                  className="relative z-10 ml-3"
                  animate={{ x: [0, 5, 0] }}
                  transition={{ duration: 2, repeat: Infinity }}
                >
                  <FaArrowRight />
                </motion.div>
              </motion.button>
            </motion.div>
          </motion.div>
        </div>

        {/* Scroll Indicator */}
        <motion.div
          className="absolute bottom-8 left-1/2 transform -translate-x-1/2 z-20"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 1.5 }}
        >
          <motion.div
            className="w-6 h-10 border-2 border-white/50 rounded-full flex justify-center"
            animate={{ opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <motion.div
              className="w-1 h-3 bg-white rounded-full mt-2"
              animate={{ y: [0, 12, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            />
          </motion.div>
        </motion.div>
      </div>
    </>
  )
}


