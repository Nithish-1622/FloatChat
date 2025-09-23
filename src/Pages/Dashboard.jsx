import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import water from '../assets/water.mp4'
import { Navigate, useNavigate } from 'react-router-dom'
import { FaRobot, FaArrowRight, FaWater, FaFish, FaLeaf, FaBookOpen, FaEnvelope , FaAnchor , FaCompass , FaShip , FaShieldAlt , FaSearch, FaCubes, FaMap, FaBell, FaInfoCircle, FaHome, FaUsers, FaHeart, FaGlobe, FaLightbulb, FaLinkedin, FaTwitter, FaGithub, FaPhone, FaMapMarkerAlt, FaNewspaper, FaPlus, FaTimes, FaQuestionCircle } from 'react-icons/fa'
import img1 from '../assets/FloatChat.png'
import  Virtual from '../components/Virtual.jsx'
import navigationImg from '../assets/Navigatiion.jpg'
import livelihoodImg from '../assets/Livelihood.jpg'
import researchImg from '../assets/Research.jpg'
export const Dashboard = () => {
  const navigate = useNavigate();
  const [scrolled, setScrolled] = useState(false);
  const [showModulesDropdown, setShowModulesDropdown] = useState(false);
  const [openIndex, setOpenIndex] = useState(null);
  const handleAsk = () => {
    navigate('/chatbot');
  }
  const HanNavigate = () => {
    navigate('/marine-navigation');
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
    } else if (href.startsWith('/')) {
    // Handle route navigation for pages like /news
    navigate(href);
  }else {
      // Handle other navigation items if needed
      const element = document.querySelector(href);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
  }

  const toggleFAQ = (idx) => {
    setOpenIndex(openIndex === idx ? null : idx);
  };

  // FAQ Data for FloatChat
  const faqs = [
    {
      question: "What is FloatChat and how does it work?",
      answer: "FloatChat is an AI-powered ocean intelligence platform that uses real-time oceanographic data from floating sensors to provide insights for marine navigation, research, and coastal development. It combines machine learning with live ocean data to deliver accurate predictions and recommendations."
    },
    {
      question: "How accurate is the marine navigation data?",
      answer: "Our marine navigation system uses data from multiple sources including Argo floats, satellite imagery, and weather stations to provide highly accurate real-time conditions. The AI algorithms continuously learn and improve, achieving over 95% accuracy in weather and current predictions."
    },
    {
      question: "Can FloatChat help with coastal livelihood planning?",
      answer: "Yes! FloatChat provides comprehensive coastal analysis including water quality monitoring, fish population tracking, and environmental impact assessments. This helps communities make informed decisions about aquaculture, fishing, and sustainable coastal development."
    },
    {
      question: "What kind of marine research capabilities does FloatChat offer?",
      answer: "FloatChat supports various research activities including ocean temperature monitoring, salinity tracking, marine biodiversity analysis, and climate change impact studies. Researchers can access historical data, real-time feeds, and predictive analytics for their studies."
    },
    {
      question: "Is FloatChat suitable for commercial maritime operations?",
      answer: "Absolutely! FloatChat provides enterprise-grade solutions for shipping companies, offshore operations, and maritime logistics. Features include route optimization, weather routing, fuel efficiency calculations, and safety monitoring."
    }
   
  ];

  // Handle scroll effect for navbar
  useEffect(() => {
    const handleScroll = () => {
      const isScrolled = window.scrollY > 50;
      setScrolled(isScrolled);
    };
    

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

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
    { name: 'News', href: '/news', icon: FaNewspaper },
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
            ? 'backdrop-blur-xl shadow-lg shadow-black/5' 
            : 'backdrop-blur-sm'
        }`}
        style={{
          backdropFilter: scrolled ? 'blur(20px) saturate(180%)' : 'blur(0px)',
          WebkitBackdropFilter: scrolled ? 'blur(20px) saturate(180%)' : 'blur(yiu80px)',
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

     {/* Modules Section */}
      <div className='w-full bg-gradient-to-b from-slate-900 to-slate-800 px-2 py-20'>
              
              {/* Section Header */}
{/* Enhanced Section Header */}
<div className="max-w-6xl mx-auto text-center mb-16">
  <motion.div
    initial={{ opacity: 0, y: 30 }}
    whileInView={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.8 }}
    viewport={{ once: true }}
    className="space-y-6"
  >
    {/* Subtitle Badge */}


    {/* Main Heading */}
    <motion.h2 
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, delay: 0.3 }}
      viewport={{ once: true }}
      className="text-5xl md:text-6xl lg:text-6xl font-bold leading-tight"
    >
      <span className="block text-white mb-2">Ocean Intelligence</span>
      <span className="block bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-transparent relative">
        Modules
        {/* Decorative underline */}
        
      </span>
    </motion.h2>

    {/* Enhanced Description */}
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, delay: 0.5 }}
      viewport={{ once: true }}
      className="max-w-4xl mx-auto"
    >
      <p className="text-xl md:text-2xl text-slate-300 leading-relaxed mb-6">
        Comprehensive <span className="text-cyan-400 font-semibold">AI-powered solutions</span> for marine navigation, 
        coastal development, and <span className="text-blue-400 font-semibold">ocean research</span>
      </p>
      
      {/* Feature highlights */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.7 }}
        viewport={{ once: true }}
        className="flex flex-wrap justify-center gap-6 text-sm"
      >
        
      </motion.div>
    </motion.div>

    {/* Floating Elements */}
    <div className="absolute inset-0 pointer-events-none overflow-hidden">
      <motion.div
        animate={{
          y: [0, -20, 0],
          rotate: [0, 5, 0],
        }}
        transition={{
          duration: 6,
          repeat: Infinity,
          ease: "easeInOut"
        }}
        className="absolute top-10 left-10 w-16 h-16 bg-gradient-to-r from-cyan-400/20 to-blue-400/20 rounded-full blur-xl"
      />
      <motion.div
        animate={{
          y: [0, 15, 0],
          rotate: [0, -3, 0],
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          ease: "easeInOut",
          delay: 2
        }}
        className="absolute top-20 right-20 w-12 h-12 bg-gradient-to-r from-purple-400/20 to-pink-400/20 rounded-full blur-xl"
      />
      <motion.div
        animate={{
          y: [0, -10, 0],
          x: [0, 10, 0],
        }}
        transition={{
          duration: 7,
          repeat: Infinity,
          ease: "easeInOut",
          delay: 1
        }}
        className="absolute bottom-10 left-1/4 w-8 h-8 bg-gradient-to-r from-teal-400/20 to-cyan-400/20 rounded-full blur-lg"
      />
    </div>
  </motion.div>
</div>

      
              {/* Marine Navigation Module - Background Image Design */}
              <section id="marine-navigation" className="mb-24">
                <div className="max-w-8xl mx-auto px-10">
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
                          onClick={ () => navigate('/marine-navigation') }
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
                <div className="max-w-8xl mx-auto px-10">
                  <motion.div 
                    initial={{ opacity: 0, y: 50 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    className="relative rounded-3xl overflow-hidden min-h-[600px] flex items-center shadow-[0_25px_50px_-12px_rgba(0,0,0,0.5)] hover:shadow-[0_35px_60px_-12px_rgba(59,130,246,0.4)] transition-all duration-500"
                    style={{
                      filter: 'drop-shadow(0 25px 50px rgba(0, 0, 0, 0.3))',
                    }}
                  >
                    {/* Background Image */}
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
              <section id="research" className="mb-2">
                <div className="max-w-8xl mx-auto px-10">
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

       {/* FAQ Section - Ocean Themed */}
        <section className="relative bg-gradient-to-b from-slate-800 to-slate-900 py-20">
          {/* Background Elements */}
          <div className="absolute inset-0 overflow-hidden">
            <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-r from-cyan-400/5 to-blue-500/5 rounded-full blur-3xl"></div>
            <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-r from-blue-400/5 to-purple-500/5 rounded-full blur-3xl"></div>
          </div>

          <div className="relative max-w-7xl mx-auto px-6">
            <div className="flex flex-col lg:flex-row items-start gap-12">
              
              {/* Left Content */}
              <motion.div 
                className="flex-1 lg:pr-8"
                initial={{ opacity: 0, x: -30 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8 }}
                viewport={{ once: true }}
              >
                <div className="space-y-6">
                  {/* Badge */}
                  <motion.span 
                    className="inline-flex items-center gap-2 bg-gradient-to-r from-cyan-500/10 to-blue-500/10 border border-cyan-500/20 text-cyan-400 px-6 py-3 rounded-full text-sm font-semibold backdrop-blur-sm"
                    initial={{ opacity: 0, scale: 0.8 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.6, delay: 0.2 }}
                    viewport={{ once: true }}
                  >
                    <FaQuestionCircle className="text-cyan-400" />
                    FREQUENTLY ASKED QUESTIONS
                  </motion.span>

                  {/* Title */}
                  <motion.h2 
                    className="text-4xl lg:text-5xl xl:text-6xl font-bold leading-tight"
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.3 }}
                    viewport={{ once: true }}
                  >
                    <span className="text-white">Have a question?</span>
                    <br />
                    <span className="bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
                      Here are some solutions
                    </span>
                  </motion.h2>

                  {/* Description */}
                  <motion.p 
                    className="text-slate-300 text-lg lg:text-xl leading-relaxed max-w-lg"
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.4 }}
                    viewport={{ once: true }}
                  >
                    For more queries about FloatChat and ocean intelligence, feel free to reach us through our support channels.
                  </motion.p>

                  {/* Contact Button */}
                  <motion.button
                    className="group relative inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-500 text-white font-semibold rounded-2xl overflow-hidden transition-all duration-300 shadow-lg hover:shadow-cyan-500/25"
                    whileHover={{ 
                      scale: 1.05,
                      boxShadow: '0 20px 40px rgba(6,182,212,0.3)'
                    }}
                    whileTap={{ scale: 0.95 }}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.5 }}
                    viewport={{ once: true }}
                  >
                    <span className="relative z-10">Contact Support</span>
                    <FaArrowRight className="relative z-10 group-hover:translate-x-1 transition-transform duration-300" />
                    <div className="absolute inset-0 bg-gradient-to-r from-cyan-600 to-blue-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                  </motion.button>
                </div>
              </motion.div>

              {/* Right Content - FAQ Items */}
              <motion.div 
                className="flex-1 w-full space-y-4"
                initial={{ opacity: 0, x: 30 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8, delay: 0.2 }}
                viewport={{ once: true }}
              >
                {faqs.map((faq, idx) => (
                  <motion.div
                    key={idx}
                    className={`group border border-slate-700/50 rounded-2xl px-6 py-5 transition-all duration-300 backdrop-blur-sm ${
                      openIndex === idx 
                        ? 'shadow-lg bg-gradient-to-r from-cyan-500/5 to-blue-500/5 border-cyan-500/30 shadow-cyan-500/10' 
                        : 'hover:shadow-md hover:bg-slate-800/30 hover:border-slate-600/50'
                    }`}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: idx * 0.1 }}
                    viewport={{ once: true }}
                  >
                    <div
                      className="flex justify-between items-center cursor-pointer"
                      onClick={() => toggleFAQ(idx)}
                    >
                      <p className="text-lg font-medium text-white pr-4 leading-relaxed group-hover:text-cyan-100 transition-colors duration-300">
                        {faq.question}
                      </p>
                      
                      <motion.div
                        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center transition-all duration-300 ${
                          openIndex === idx 
                            ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white' 
                            : 'bg-slate-700/50 text-slate-400 group-hover:bg-slate-600/50 group-hover:text-slate-300'
                        }`}
                        animate={{ rotate: openIndex === idx ? 45 : 0 }}
                        transition={{ duration: 0.3 }}
                      >
                        {openIndex === idx ? (
                          <FaTimes className="w-4 h-4" />
                        ) : (
                          <FaPlus className="w-4 h-4" />
                        )}
                      </motion.div>
                    </div>
                    
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ 
                        height: openIndex === idx ? 'auto' : 0,
                        opacity: openIndex === idx ? 1 : 0
                      }}
                      transition={{ duration: 0.3, ease: 'easeInOut' }}
                      className="overflow-hidden"
                    >
                      {openIndex === idx && (
                        <motion.p 
                          className="text-slate-300 mt-6 text-base leading-relaxed border-t border-slate-700/30 pt-6"
                          initial={{ opacity: 0, y: -10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ duration: 0.3, delay: 0.1 }}
                        >
                          {faq.answer}
                        </motion.p>
                      )}
                    </motion.div>
                  </motion.div>
                ))}
              </motion.div>
            </div>
          </div>
        </section>

      {/* Compact Professional Footer */}
<footer id="about" className="bg-gradient-to-r from-slate-800 to-slate-900 border-t border-slate-700/50">
  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    
    {/* Main Footer Content */}
    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-6">
      
      {/* Company Info */}
      <motion.div 
        className="space-y-4"
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        viewport={{ once: true }}
      >
        <div className="flex items-center space-x-3">
          <img src={img1} alt="FloatChat Logo" className="w-8 h-8 rounded-lg" />
          <div>
            <h3 className="text-lg font-bold text-white font-poppins">FloatChat</h3>
            <p className="text-xs text-cyan-400">by SYNTAX SQUAD</p>
          </div>
        </div>
        <p className="text-slate-400 text-sm leading-relaxed">
          AI-powered ocean intelligence platform revolutionizing marine navigation and research.
        </p>
      </motion.div>

      {/* Quick Links */}
      <motion.div 
        className="space-y-4"
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
        viewport={{ once: true }}
      >
        <h4 className="text-md font-semibold text-white font-poppins">Quick Links</h4>
        <div className="grid grid-cols-2 gap-2">
          {[
            'About Us', 'Marine Navigation', 'Ocean Research', 'Contact',
            'Documentation', 'API Reference', 'Support', 'Privacy'
          ].map((link, index) => (
            <a 
              key={link}
              href="#" 
              className="text-slate-400 hover:text-cyan-400 transition-colors duration-300 text-sm"
            >
              {link}
            </a>
          ))}
        </div>
      </motion.div>

      {/* Contact & Social */}
      <motion.div 
        className="space-y-4"
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        viewport={{ once: true }}
      >
        <h4 className="text-md font-semibold text-white font-poppins">Connect</h4>
        <div className="space-y-2">
          <a href="mailto:support@floatchat.ai" className="block text-slate-400 hover:text-cyan-400 transition-colors text-sm">
            support@floatchat.ai
          </a>
          <p className="text-slate-400 text-sm">24/7 Maritime Support</p>
        </div>
        
        {/* Social Links */}
        <div className="flex space-x-3">
          {[
            { icon: '🌊', label: 'Ocean Network' },
            { icon: '📧', label: 'Email' },
            { icon: '🔗', label: 'LinkedIn' },
            { icon: '🐙', label: 'GitHub' }
          ].map((social, index) => (
            <motion.a
              key={social.label}
              href="#"
              className="w-8 h-8 bg-slate-700/50 hover:bg-cyan-500/20 rounded-full flex items-center justify-center transition-all duration-300 border border-slate-600/50 hover:border-cyan-400/50"
              whileHover={{ scale: 1.1 }}
            >
              <span className="text-sm">{social.icon}</span>
            </motion.a>
          ))}
        </div>
      </motion.div>
    </div>

    {/* Bottom Bar */}
    <div className="border-t border-slate-700/50 pt-6">
      <div className="flex flex-col md:flex-row justify-between items-center space-y-3 md:space-y-0">
        
        {/* Copyright */}
        <div className="text-sm text-slate-400 text-center md:text-left">
          © 2024 FloatChat by SYNTAX SQUAD. All rights reserved.
        </div>

        {/* Tech Credits */}

      </div>
    </div>
  </div>
</footer>

{/* Compact Back to Top Button */}
<motion.button
  className="fixed bottom-6 right-6 w-12 h-12 bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-300 z-40 flex items-center justify-center"
  onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
  whileHover={{ scale: 1.1 }}
  whileTap={{ scale: 0.9 }}
  initial={{ opacity: 0, y: 100 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.6, delay: 2 }}
>
  ↑
</motion.button>
      </div>
          <Virtual />
      
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

