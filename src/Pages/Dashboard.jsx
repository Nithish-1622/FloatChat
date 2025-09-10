import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import water from '../Assets/water.mp4'
import { useNavigate } from 'react-router-dom'
import { FaRobot, FaArrowRight, FaWater, FaFish, FaLeaf, FaBookOpen, FaEnvelope , FaAnchor , FaCompass , FaShip , FaShieldAlt , FaSearch } from 'react-icons/fa'
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

    <div className="no-scrollbar">

      {/* Enhanced Navigation Bar with Fixed Position and Blur Effect */}
      <motion.nav
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
          scrolled 
            ? '  backdrop-blur-xl  shadow-lg shadow-black/5' 
            : ' backdrop-blur-sm'
        }`}
        style={{
          backdropFilter: scrolled ? 'blur(20px) saturate(180%)' : 'blur(0px)',
          WebkitBackdropFilter: scrolled ? 'blur(20px) saturate(180%)' : 'blur(0px)',
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

     {/* Modules Section */}
      <div className='w-full bg-gradient-to-b from-slate-900 to-slate-800 px-4 py-20'>
        
        {/* Section Header */}
        <div className="max-w-6xl mx-auto text-center mb-16">
          <h2 className="text-5xl font-bold text-white mb-6">Ocean Intelligence Modules</h2>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto">
            Comprehensive AI-powered solutions for marine navigation, coastal development, and ocean research
          </p>
        </div>

        {/* Marine Navigation Module */}
        <section id="marine-navigation" className="mb-24">
          <div className="max-w-6xl mx-auto">
            <div className="bg-gradient-to-r from-cyan-900/30 to-cyan-500/30 backdrop-blur-sm rounded-3xl p-8 border border-cyan-500/20 shadow-2xl">
              <div className="text-center mb-8">
                <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-full mb-6 shadow-lg">
                  <FaAnchor className="text-3xl text-white" />
                </div>
                <h3 className="text-3xl font-bold text-white mb-4">Marine Navigation & Sea Travel Intelligence</h3>
                <p className="text-lg text-slate-300 max-w-4xl mx-auto leading-relaxed">
                  AI-powered navigation system serving fishers, cargo ships, and coast guard with intelligent routing, 
                  real-time weather integration, and comprehensive maritime domain awareness.
                </p>
              </div>
              
              <div className="grid md:grid-cols-3 gap-6 mb-8">
                <ModuleFeature 
                  icon={<FaCompass />}
                  title="Fisheries Support"
                  description="AI Navigation Assistant with PFZ integration, border alerts, and storm warnings"
                  color="cyan"
                />
                <ModuleFeature 
                  icon={<FaShip />}
                  title="Cargo Operations"
                  description="Route optimization, traffic control, and emission reduction for green shipping"
                  color="blue"
                />
                <ModuleFeature 
                  icon={<FaShieldAlt />}
                  title="Coast Guard Intelligence"
                  description="Maritime domain awareness with dark vessel detection and enforcement tools"
                  color="indigo"
                />
              </div>
              
              <div className="text-center">
                <button 
                  onClick={() => handleModuleNavigation('marine-navigation')}
                  className="group inline-flex items-center px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-semibold rounded-full shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105"
                >
                  Explore Module
                  <FaArrowRight className="ml-3 group-hover:translate-x-1 transition-transform" />
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* Coastal Livelihood Module */}
        <section id="coastal-livelihood" className="mb-24">
          <div className="max-w-6xl mx-auto">
            <div className="bg-gradient-to-r from-blue-900/30 to-blue-500/30 backdrop-blur-sm rounded-3xl p-8 border border-blue-500/20 shadow-2xl">
              <div className="text-center mb-8">
                <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full mb-6 shadow-lg">
                  <FaFish className="text-3xl text-white" />
                </div>
                <h3 className="text-3xl font-bold text-white mb-4">Coastal Livelihood & Community Development</h3>
                <p className="text-lg text-slate-300 max-w-4xl mx-auto leading-relaxed">
                  Sustainable development solutions for coastal communities including aquaculture optimization, 
                  eco-tourism planning, and resource management systems.
                </p>
              </div>
              
              <div className="grid md:grid-cols-3 gap-6 mb-8">
                <ModuleFeature 
                  icon={<FaFish />}
                  title="Sustainable Fisheries"
                  description="Smart fishing zones, quota management, and ecosystem preservation"
                  color="blue"
                />
                <ModuleFeature 
                  icon={<FaWater />}
                  title="Aquaculture Systems"
                  description="AI-driven fish farming and seaweed cultivation optimization"
                  color="teal"
                />
                <ModuleFeature 
                  icon={<FaCompass />}
                  title="Eco-Tourism"
                  description="Community-based tourism with environmental impact monitoring"
                  color="purple"
                />
              </div>
              
              <div className="text-center">
                <button 
                  onClick={() => handleModuleNavigation('coastal-livelihood')}
                  className="group inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold rounded-full shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105"
                >
                  Explore Module
                  <FaArrowRight className="ml-3 group-hover:translate-x-1 transition-transform" />
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* Marine Research Module */}
        <section id="research" className="mb-24">
          <div className="max-w-6xl mx-auto">
            <div className="bg-gradient-to-r from-purple-900/30 to-indigo-900/30 backdrop-blur-sm rounded-3xl p-8 border border-purple-500/20 shadow-2xl">
              <div className="text-center mb-8">
                <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-purple-400 to-indigo-500 rounded-full mb-6 shadow-lg">
                  <FaSearch className="text-3xl text-white" />
                </div>
                <h3 className="text-3xl font-bold text-white mb-4">Marine Research & Ocean Analytics</h3>
                <p className="text-lg text-slate-300 max-w-4xl mx-auto leading-relaxed">
                  Advanced oceanographic research tools with AI-powered data analysis, climate monitoring, 
                  and biodiversity assessment for scientific discovery.
                </p>
              </div>
              
              <div className="grid md:grid-cols-3 gap-6 mb-8">
                <ModuleFeature 
                  icon={<FaSearch />}
                  title="Data Collection"
                  description="Automated sensor networks and satellite data integration"
                  color="purple"
                />
                <ModuleFeature 
                  icon={<FaWater />}
                  title="Marine Biology"
                  description="Species tracking, migration analysis, and ecosystem health monitoring"
                  color="indigo"
                />
                <ModuleFeature 
                  icon={<FaShieldAlt />}
                  title="Climate Impact"
                  description="Ocean acidification tracking and sea level rise prediction"
                  color="violet"
                />
              </div>
              
              <div className="text-center">
                <button 
                  onClick={() => handleModuleNavigation('research')}
                  className="group inline-flex items-center px-8 py-4 bg-gradient-to-r from-purple-500 to-indigo-600 text-white font-semibold rounded-full shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105"
                >
                  Explore Module
                  <FaArrowRight className="ml-3 group-hover:translate-x-1 transition-transform" />
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* All Modules Overview */}
        <section id="blogs" className="mb-20">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-12">
              <FaWater className="text-5xl text-teal-400 mx-auto mb-4" />
              <h2 className="text-4xl font-bold text-white mb-4">Complete Ocean Intelligence Suite</h2>
              <p className="text-xl text-slate-300 max-w-3xl mx-auto">
                Integrated solutions for comprehensive ocean management and exploration
              </p>
            </div>
            
            <div className="grid md:grid-cols-3 gap-8">
              <QuickAccessCard 
                icon={<FaAnchor />}
                title="Marine Navigation"
                description="Smart navigation for all maritime sectors"
                color="cyan"
                onClick={() => handleModuleNavigation('marine-navigation')}
              />
              <QuickAccessCard 
                icon={<FaFish />}
                title="Coastal Livelihood"
                description="Sustainable coastal development"
                color="blue"
                onClick={() => handleModuleNavigation('coastal-livelihood')}
              />
              <QuickAccessCard 
                icon={<FaSearch />}
                title="Marine Research"
                description="Advanced ocean analytics"
                color="purple"
                onClick={() => handleModuleNavigation('research')}
              />
            </div>
          </div>
        </section>
      </div>

      
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

