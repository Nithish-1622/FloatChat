import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  FaAnchor, FaArrowLeft, FaCompass, FaShip, FaMap, FaCloud, 
  FaRoute, FaShieldAlt, FaMapMarkerAlt, FaWifi, FaCog,
  FaPlay, FaChartLine, FaBell, FaUser, FaExpand, FaCompress,
  FaLayerGroup, FaSatellite, FaWater, FaGlobe, FaTachometerAlt,
  FaLightbulb, FaRocket, FaEye, FaLock
} from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

export const MarineNavigation = () => {
  const navigate = useNavigate();
  const [activeFeature, setActiveFeature] = useState(0);
  const [isMapFullscreen, setIsMapFullscreen] = useState(false);
  const [selectedLayer, setSelectedLayer] = useState('wind');
  const [currentTime, setCurrentTime] = useState(new Date());

  // Scroll to top when component mounts
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  // Update time every second for real-time 
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const features = [
    {
      icon: FaCompass,
      title: "AI Smart Compass",
      description: "Advanced compass system with machine learning corrections, magnetic declination auto-adjustment, and GPS precision enhancement.",
      color: "from-cyan-500 to-blue-500",
      gradient: "bg-gradient-to-br from-cyan-500/10 to-blue-500/10"
    },
    {
      icon: FaRoute,
      title: "Intelligent Routing",
      description: "ML-powered route optimization considering real-time weather, ocean currents, fuel efficiency, and maritime traffic patterns.",
      color: "from-blue-500 to-indigo-500",
      gradient: "bg-gradient-to-br from-blue-500/10 to-indigo-500/10"
    },
    {
      icon: FaCloud,
      title: "Weather Intelligence",
      description: "Predictive weather analytics with storm tracking, visibility forecasting, and automated safety recommendations.",
      color: "from-indigo-500 to-purple-500",
      gradient: "bg-gradient-to-br from-indigo-500/10 to-purple-500/10"
    },
    {
      icon: FaShip,
      title: "Fleet Command Center",
      description: "Centralized fleet management with real-time vessel tracking, crew communication, and automated dispatch systems.",
      color: "from-purple-500 to-pink-500",
      gradient: "bg-gradient-to-br from-purple-500/10 to-pink-500/10"
    },
    {
      icon: FaMap,
      title: "Dynamic Chart System",
      description: "Real-time nautical charts with depth mapping, hazard detection, and automatic chart updates from maritime authorities.",
      color: "from-teal-500 to-green-500",
      gradient: "bg-gradient-to-br from-teal-500/10 to-green-500/10"
    },
    {
      icon: FaShieldAlt,
      title: "Safety Guardian",
      description: "24/7 safety monitoring with collision avoidance, emergency response automation, and rescue coordination assistance.",
      color: "from-green-500 to-emerald-500",
      gradient: "bg-gradient-to-br from-green-500/10 to-emerald-500/10"
    }
  ];

  const stats = [
    { 
      label: "Active Vessels", 
      value: "2,847", 
      icon: FaShip, 
      change: "+12%",
      color: "text-cyan-400",
      bgColor: "bg-cyan-500/10"
    },
    { 
      label: "Routes Optimized", 
      value: "15,420", 
      icon: FaRoute, 
      change: "+8%",
      color: "text-blue-400",
      bgColor: "bg-blue-500/10"
    },
    { 
      label: "Safety Score", 
      value: "98.7%", 
      icon: FaShieldAlt, 
      change: "+2.1%",
      color: "text-green-400",
      bgColor: "bg-green-500/10"
    },
    { 
      label: "Fuel Efficiency", 
      value: "23%", 
      icon: FaChartLine, 
      change: "+5.2%",
      color: "text-purple-400",
      bgColor: "bg-purple-500/10"
    }
  ];

  const weatherLayers = [
    { 
      id: 'wind', 
      name: 'Wind Patterns', 
      icon: FaCloud, 
      overlay: 'wind',
      color: 'text-blue-400'
    },
    { 
      id: 'waves', 
      name: 'Wave Analysis', 
      icon: FaWater, 
      overlay: 'waves',
      color: 'text-cyan-400'
    },
    { 
      id: 'temp', 
      name: 'Temperature', 
      icon: FaSatellite, 
      overlay: 'temp',
      color: 'text-orange-400'
    },
    { 
      id: 'rain', 
      name: 'Precipitation', 
      icon: FaCloud, 
      overlay: 'rain',
      color: 'text-indigo-400'
    }
  ];

  // Fixed arrays for the control panels
  const positionData = [
    { label: "Latitude", value: "40°45'N", icon: FaGlobe },
    { label: "Longitude", value: "74°00'W", icon: FaGlobe },
    { label: "Speed", value: "12.5 knots", icon: FaTachometerAlt },
    { label: "Course", value: "045°", icon: FaCompass }
  ];

  const weatherData = [
    { label: "Wind Speed", value: "15 kts", color: "text-blue-400" },
    { label: "Wind Direction", value: "SW", color: "text-cyan-400" },
    { label: "Wave Height", value: "2.1 m", color: "text-teal-400" },
    { label: "Visibility", value: "Good", color: "text-green-400" }
  ];

  const systemData = [
    { label: "GPS Signal", value: "Strong", color: "text-green-400" },
    { label: "Weather Data", value: "Updated", color: "text-green-400" },
    { label: "Route Status", value: "Optimized", color: "text-blue-400" }
  ];

  const toggleMapFullscreen = () => {
    setIsMapFullscreen(!isMapFullscreen);
  };

  const getWindyMapUrl = (layer = 'wind', fullscreen = false) => {
    const baseUrl = 'https://embed.windy.com/embed2.html';
    const params = new URLSearchParams({
      lat: '40.759',
      lon: '-73.985',
      detailLat: '40.759',
      detailLon: '-73.985',
      width: fullscreen ? '1920' : '650',
      height: fullscreen ? '1080' : '450',
      zoom: '8',
      level: 'surface',
      overlay: layer,
      product: 'ecmwf',
      menu: '',
      message: '',
      marker: 'true',
      calendar: 'now',
      pressure: '',
      type: 'map',
      location: 'coordinates',
      detail: '',
      metricWind: 'default',
      metricTemp: 'default',
      radarRange: '-1'
    });
    return `${baseUrl}?${params.toString()}`;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-blue-950 relative overflow-hidden">
      
      {/* Background Elements */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-900/20 via-transparent to-transparent"></div>
      <div className="absolute top-0 left-0 w-full h-full">
        <div className="absolute top-20 left-20 w-64 h-64 bg-cyan-500/5 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-blue-500/5 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>
      
      {/* Fullscreen Map Modal */}
      <AnimatePresence>
        {isMapFullscreen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/95 backdrop-blur-sm"
          >
            <div className="relative w-full h-full">
              <motion.button
                onClick={toggleMapFullscreen}
                className="absolute top-6 right-6 z-60 p-4 bg-slate-800/90 backdrop-blur-xl text-white rounded-2xl hover:bg-slate-700/90 transition-all duration-300 shadow-2xl border border-slate-600/50"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <FaCompress className="text-xl" />
              </motion.button>
              
              {/* Enhanced Fullscreen Layer Controls */}
              <motion.div
                initial={{ x: -100, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                className="absolute top-6 left-6 z-60 bg-slate-800/90 backdrop-blur-xl rounded-2xl p-6 border border-slate-600/50 shadow-2xl min-w-[300px]"
              >
                <h4 className="text-white text-lg font-semibold mb-4 flex items-center">
                  <FaLayerGroup className="mr-3 text-cyan-400" />
                  Weather Intelligence Layers
                </h4>
                <div className="grid grid-cols-1 gap-3">
                  {weatherLayers.map((layer) => (
                    <motion.button
                      key={layer.id}
                      onClick={() => setSelectedLayer(layer.overlay)}
                      className={`flex items-center space-x-3 px-4 py-3 rounded-xl text-sm transition-all duration-300 ${
                        selectedLayer === layer.overlay
                          ? 'bg-gradient-to-r from-cyan-500/30 to-blue-500/30 text-white border border-cyan-400/50 shadow-lg'
                          : 'bg-slate-700/50 text-slate-300 hover:bg-slate-600/70'
                      }`}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      <layer.icon className={`text-lg ${layer.color}`} />
                      <span className="font-medium">{layer.name}</span>
                    </motion.button>
                  ))}
                </div>
              </motion.div>

              <div className="w-full h-full">
                <iframe
                  src={getWindyMapUrl(selectedLayer, true)}
                  width="100%"
                  height="100%"
                  frameBorder="0"
                  className="rounded-none"
                  title="Windy Marine Navigation Map - Fullscreen"
                />
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Enhanced Header Section */}
      <header className="relative bg-gradient-to-r from-slate-900/95 via-slate-800/95 to-slate-900/95 backdrop-blur-xl border-b border-slate-700/50 shadow-2xl">
        <div className="container mx-auto px-6 py-8">
          
          {/* Back Button */}
          <motion.button
            onClick={() => navigate(-1)}
            className="inline-flex items-center space-x-3 text-cyan-400 hover:text-cyan-300 transition-all duration-300 mb-10 p-3 rounded-xl hover:bg-slate-800/50"
            whileHover={{ x: -8, scale: 1.05 }}
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            <FaArrowLeft className="text-lg" />
            <span className="font-semibold">Back to Dashboard</span>
          </motion.button>

          {/* Header Content */}
          <div className="flex flex-col justify-center items-center xl:flex-row xl:items-center ">
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="flex-1"
            >
              <div className="flex  items-center space-x-6 mb-6">
                <div className="relative w-20 h-20 bg-gradient-to-br from-cyan-500/20 to-blue-500/20 backdrop-blur-xl rounded-3xl flex items-center justify-center border border-cyan-400/30 shadow-2xl">
                  <FaAnchor className="text-4xl text-cyan-400" />
                </div>
                <div>
                  <h1 className="text-5xl xl:text-6xl font-bold bg-gradient-to-r from-white via-cyan-100 to-blue-200 bg-clip-text text-transparent">
                    Marine Navigation
                  </h1>
                  <p className="text-xl text-cyan-400 font-semibold mt-2">AI-Powered Maritime Intelligence Platform</p>
             
                </div>
              </div>
              <p className="text-xl text-slate-300 max-w-3xl mb-8 leading-relaxed">
                Revolutionary navigation system integrating cutting-edge AI analytics, real-time meteorological data, 
                and predictive routing algorithms for unprecedented maritime safety and operational efficiency.
              </p>
            </motion.div>

            {/* Enhanced Quick Actions */}
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, delay: 0.3 }}
              className="flex flex-col sm:flex-row gap-4 mt-1 xl:mt-0"
            >
              <motion.button 
                onClick={() => navigate('/chatbot')}
                className="group px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-600 text-white rounded-2xl font-semibold hover:from-cyan-400 hover:to-blue-500 transition-all duration-300 flex items-center space-x-3 shadow-2xl border border-cyan-400/30"
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.95 }}
              >
                <FaRocket className="text-lg group-hover:animate-bounce" />
                <span>Launch Ocean Bot</span>
              </motion.button>
            </motion.div>
          </div>
        </div>
      </header>

      {/* Enhanced Stats Section */}
      <section className="py-16 bg-gradient-to-r from-slate-800/30 to-slate-700/30 backdrop-blur-sm">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="grid grid-cols-2 lg:grid-cols-4 gap-6"
          >
            {stats.map((stat, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.1 * index }}
                className="relative group"
              >
                <div className={`${stat.bgColor} backdrop-blur-xl rounded-3xl p-8 border border-slate-700/50 text-center transition-all duration-300 group-hover:border-cyan-400/50 group-hover:shadow-2xl group-hover:scale-105`}>
                  <div className="absolute top-4 right-4 text-xs text-green-400 font-semibold">
                    {stat.change}
                  </div>
                  <stat.icon className={`text-4xl ${stat.color} mx-auto mb-4 group-hover:scale-110 transition-transform duration-300`} />
                  <div className="text-3xl font-bold text-white mb-2">{stat.value}</div>
                  <div className="text-sm text-slate-400 font-medium">{stat.label}</div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-20">
        
        {/* Enhanced Windy Map Integration */}
        <section className="mb-24">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="bg-gradient-to-br from-slate-800/60 to-slate-700/60 backdrop-blur-xl rounded-4xl p-10 border border-slate-600/50 shadow-2xl"
          >
            <div className="flex flex-col xl:flex-row items-start xl:items-center justify-between mb-10">
              <div>
                <h2 className="text-4xl font-bold bg-gradient-to-r from-white to-cyan-200 bg-clip-text text-transparent mb-3">
                  Live Maritime Intelligence Center
                </h2>
                <p className="text-slate-400 text-lg">Advanced weather analytics and navigation data powered by Windy's global network</p>
              </div>
              <div className="flex items-center space-x-6 mt-6 xl:mt-0">
                <div className="flex items-center space-x-3">
                  <div className="relative">
                    <div className="w-4 h-4 bg-green-400 rounded-full animate-ping"></div>
                    <div className="absolute inset-0 w-4 h-4 bg-green-400 rounded-full"></div>
                  </div>
                  <span className="text-green-400 font-semibold">Real-time Data Stream</span>
                </div>
                <motion.button 
                  onClick={toggleMapFullscreen}
                  className="p-4 bg-slate-700/50 backdrop-blur-xl rounded-2xl hover:bg-slate-600/70 transition-all duration-300 border border-slate-600/50"
                  title="Expand to Fullscreen"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                >
                  <FaExpand className="text-slate-400 text-xl" />
                </motion.button>
              </div>
            </div>

            {/* Enhanced Map Container */}
            <div className="bg-slate-900/70 backdrop-blur-xl rounded-3xl p-6 border border-slate-600/30 shadow-inner">
              <div className="grid xl:grid-cols-4 gap-8">
                
                {/* Map Section */}
                <div className="xl:col-span-3">
                  <div className="relative w-full h-[600px] bg-slate-800/50 rounded-2xl overflow-hidden border border-slate-600/30 shadow-2xl">
                    <iframe
                      key={selectedLayer}
                      src={getWindyMapUrl(selectedLayer)}
                      width="100%"
                      height="100%"
                      frameBorder="0"
                      className="rounded-2xl"
                      title="Windy Marine Navigation Map"
                    />
                    
                    {/* Enhanced Map Controls */}
                    <div className="absolute top-6 left-6 bg-slate-800/95 backdrop-blur-xl rounded-2xl p-5 border border-slate-600/50 shadow-2xl min-w-[280px]">
                      <h4 className="text-white text-lg font-semibold mb-4 flex items-center">
                        <FaLayerGroup className="mr-3 text-cyan-400" />
                        Weather Layers
                      </h4>
                      <div className="space-y-3">
                        {weatherLayers.map((layer) => (
                          <motion.button
                            key={layer.id}
                            onClick={() => setSelectedLayer(layer.overlay)}
                            className={`flex items-center space-x-3 w-full px-4 py-3 rounded-xl text-sm transition-all duration-300 ${
                              selectedLayer === layer.overlay
                                ? 'bg-gradient-to-r from-cyan-500/30 to-blue-500/30 text-white border border-cyan-400/50 shadow-lg'
                                : 'bg-slate-700/50 text-slate-300 hover:bg-slate-600/70'
                            }`}
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                          >
                            <layer.icon className={`text-lg ${layer.color}`} />
                            <span className="font-medium">{layer.name}</span>
                          </motion.button>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Enhanced Controls Panel */}
                <div className="space-y-6">
                  {/* Current Position Panel */}
                  <motion.div
                    initial={{ opacity: 0, x: 30 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.6, delay: 0.7 }}
                    className="bg-slate-800/60 backdrop-blur-xl rounded-2xl p-6 border border-slate-600/30 shadow-xl"
                  >
                    <h4 className="text-white font-semibold text-lg mb-4 flex items-center">
                      <FaMapMarkerAlt className="text-cyan-400 mr-3 text-xl" />
                      Current Position
                    </h4>
                    <div className="space-y-3">
                      {positionData.map((item, index) => (
                        <div key={index} className="flex items-center justify-between p-3 bg-slate-700/30 rounded-xl">
                          <div className="flex items-center space-x-3">
                            <item.icon className="text-cyan-400" />
                            <span className="text-slate-400">{item.label}:</span>
                          </div>
                          <span className="text-white font-semibold">{item.value}</span>
                        </div>
                      ))}
                    </div>
                  </motion.div>

                  {/* Weather Conditions Panel */}
                  <motion.div
                    initial={{ opacity: 0, x: 30 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.6, delay: 0.8 }}
                    className="bg-slate-800/60 backdrop-blur-xl rounded-2xl p-6 border border-slate-600/30 shadow-xl"
                  >
                    <h4 className="text-white font-semibold text-lg mb-4 flex items-center">
                      <FaCloud className="text-blue-400 mr-3 text-xl" />
                      Weather Conditions
                    </h4>
                    <div className="space-y-3">
                      {weatherData.map((item, index) => (
                        <div key={index} className="flex items-center justify-between p-3 bg-slate-700/30 rounded-xl">
                          <span className="text-slate-400">{item.label}:</span>
                          <span className={`font-semibold ${item.color}`}>{item.value}</span>
                        </div>
                      ))}
                    </div>
                  </motion.div>

                  {/* System Status Panel */}
                  <motion.div
                    initial={{ opacity: 0, x: 30 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.6, delay: 0.9 }}
                    className="bg-slate-800/60 backdrop-blur-xl rounded-2xl p-6 border border-slate-600/30 shadow-xl"
                  >
                    <h4 className="text-white font-semibold text-lg mb-4 flex items-center">
                      <FaWifi className="text-green-400 mr-3 text-xl" />
                      System Status
                    </h4>
                    <div className="space-y-3">
                      {systemData.map((item, index) => (
                        <div key={index} className="flex items-center justify-between p-3 bg-slate-700/30 rounded-xl">
                          <span className="text-slate-400">{item.label}:</span>
                          <div className="flex items-center space-x-2">
                            <div className={`w-2 h-2 rounded-full ${item.color.replace('text-', 'bg-')} animate-pulse`}></div>
                            <span className={`font-semibold ${item.color}`}>{item.value}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </motion.div>
                </div>
              </div>
            </div>
          </motion.div>
        </section>

        {/* Enhanced Features Section */}
        <section className="mb-24">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="text-center mb-16"
          >
            <h2 className="text-5xl font-bold bg-gradient-to-r from-white via-cyan-200 to-blue-300 bg-clip-text text-transparent mb-6">
              Advanced Navigation Features
            </h2>
            <p className="text-xl text-slate-400 max-w-4xl mx-auto leading-relaxed">
              Cutting-edge maritime technology suite designed to revolutionize ocean navigation, 
              enhance safety protocols, and optimize operational efficiency across all vessel types.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.1 * index }}
                className="group relative"
                whileHover={{ y: -8, scale: 1.02 }}
                onClick={() => setActiveFeature(index)}
              >
                <div className={`${feature.gradient} backdrop-blur-xl rounded-3xl p-8 border border-slate-700/50 hover:border-cyan-400/50 transition-all duration-500 cursor-pointer shadow-2xl group-hover:shadow-cyan-500/20`}>
                  <div className={`w-16 h-16 bg-gradient-to-r ${feature.color} rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-all duration-300 shadow-lg`}>
                    <feature.icon className="text-3xl text-white" />
                  </div>
                  <h3 className="text-2xl font-bold text-white mb-4 group-hover:text-cyan-300 transition-colors duration-300">
                    {feature.title}
                  </h3>
                  <p className="text-slate-400 leading-relaxed group-hover:text-slate-300 transition-colors duration-300">
                    {feature.description}
                  </p>
                  
                  {/* Hover effect overlay */}
                  <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/5 to-blue-500/5 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                </div>
              </motion.div>
            ))}
          </div>
        </section>

      </main>
    </div>
  );
};
