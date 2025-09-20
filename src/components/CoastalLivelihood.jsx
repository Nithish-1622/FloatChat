import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  FaFish, FaArrowLeft, FaWater, FaShip, FaLeaf, FaCloud, 
  FaRoute, FaShieldAlt, FaMapMarkerAlt, FaWifi, FaCog,
  FaPlay, FaChartLine, FaBell, FaUser, FaExpand, FaCompress,
  FaLayerGroup, FaSatellite, FaHome, FaGlobe, FaTachometerAlt,
  FaLightbulb, FaRocket, FaEye, FaLock, FaTree, FaIndustry,
  FaUsers, FaHeart, FaDollarSign, FaRecycle, FaGem, FaMask,
  FaSnowflake, FaThermometerHalf, FaExclamationTriangle,
  FaCheckCircle, FaClock, FaArrowUp, FaArrowDown,
  FaChevronRight, FaChevronDown, FaInfoCircle, FaToggleOn,
  FaToggleOff, FaLanguage, FaDownload, FaUpload, FaSyncAlt
} from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

export const CoastalLivelihood = () => {
  const navigate = useNavigate();
  const [activeRole, setActiveRole] = useState('pearl');
  const [expandedCard, setExpandedCard] = useState(null);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [alertsVisible, setAlertsVisible] = useState(true);
  const [offlineMode, setOfflineMode] = useState(false);

  // Update time every second for real-time feel
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const roles = [
    {
      id: 'pearl',
      name: 'Pearl Cultivators',
      icon: FaGem,
      color: 'from-purple-500 to-pink-500',
      bgColor: 'bg-purple-500/10',
      count: '324',
      description: 'Monitoring pearl cultivation conditions'
    },
    {
      id: 'diver',
      name: 'Scuba Divers & Tourism',
      icon: FaMask,
      color: 'from-cyan-500 to-blue-500',
      bgColor: 'bg-cyan-500/10',
      count: '189',
      description: 'Dive safety and tourism operations'
    },
    {
      id: 'salt',
      name: 'Salt Manufacturers',
      icon: FaSnowflake,
      color: 'from-orange-500 to-yellow-500',
      bgColor: 'bg-orange-500/10',
      count: '156',
      description: 'Salt production optimization'
    },
    {
      id: 'aqua',
      name: 'Aquaculture Operators',
      icon: FaFish,
      color: 'from-green-500 to-teal-500',
      bgColor: 'bg-green-500/10',
      count: '567',
      description: 'Fish and shrimp farming management'
    }
  ];

  const alertTypes = {
    critical: { color: 'red', icon: FaExclamationTriangle },
    warning: { color: 'yellow', icon: FaClock },
    info: { color: 'blue', icon: FaInfoCircle },
    success: { color: 'green', icon: FaCheckCircle }
  };

  const roleData = {
    pearl: {
      metrics: [
        { label: 'Salinity Level', value: '34.2 PSU', status: 'optimal', trend: 'stable', icon: FaWater },
        { label: 'Turbidity', value: '2.1 NTU', status: 'good', trend: 'improving', icon: FaEye },
        { label: 'Water Quality Index', value: '8.7/10', status: 'excellent', trend: 'stable', icon: FaShieldAlt },
        { label: 'Pearl Growth Rate', value: '+12%', status: 'good', trend: 'improving', icon: FaGem }
      ],
      alerts: [
        { type: 'warning', message: 'Algal bloom risk increasing in Zone B', time: '2 hours ago' },
        { type: 'info', message: 'Optimal conditions for pearl seeding next week', time: '4 hours ago' },
        { type: 'success', message: 'Water quality improved by 15%', time: '1 day ago' }
      ],
      forecasts: [
        { parameter: 'Salinity', current: 34.2, forecast: [34.1, 34.0, 33.9, 34.1, 34.3], optimal: [32, 36] },
        { parameter: 'Turbidity', current: 2.1, forecast: [2.3, 2.5, 2.2, 2.0, 1.9], optimal: [0, 3] }
      ]
    },
    diver: {
      metrics: [
        { label: 'Dive Safety Index', value: '9.2/10', status: 'excellent', trend: 'stable', icon: FaShieldAlt },
        { label: 'Visibility', value: '18.5m', status: 'excellent', trend: 'improving', icon: FaEye },
        { label: 'Current Strength', value: '0.3 m/s', status: 'safe', trend: 'stable', icon: FaRoute },
        { label: 'Tourism Load', value: '45%', status: 'moderate', trend: 'stable', icon: FaUsers }
      ],
      alerts: [
        { type: 'success', message: 'Perfect diving conditions today', time: '30 minutes ago' },
        { type: 'info', message: 'Tourist group arriving at 2 PM', time: '1 hour ago' },
        { type: 'warning', message: 'Increased boat traffic expected tomorrow', time: '3 hours ago' }
      ],
      forecasts: [
        { parameter: 'Visibility', current: 18.5, forecast: [19.2, 20.1, 18.8, 17.5, 18.9], optimal: [15, 25] },
        { parameter: 'Wave Height', current: 0.8, forecast: [0.9, 1.1, 1.3, 1.0, 0.7], optimal: [0, 1.5] }
      ]
    },
    salt: {
      metrics: [
        { label: 'Evaporation Rate', value: '4.2 mm/day', status: 'optimal', trend: 'improving', icon: FaThermometerHalf },
        { label: 'Salinity Concentration', value: '25.8%', status: 'good', trend: 'stable', icon: FaSnowflake },
        { label: 'Production Efficiency', value: '87%', status: 'good', trend: 'improving', icon: FaIndustry },
        { label: 'Climate Impact Score', value: 'Low', status: 'good', trend: 'stable', icon: FaCloud }
      ],
      alerts: [
        { type: 'info', message: 'Ideal harvest conditions in 3 days', time: '1 hour ago' },
        { type: 'warning', message: 'Rain expected next week - prepare covers', time: '2 hours ago' },
        { type: 'success', message: 'Production up 23% this month', time: '1 day ago' }
      ],
      forecasts: [
        { parameter: 'Evaporation', current: 4.2, forecast: [4.5, 4.8, 4.6, 4.3, 4.1], optimal: [4, 6] },
        { parameter: 'Humidity', current: 65, forecast: [62, 58, 60, 68, 72], optimal: [50, 70] }
      ]
    },
    aqua: {
      metrics: [
        { label: 'Dissolved Oxygen', value: '7.8 mg/L', status: 'optimal', trend: 'stable', icon: FaWater },
        { label: 'Water Temperature', value: '26.5°C', status: 'optimal', trend: 'stable', icon: FaThermometerHalf },
        { label: 'Fish Health Index', value: '9.1/10', status: 'excellent', trend: 'improving', icon: FaFish },
        { label: 'Feed Efficiency', value: '92%', status: 'excellent', trend: 'improving', icon: FaLeaf }
      ],
      alerts: [
        { type: 'critical', message: 'Oxygen levels dropping in Cage 3 - immediate action required', time: '15 minutes ago' },
        { type: 'warning', message: 'Pollution detected 2km upstream', time: '45 minutes ago' },
        { type: 'info', message: 'Optimal feeding time window opening', time: '1 hour ago' }
      ],
      forecasts: [
        { parameter: 'Dissolved Oxygen', current: 7.8, forecast: [7.6, 7.4, 7.2, 7.5, 7.9], optimal: [6, 9] },
        { parameter: 'Temperature', current: 26.5, forecast: [26.8, 27.1, 26.9, 26.4, 26.2], optimal: [24, 28] }
      ]
    }
  };

  const currentRoleData = roleData[activeRole];

  const getStatusColor = (status) => {
    const colors = {
      excellent: 'text-green-400',
      optimal: 'text-green-400',
      good: 'text-blue-400',
      moderate: 'text-yellow-400',
      safe: 'text-green-400',
      warning: 'text-yellow-400',
      critical: 'text-red-400'
    };
    return colors[status] || 'text-slate-400';
  };

  const getTrendIcon = (trend) => {
    if (trend === 'improving') return <FaArrowUp className="text-green-400" />;
    if (trend === 'declining') return <FaArrowDown className="text-red-400" />;
    return <FaChartLine className="text-blue-400" />;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-teal-950 relative overflow-hidden">
      
      {/* Background Elements */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-900/20 via-transparent to-transparent"></div>
      <div className="absolute top-0 left-0 w-full h-full">
        <div className="absolute top-20 left-20 w-64 h-64 bg-cyan-500/5 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-teal-500/5 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

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
          <div className="flex flex-col justify-center items-center xl:flex-row xl:items-center">
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="flex-1"
            >
              <div className="flex items-center space-x-6 mb-6">
                <div className="relative w-20 h-20 bg-gradient-to-br from-cyan-500/20 to-teal-500/20 backdrop-blur-xl rounded-3xl flex items-center justify-center border border-cyan-400/30 shadow-2xl">
                  <FaShip className="text-4xl text-cyan-400" />
                </div>
                <div>
                  <h1 className="text-5xl xl:text-6xl font-bold bg-gradient-to-r from-white via-cyan-100 to-teal-200 bg-clip-text text-transparent">
                    Ocean Intelligence Hub
                  </h1>
                  <p className="text-xl text-cyan-400 font-semibold mt-2">Smart Livelihood Support System</p>
                  
                </div>
              </div>
              <p className="text-xl text-slate-300 max-w-3xl mb-8 leading-relaxed">
                Empowering coastal communities with AI-driven ocean intelligence. Real-time monitoring, 
                multilingual support, and offline capabilities for pearl cultivators, divers, salt manufacturers, and aquaculture operators.
              </p>
            </motion.div>

            {/* Quick Actions */}
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, delay: 0.3 }}
              className="flex flex-col sm:flex-row gap-4 mt-8 xl:mt-0"
            >
              <motion.button 
                onClick={() => navigate('/chatbot')}
                className="group px-8 py-4 bg-gradient-to-r from-cyan-500 to-teal-600 text-white rounded-2xl font-semibold hover:from-cyan-400 hover:to-teal-500 transition-all duration-300 flex items-center space-x-3 shadow-2xl border border-cyan-400/30"
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.95 }}
              >
                <FaRocket className="text-lg group-hover:animate-bounce" />
                <span>Ocean Bot Assistant</span>
              </motion.button>
              
            </motion.div>
          </div>
        </div>
      </header>

      {/* Role Selection */}
      <section className="py-8 bg-gradient-to-r from-slate-800/30 to-slate-700/30 backdrop-blur-sm">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="grid grid-cols-2 lg:grid-cols-4 gap-4"
          >
            {roles.map((role, index) => (
              <motion.button
                key={role.id}
                onClick={() => setActiveRole(role.id)}
                className={`relative group p-6 rounded-2xl border transition-all duration-300 ${
                  activeRole === role.id
                    ? `bg-gradient-to-r ${role.color}/20 border-cyan-400/50 shadow-2xl`
                    : 'bg-slate-800/50 border-slate-700/50 hover:border-cyan-400/30'
                }`}
                whileHover={{ scale: 1.02, y: -2 }}
                whileTap={{ scale: 0.98 }}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.1 * index }}
              >
                <div className="text-center">
                  <div className={`w-12 h-12 bg-gradient-to-r ${role.color} rounded-xl flex items-center justify-center mx-auto mb-3 group-hover:scale-110 transition-transform duration-300`}>
                    <role.icon className="text-2xl text-white" />
                  </div>
                  <h3 className="text-lg font-semibold text-white mb-1">{role.name}</h3>
                  <p className="text-sm text-slate-400 mb-2">{role.description}</p>
                  <div className="text-2xl font-bold text-cyan-400">{role.count}</div>
                  <div className="text-xs text-slate-500">Active Users</div>
                </div>
                {activeRole === role.id && (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="absolute top-2 right-2 w-3 h-3 bg-green-400 rounded-full"
                  />
                )}
              </motion.button>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Main Dashboard */}
      <main className="container mx-auto px-6 py-12">
        
        {/* Live Alerts Section */}
        <AnimatePresence>
          {alertsVisible && (
            <motion.section
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mb-12"
            >
              <div className="bg-gradient-to-r from-slate-800/60 to-slate-700/60 backdrop-blur-xl rounded-3xl p-8 border border-slate-600/50 shadow-2xl">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-3xl font-bold text-white flex items-center">
                    <FaBell className="text-cyan-400 mr-4 text-2xl" />
                    Live Alerts & Advisories
                  </h2>
                  <motion.button
                    onClick={() => setAlertsVisible(false)}
                    className="text-slate-400 hover:text-white transition-colors duration-300"
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                  >
                    <FaCompress className="text-xl" />
                  </motion.button>
                </div>
                <div className="grid md:grid-cols-3 gap-4">
                  {currentRoleData.alerts.map((alert, index) => {
                    const AlertIcon = alertTypes[alert.type].icon;
                    const alertColor = alertTypes[alert.type].color;
                    return (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.5, delay: index * 0.1 }}
                        className={`p-4 rounded-xl border-l-4 bg-slate-700/50 border-${alertColor}-400`}
                      >
                        <div className="flex items-start space-x-3">
                          <AlertIcon className={`text-${alertColor}-400 text-xl mt-1`} />
                          <div className="flex-1">
                            <p className="text-white text-sm font-medium">{alert.message}</p>
                            <p className="text-slate-400 text-xs mt-1">{alert.time}</p>
                          </div>
                        </div>
                      </motion.div>
                    );
                  })}
                </div>
              </div>
            </motion.section>
          )}
        </AnimatePresence>

        {/* Metrics Dashboard */}
        <section className="mb-12">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="grid md:grid-cols-2 xl:grid-cols-4 gap-6"
          >
            {currentRoleData.metrics.map((metric, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="bg-gradient-to-br from-slate-800/60 to-slate-700/60 backdrop-blur-xl rounded-2xl p-6 border border-slate-600/50 shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-105"
              >
                <div className="flex items-center justify-between mb-4">
                  <metric.icon className="text-3xl text-cyan-400" />
                  {getTrendIcon(metric.trend)}
                </div>
                <h3 className="text-slate-400 text-sm font-medium mb-2">{metric.label}</h3>
                <div className="flex items-center justify-between">
                  <span className="text-2xl font-bold text-white">{metric.value}</span>
                  <span className={`text-sm font-semibold ${getStatusColor(metric.status)}`}>
                    {metric.status}
                  </span>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </section>

        {/* Forecast Charts */}
        <section className="mb-12">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="bg-gradient-to-br from-slate-800/60 to-slate-700/60 backdrop-blur-xl rounded-3xl p-8 border border-slate-600/50 shadow-2xl"
          >
            <h2 className="text-3xl font-bold text-white mb-8 flex items-center">
              <FaChartLine className="text-cyan-400 mr-4" />
              AI-Powered Forecasts
            </h2>
            <div className="grid lg:grid-cols-2 gap-8">
              {currentRoleData.forecasts.map((forecast, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.2 }}
                  className="bg-slate-700/50 rounded-2xl p-6"
                >
                  <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
                    <FaTachometerAlt className="text-cyan-400 mr-3" />
                    {forecast.parameter}
                  </h3>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-slate-400">Current:</span>
                      <span className="text-2xl font-bold text-white">{forecast.current}</span>
                    </div>
                    <div className="relative h-16 bg-slate-800 rounded-lg p-2">
                      <div className="flex items-end justify-between h-full space-x-1">
                        {forecast.forecast.map((value, i) => (
                          <div key={i} className="flex-1 flex flex-col items-center">
                            <div
                              className="bg-gradient-to-t from-cyan-500 to-teal-400 rounded-sm w-full"
                              style={{
                                height: `${(value / Math.max(...forecast.forecast)) * 100}%`,
                                minHeight: '8px'
                              }}
                            />
                            <span className="text-xs text-slate-400 mt-1">Day {i + 1}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                    <div className="text-sm text-slate-400">
                      Optimal Range: {forecast.optimal[0]} - {forecast.optimal[1]}
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </section>

        {/* Action Cards */}
        <section className="mb-12">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="grid md:grid-cols-3 gap-6"
          >
            <div className="bg-gradient-to-br from-green-900/40 to-green-800/40 backdrop-blur-xl rounded-2xl p-6 border border-green-600/50">
              <FaLanguage className="text-3xl text-green-400 mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">Multilingual Support</h3>
              <p className="text-slate-300 text-sm mb-4">Available in 12 local languages with voice commands</p>
              <button className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-500 transition-colors duration-300">
                Change Language
              </button>
            </div>

            <div className="bg-gradient-to-br from-blue-900/40 to-blue-800/40 backdrop-blur-xl rounded-2xl p-6 border border-blue-600/50">
              <FaDownload className="text-3xl text-blue-400 mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">Offline Data Sync</h3>
              <p className="text-slate-300 text-sm mb-4">Download forecasts and alerts for offline access</p>
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-500 transition-colors duration-300">
                Sync Now
              </button>
            </div>

            <div className="bg-gradient-to-br from-purple-900/40 to-purple-800/40 backdrop-blur-xl rounded-2xl p-6 border border-purple-600/50">
              <FaSyncAlt className="text-3xl text-purple-400 mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">Real-time Updates</h3>
              <p className="text-slate-300 text-sm mb-4">Live monitoring with instant alert notifications</p>
              <button className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-500 transition-colors duration-300">
                View Updates
              </button>
            </div>
          </motion.div>
        </section>

       
      </main>
    </div>
  );
};