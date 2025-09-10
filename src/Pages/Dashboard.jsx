import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import water from '../Assets/water.mp4'
import { useNavigate } from 'react-router-dom'
import { FaRobot, FaArrowRight, FaWater, FaFish, FaLeaf, FaBookOpen, FaEnvelope , FaAnchor , FaCompass , FaShip , FaShieldAlt , FaSearch, FaCubes, FaMap, FaBell, FaInfoCircle, FaHome, FaUsers, FaHeart, FaGlobe, FaLightbulb, FaLinkedin, FaTwitter, FaGithub, FaPhone, FaMapMarkerAlt } from 'react-icons/fa'
import img1 from '../assets/FloatChat.png'
import navigationImg from '../assets/Navigatiion.jpg'
import livelihoodImg from '../assets/Livelihood.jpg'
import researchImg from '../assets/Research.jpg'
export const Dashboard = () => {
  const navigate = useNavigate();
  const [scrolled, setScrolled] = useState(false);
  const [showModulesDropdown, setShowModulesDropdown] = useState(false);

  const handleAsk = () => {
    navigate('/chatbot');
  }

  const handleModuleNavigation = (moduleId) => {
    const element = document.getElementById(moduleId);
    if (element) {
      const offsetTop = element.offsetTop - 100; // Account for fixed navbar
      window.scrollTo({
        top: offsetTop,
        behavior: 'smooth'
      });
    }
    setShowModulesDropdown(false); // Close dropdown after navigation
  }

  const handleNavigation = (href) => {
    if (href === '#about') {
      const element = document.getElementById('about');
      if (element) {
        const offsetTop = element.offsetTop - 100; // Account for fixed navbar
        window.scrollTo({
          top: offsetTop,
          behavior: 'smooth'
        });
      }
    } else {
      // Handle other navigation items if needed
      const element = document.querySelector(href);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
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

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (showModulesDropdown && !event.target.closest('.modules-dropdown')) {
        setShowModulesDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showModulesDropdown]);

  const navItems = [
    { name: 'Home', href: '#home', icon: FaHome },
    { name: 'Modules', href: '#modules', icon: FaCubes },
    { name: 'Map', href: '#map', icon: FaMap },
    { name: 'Notification', href: '#notification', icon: FaBell },
    { name: 'About Us', href: '#about', icon: FaInfoCircle },
  ];

  return (
    <>

    <div className="no-scrollbar">

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
        <div className="max-w-7xl mx-auto px-2 sm:px-4 lg:px-6">
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
                  className="relative"
                >
                  {item.name === 'Modules' ? (
                    // Modules Dropdown
                    <div className="relative modules-dropdown">
                      <motion.button
                        onClick={() => setShowModulesDropdown(!showModulesDropdown)}
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
                        
                        {/* Dropdown Arrow */}
                        <motion.div
                          animate={{ rotate: showModulesDropdown ? 180 : 0 }}
                          transition={{ duration: 0.3 }}
                        >
                          <svg className="w-3 h-3 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                          </svg>
                        </motion.div>
                        
                        {/* Enhanced Hover Effect */}
                        <motion.div
                          className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                        />
                      </motion.button>

                      {/* Dropdown Menu */}
                      {showModulesDropdown && (
                        <motion.div
                          initial={{ opacity: 0, y: 10, scale: 0.95 }}
                          animate={{ opacity: 1, y: 0, scale: 1 }}
                          exit={{ opacity: 0, y: 10, scale: 0.95 }}
                          className="absolute top-full mt-2 left-0 w-56 bg-slate-800/95 backdrop-blur-md rounded-xl shadow-xl border border-slate-700/50 overflow-hidden z-50"
                        >
                          <div className="py-2">
                            <button
                              onClick={() => handleModuleNavigation('marine-navigation')}
                              className="w-full flex items-center space-x-3 px-4 py-3 text-sm text-slate-300 hover:text-white hover:bg-slate-700/50 transition-colors duration-200"
                            >
                              <FaAnchor className="text-cyan-400" />
                              <span>Marine Navigation</span>
                            </button>
                            <button
                              onClick={() => handleModuleNavigation('coastal-livelihood')}
                              className="w-full flex items-center space-x-3 px-4 py-3 text-sm text-slate-300 hover:text-white hover:bg-slate-700/50 transition-colors duration-200"
                            >
                              <FaFish className="text-blue-400" />
                              <span>Coastal Livelihood</span>
                            </button>
                            <button
                              onClick={() => handleModuleNavigation('research')}
                              className="w-full flex items-center space-x-3 px-4 py-3 text-sm text-slate-300 hover:text-white hover:bg-slate-700/50 transition-colors duration-200"
                            >
                              <FaSearch className="text-purple-400" />
                              <span>Marine Research</span>
                            </button>
                          </div>
                        </motion.div>
                      )}
                    </div>
                  ) : item.name === 'Home' ? (
                    // Home Button - Special scroll to top behavior
                    <motion.button
                      onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
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
                    </motion.button>
                  ) : (
                    // Regular Navigation Items
                    <motion.button
                      onClick={() => handleNavigation(item.href)}
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
                    </motion.button>
                  )}
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
        <div className="absolute top-0 left-0 w-full h-full flex flex-col items-center justify-center z-10 px-2">
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

     {/* Modules Section */}
      <div className='w-full bg-gradient-to-b from-slate-900 to-slate-800 px-2 py-20'>
        
        {/* Section Header */}
        <div className="max-w-6xl mx-auto text-center mb-16">
          <h2 className="text-5xl font-bold text-white mb-6">Ocean Intelligence Modules</h2>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto">
            Comprehensive AI-powered solutions for marine navigation, coastal development, and ocean research
          </p>
        </div>

        {/* Marine Navigation Module - Background Image Design */}
        <section id="marine-navigation" className="mb-24">
          <div className="max-w-7xl mx-auto px-6">
            <motion.div 
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="relative rounded-3xl overflow-hidden min-h-[600px] flex items-center shadow-[0_25px_50px_-12px_rgba(0,0,0,0.5)] hover:shadow-[0_35px_60px_-12px_rgba(6,182,212,0.4)] transition-all duration-500"
              style={{
                filter: 'drop-shadow(0 25px 50px rgba(0, 0, 0, 0.3))',
              }}
            >
              {/* Background Image */}
              <div 
                className="absolute inset-0 bg-cover bg-center bg-no-repeat"
                style={{ backgroundImage: `url(${navigationImg})` }}
              />
              
              {/* Overlay */}
              <div className="absolute inset-0 bg-gradient-to-r from-slate-900/90 via-slate-900/70 to-slate-900/40" />
              
              {/* Content */}
              <div className="relative z-10 w-full max-w-2xl p-12 lg:p-16">
                <motion.div
                  initial={{ opacity: 0, x: -50 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.6, delay: 0.2 }}
                >
                  <div 
                    className="inline-flex items-center justify-center w-20 h-20 bg-cyan-500/20 backdrop-blur-md rounded-2xl mb-8 border border-cyan-400/30"
                    style={{
                      boxShadow: '0 10px 25px -5px rgba(6, 182, 212, 0.3), 0 4px 15px -3px rgba(0, 0, 0, 0.2)',
                      filter: 'drop-shadow(0 4px 8px rgba(6, 182, 212, 0.2))',
                    }}
                  >
                    <FaAnchor className="text-3xl text-cyan-400" />
                  </div>
                  
                  <h2 className="text-5xl lg:text-6xl font-bold text-white mb-6 leading-tight">
                    Marine
                    <span className="block text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-400">
                      Navigation
                    </span>
                  </h2>
                  
                  <p className="text-xl text-slate-200 mb-10 leading-relaxed max-w-lg">
                    AI-powered maritime intelligence for smart navigation, weather integration, and real-time sea route optimization.
                  </p>
                  
                  <motion.button
                    onClick={() => navigate('/marine-navigation')}
                    className="group relative inline-flex items-center px-10 py-5 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-bold text-lg rounded-2xl transition-all duration-300 overflow-hidden"
                    style={{
                      boxShadow: '0 20px 40px -12px rgba(6, 182, 212, 0.4), 0 8px 25px -8px rgba(0, 0, 0, 0.3)',
                      filter: 'drop-shadow(0 8px 16px rgba(6, 182, 212, 0.3))',
                    }}
                    whileHover={{ 
                      scale: 1.05, 
                      y: -2,
                      boxShadow: '0 25px 50px -12px rgba(6, 182, 212, 0.6), 0 12px 30px -8px rgba(0, 0, 0, 0.4)',
                      filter: 'drop-shadow(0 12px 24px rgba(6, 182, 212, 0.5))',
                    }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <span className="relative z-10 flex items-center">
                      Explore Navigation
                      <FaArrowRight className="ml-4 group-hover:translate-x-2 transition-transform duration-300" />
                    </span>
                    <div className="absolute inset-0 bg-gradient-to-r from-cyan-600 to-blue-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                  </motion.button>
                </motion.div>
              </div>
            
            </motion.div>
          </div>
        </section>

        {/* Coastal Livelihood Module - Background Design */}
        <section id="coastal-livelihood" className="mb-24">
          <div className="max-w-7xl mx-auto px-6">
            <motion.div 
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="relative rounded-3xl overflow-hidden min-h-[600px] flex items-center shadow-[0_25px_50px_-12px_rgba(0,0,0,0.5)] hover:shadow-[0_35px_60px_-12px_rgba(59,130,246,0.4)] transition-all duration-500"
              style={{
                filter: 'drop-shadow(0 25px 50px rgba(0, 0, 0, 0.3))',
              }}
            >
              {/* Background Image  */}
              <div 
                className="absolute inset-0 bg-cover bg-center bg-no-repeat"
                style={{ backgroundImage: `url(${livelihoodImg})` }}
              />
              
              {/* Overlay */}
              <div className="absolute inset-0 bg-gradient-to-r from-slate-900/30 via-slate-900/55 to-slate-900/70" />
              
              {/* Content positioned on the right */}
              <div className="relative z-10 w-full max-w-2xl ml-auto p-12 lg:p-16">
                <motion.div
                  initial={{ opacity: 0, x: 50 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.6, delay: 0.2 }}
                >
                  <div 
                    className="inline-flex items-center justify-center w-20 h-20 bg-blue-500/20 backdrop-blur-md rounded-2xl mb-8 border border-blue-400/30"
                    style={{
                      boxShadow: '0 10px 25px -5px rgba(59, 130, 246, 0.3), 0 4px 15px -3px rgba(0, 0, 0, 0.2)',
                      filter: 'drop-shadow(0 4px 8px rgba(59, 130, 246, 0.2))',
                    }}
                  >
                    <FaFish className="text-3xl text-blue-400" />
                  </div>
                  
                  <h2 className="text-5xl lg:text-6xl font-bold text-white mb-6 leading-tight">
                    Coastal
                    <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">
                      Livelihood
                    </span>
                  </h2>
                  
                  <p className="text-xl text-slate-200 mb-10 leading-relaxed max-w-lg">
                    Sustainable development solutions for coastal communities. Smart aquaculture, eco-tourism, and resource management.
                  </p>
                  
                  <motion.button
                    onClick={() => navigate('/coastal-livelihood')}
                    className="group relative inline-flex items-center px-10 py-5 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold text-lg rounded-2xl transition-all duration-300 overflow-hidden"
                    style={{
                      boxShadow: '0 20px 40px -12px rgba(59, 130, 246, 0.4), 0 8px 25px -8px rgba(0, 0, 0, 0.3)',
                      filter: 'drop-shadow(0 8px 16px rgba(59, 130, 246, 0.3))',
                    }}
                    whileHover={{ 
                      scale: 1.05, 
                      y: -2,
                      boxShadow: '0 25px 50px -12px rgba(59, 130, 246, 0.6), 0 12px 30px -8px rgba(0, 0, 0, 0.4)',
                      filter: 'drop-shadow(0 12px 24px rgba(59, 130, 246, 0.5))',
                    }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <span className="relative z-10 flex items-center">
                      Explore Livelihood
                      <FaArrowRight className="ml-4 group-hover:translate-x-2 transition-transform duration-300" />
                    </span>
                    <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                  </motion.button>
                </motion.div>
              </div>
              
        
            </motion.div>
          </div>
        </section>

        {/* Marine Research Module - Background Image Design */}
        <section id="research" className="mb-24">
          <div className="max-w-7xl mx-auto px-6">
            <motion.div 
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="relative rounded-3xl overflow-hidden min-h-[600px] flex items-center shadow-[0_25px_50px_-12px_rgba(0,0,0,0.5)] hover:shadow-[0_35px_60px_-12px_rgba(147,51,234,0.4)] transition-all duration-500"
              style={{
                filter: 'drop-shadow(0 25px 50px rgba(0, 0, 0, 0.3))',
              }}
            >
              {/* Background Image */}
              <div 
                className="absolute inset-0 bg-cover bg-center bg-no-repeat"
                style={{ backgroundImage: `url(${researchImg})` }}
              />
              
              {/* Overlay */}
              <div className="absolute inset-0 bg-gradient-to-r from-slate-900/70 via-slate-900/50 to-slate-900/40" />
              
              {/* Content */}
              <div className="relative z-10 w-full max-w-2xl p-12 lg:p-16">
                <motion.div
                  initial={{ opacity: 0, x: -50 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.6, delay: 0.2 }}
                >
                  <div 
                    className="inline-flex items-center justify-center w-20 h-20 bg-purple-500/20 backdrop-blur-md rounded-2xl mb-8 border border-purple-400/30"
                    style={{
                      boxShadow: '0 10px 25px -5px rgba(147, 51, 234, 0.3), 0 4px 15px -3px rgba(0, 0, 0, 0.2)',
                      filter: 'drop-shadow(0 4px 8px rgba(147, 51, 234, 0.2))',
                    }}
                  >
                    <FaSearch className="text-3xl text-purple-400" />
                  </div>
                  
                  <h2 className="text-5xl lg:text-6xl font-bold text-white mb-6 leading-tight">
                    Marine
                    <span className="block text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-indigo-400">
                      Research
                    </span>
                  </h2>
                  
                  <p className="text-xl text-slate-200 mb-10 leading-relaxed max-w-lg">
                    Advanced oceanographic research with AI-powered analytics. Climate monitoring, biodiversity tracking, and scientific discovery.
                  </p>
                  
                  <motion.button
                    onClick={() => navigate('/marine-research')}
                    className="group relative inline-flex items-center px-10 py-5 bg-gradient-to-r from-purple-500 to-indigo-600 text-white font-bold text-lg rounded-2xl transition-all duration-300 overflow-hidden"
                    style={{
                      boxShadow: '0 20px 40px -12px rgba(147, 51, 234, 0.4), 0 8px 25px -8px rgba(0, 0, 0, 0.3)',
                      filter: 'drop-shadow(0 8px 16px rgba(147, 51, 234, 0.3))',
                    }}
                    whileHover={{ 
                      scale: 1.05, 
                      y: -2,
                      boxShadow: '0 25px 50px -12px rgba(147, 51, 234, 0.6), 0 12px 30px -8px rgba(0, 0, 0, 0.4)',
                      filter: 'drop-shadow(0 12px 24px rgba(147, 51, 234, 0.5))',
                    }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <span className="relative z-10 flex items-center">
                      Explore Research
                      <FaArrowRight className="ml-4 group-hover:translate-x-2 transition-transform duration-300" />
                    </span>
                    <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-indigo-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                  </motion.button>
                </motion.div>
              </div>
              
            </motion.div>
          </div>
        </section>

       
      </div>

      {/* Simple About Us Section */}
      <section id="about" className="w-full bg-gradient-to-b from-slate-800 to-slate-900 py-16">
        <div className="max-w-4xl mx-auto px-6">
          
          {/* Header */}
          <motion.div 
            className="text-center mb-12"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="inline-flex items-center justify-center w-16 h-16 bg-cyan-500/20 backdrop-blur-md rounded-2xl mb-6 border border-cyan-400/30">
              <FaInfoCircle className="text-2xl text-cyan-400" />
            </div>
            <h2 className="text-4xl font-bold text-white mb-4">About FloatChat</h2>
            <p className="text-lg text-slate-300 max-w-2xl mx-auto">
              AI-powered ocean intelligence platform for marine navigation, coastal development, and research
            </p>
          </motion.div>

          {/* Contact Information */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="bg-slate-800/50 backdrop-blur-md rounded-2xl p-8 border border-slate-700/50"
          >
            <div className="grid md:grid-cols-2 gap-8">
              
              {/* Contact Details */}
              <div>
                <h3 className="text-2xl font-bold text-white mb-6">Contact Us</h3>
                <div className="space-y-4">
                  <div className="flex items-center space-x-4">
                    <div className="w-10 h-10 bg-cyan-500/20 rounded-full flex items-center justify-center">
                      <FaEnvelope className="text-cyan-400" />
                    </div>
                    <div>
                      <p className="text-slate-300 text-sm">Email</p>
                      <p className="text-white font-medium">contact@floatchat.com</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-4">
                    <div className="w-10 h-10 bg-blue-500/20 rounded-full flex items-center justify-center">
                      <FaPhone className="text-blue-400" />
                    </div>
                    <div>
                      <p className="text-slate-300 text-sm">Phone</p>
                      <p className="text-white font-medium">+1 (555) 123-4567</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-4">
                    <div className="w-10 h-10 bg-purple-500/20 rounded-full flex items-center justify-center">
                      <FaMapMarkerAlt className="text-purple-400" />
                    </div>
                    <div>
                      <p className="text-slate-300 text-sm">Address</p>
                      <p className="text-white font-medium">Ocean Tech Hub, Marine Drive</p>
                      <p className="text-slate-300 text-sm">San Francisco, CA 94102</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Quick Info */}
              <div>
                <h3 className="text-2xl font-bold text-white mb-6">Quick Info</h3>
                <div className="space-y-4">
                  <div>
                    <p className="text-slate-300 text-sm">Founded</p>
                    <p className="text-white font-medium">2024</p>
                  </div>
                  
                  <div>
                    <p className="text-slate-300 text-sm">Industry</p>
                    <p className="text-white font-medium">Marine Technology & AI</p>
                  </div>
                  
                  <div>
                    <p className="text-slate-300 text-sm">Services</p>
                    <p className="text-white font-medium">Ocean Intelligence Solutions</p>
                  </div>
                  
                  <div>
                    <p className="text-slate-300 text-sm">Support Hours</p>
                    <p className="text-white font-medium">24/7 Available</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Social Links */}
            <div className="mt-8 pt-6 border-t border-slate-700/50">
              <div className="flex justify-center space-x-4">
                <a 
                  href="#" 
                  className="w-10 h-10 bg-cyan-500/20 rounded-full flex items-center justify-center hover:bg-cyan-500/30 transition-colors duration-200"
                >
                  <FaLinkedin className="text-cyan-400" />
                </a>
                <a 
                  href="#" 
                  className="w-10 h-10 bg-blue-500/20 rounded-full flex items-center justify-center hover:bg-blue-500/30 transition-colors duration-200"
                >
                  <FaTwitter className="text-blue-400" />
                </a>
                <a 
                  href="#" 
                  className="w-10 h-10 bg-purple-500/20 rounded-full flex items-center justify-center hover:bg-purple-500/30 transition-colors duration-200"
                >
                  <FaGithub className="text-purple-400" />
                </a>
                <a 
                  href="#" 
                  className="w-10 h-10 bg-green-500/20 rounded-full flex items-center justify-center hover:bg-green-500/30 transition-colors duration-200"
                >
                  <FaGlobe className="text-green-400" />
                </a>
              </div>
            </div>
          </motion.div>

          {/* Simple CTA */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="text-center mt-8"
          >
            <motion.button
              onClick={handleAsk}
              className="inline-flex items-center px-8 py-3 bg-gradient-to-r from-cyan-500 to-blue-500 text-white font-medium rounded-full hover:from-cyan-400 hover:to-blue-400 transition-all duration-300"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <FaEnvelope className="mr-2" />
              Get Started
            </motion.button>
          </motion.div>
        </div>
      </section>
      
      </div>
    </>
  )
}

// Enhanced Module Feature Component
const ModuleFeature = ({ icon, title, description, color }) => {
  const colorClasses = {
    cyan: 'text-cyan-400 border-cyan-500/30 hover:border-cyan-400',
    blue: 'text-blue-400 border-blue-500/30 hover:border-blue-400',
    indigo: 'text-indigo-400 border-indigo-500/30 hover:border-indigo-400',
    purple: 'text-purple-400 border-purple-500/30 hover:border-purple-400',
    teal: 'text-teal-400 border-teal-500/30 hover:border-teal-400',
    violet: 'text-violet-400 border-violet-500/30 hover:border-violet-400'
  };

  return (
    <div className={`p-6 rounded-xl bg-slate-800/50 border ${colorClasses[color]} transition-all duration-300 hover:transform hover:scale-105`}>
      <div className={`text-2xl ${colorClasses[color].split(' ')[0]} mb-3`}>
        {icon}
      </div>
      <h4 className="text-lg font-semibold text-white mb-2">{title}</h4>
      <p className="text-slate-400 text-sm leading-relaxed">{description}</p>
    </div>
  );
};

// Quick Access Card Component - FIXED
const QuickAccessCard = ({ icon, title, description, color, onClick }) => {
  const getColorClasses = (color) => {
    switch(color) {
      case 'cyan':
        return {
          background: 'from-cyan-900/50 to-cyan-900/20',
          border: 'border-cyan-500/30 hover:border-cyan-400',
          iconColor: 'text-cyan-400',
          hoverColor: 'hover:text-cyan-300'
        };
      case 'blue':
        return {
          background: 'from-blue-900/50 to-blue-900/20',
          border: 'border-blue-500/30 hover:border-blue-400',
          iconColor: 'text-blue-400',
          hoverColor: 'hover:text-blue-300'
        };
      case 'purple':
        return {
          background: 'from-purple-900/50 to-purple-900/20',
          border: 'border-purple-500/30 hover:border-purple-400',
          iconColor: 'text-purple-400',
          hoverColor: 'hover:text-purple-300'
        };
      default:
        return {
          background: 'from-slate-900/50 to-slate-900/20',
          border: 'border-slate-500/30 hover:border-slate-400',
          iconColor: 'text-slate-400',
          hoverColor: 'hover:text-slate-300'
        };
    }
  };

  const colors = getColorClasses(color);

  return (
    <div 
      className={`text-center p-8 rounded-2xl bg-gradient-to-b ${colors.background} border ${colors.border} transition-all duration-300 hover:transform hover:scale-105 cursor-pointer`} 
      onClick={onClick}
    >
      <div className={`text-4xl ${colors.iconColor} mx-auto mb-4`}>
        {icon}
      </div>
      <h3 className="text-2xl font-bold text-white mb-3">{title}</h3>
      <p className="text-slate-300 mb-4">{description}</p>
      <button className={`${colors.iconColor} ${colors.hoverColor} font-medium transition-colors`}>
        Learn More →
      </button>
    </div>
  );
};