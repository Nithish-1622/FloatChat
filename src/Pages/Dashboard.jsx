import React, { useState, useEffect } from 'react'
import water from '../Assets/water.mp4'
import { useNavigate } from 'react-router-dom'
import { 
  FaRobot, 
  FaArrowRight, 
  FaWater, 
  FaFish, 
  FaLeaf, 
  FaChartLine, 
  FaGlobe, 
  FaDatabase,
  FaSearch,
  FaBell,
  FaUser,
  FaCog,
  FaBookmark,
  FaClock,
  FaEye,
  FaUsers
} from 'react-icons/fa'

export const Dashboard = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    users: 0,
    dataPoints: 0,
    queries: 0,
    accuracy: 0
  });

  // Animated counter effect
  useEffect(() => {
    const targetStats = {
      users: 15420,
      dataPoints: 2847365,
      queries: 98750,
      accuracy: 97.8
    };

    const animateCount = (key, target) => {
      const increment = target / 100;
      let current = 0;
      const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
          current = target;
          clearInterval(timer);
        }
        setStats(prev => ({
          ...prev,
          [key]: Math.floor(current)
        }));
      }, 20);
    };

    // Start animations after component mounts
    setTimeout(() => {
      Object.entries(targetStats).forEach(([key, value]) => {
        animateCount(key, value);
      });
    }, 500);
  }, []);

  const handleAsk = () => {
    navigate('/chatbot');
  }

  return (
    <div className="min-h-screen bg-slate-900">
      {/* Professional Navigation Bar - Fixed Height */}
      <nav className="fixed top-0 left-0 right-0 z-50 h-16 bg-slate-900/95 backdrop-blur-md border-b border-slate-700/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full">
          <div className="flex justify-between items-center h-full">
            {/* Logo Section */}
            <div className="flex items-center space-x-3">
              <FaWater className="text-2xl text-cyan-400" />
              <span className="text-xl font-bold text-white font-poppins">FloatChat</span>
            </div>

            {/* Navigation Links */}
            <div className="hidden md:flex items-center space-x-8">
              <a href="#home" className="text-slate-300 hover:text-cyan-400 transition-colors font-poppins">Home</a>
              <a href="#features" className="text-slate-300 hover:text-cyan-400 transition-colors font-poppins">Features</a>
              <a href="#about" className="text-slate-300 hover:text-cyan-400 transition-colors font-poppins">About</a>
              <a href="#contact" className="text-slate-300 hover:text-cyan-400 transition-colors font-poppins">Contact</a>
            </div>

            {/* Right Section */}
            <div className="flex items-center space-x-4">
              <FaSearch className="text-slate-300 hover:text-cyan-400 cursor-pointer transition-colors" />
              <FaBell className="text-slate-300 hover:text-cyan-400 cursor-pointer transition-colors" />
              <FaUser className="text-slate-300 hover:text-cyan-400 cursor-pointer transition-colors" />
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content - Starts after navbar */}
      <main className="pt-10">
        {/* Hero Section */}
        <section className="relative w-full h-screen">
          {/* Video Background */}
          <video
            className="absolute inset-0 w-full h-full object-cover"
            autoPlay
            loop
            muted
          >
            <source src={water} type="video/mp4" />
          </video>

          {/* Gradient Overlay */}
          <div className="absolute inset-0 bg-gradient-to-b from-slate-900/80 via-slate-900/60 to-slate-900/90"></div>

          {/* Content */}
          <div className="relative z-10 h-full flex items-center justify-center px-4">
            <div className="text-center max-w-5xl space-y-8">
              {/* Logo and Title */}
              <div className="flex items-center justify-center space-x-4 mb-6">
                <div className="p-3 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full">
                  <FaRobot className="text-3xl text-white" />
                </div>
                <h1 className="text-6xl md:text-7xl font-bold font-poppins tracking-tight bg-gradient-to-r from-white to-cyan-200 bg-clip-text text-transparent">
                  Float Chat
                </h1>
              </div>

              {/* Description */}
              <div className="space-y-4">
                <p className="text-slate-200 text-2xl md:text-3xl font-light max-w-3xl mx-auto leading-relaxed">
                  Dive into the future of ocean exploration
                </p>
                <p className="text-cyan-300 text-lg md:text-xl font-medium max-w-2xl mx-auto">
                  Powered by advanced AI algorithms for real-time ocean data insights
                </p>
              </div>

              {/* Statistics Row */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto py-4">
                <StatCard number={stats.users.toLocaleString()} label="Active Users" icon={FaUsers} />
                <StatCard number={stats.dataPoints.toLocaleString()} label="Data Points" icon={FaDatabase} />
                <StatCard number={stats.queries.toLocaleString()} label="Queries Answered" icon={FaChartLine} />
                <StatCard number={`${stats.accuracy}%`} label="Accuracy Rate" icon={FaEye} />
              </div>

              {/* CTA Buttons */}
              <div className="flex flex-col sm:flex-row gap-6 justify-center pt-4">
                <button 
                  onClick={handleAsk}
                  className="group relative inline-flex items-center justify-center px-10 py-4 font-poppins text-xl font-semibold text-white bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-500 rounded-full shadow-2xl transition-all duration-300 hover:scale-105 hover:shadow-cyan-500/30"
                >
                  <span className="relative z-10">Start Exploring</span>
                  <FaArrowRight className="ml-3 group-hover:translate-x-1 transition-transform relative z-10" />
                </button>
              
              </div>
            </div>
          </div>
        </section>

        {/* Wave Separator */}
        <div className="relative w-full bg-slate-900">
          <svg
            className="w-full h-24"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 1200 120"
            preserveAspectRatio="none"
          >
            <defs>
              <linearGradient id="waveSeparator" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stopColor="#0f172a" stopOpacity="0.8" />
                <stop offset="50%" stopColor="#0f172a" stopOpacity="0.9" />
                <stop offset="100%" stopColor="#0f172a" stopOpacity="1" />
              </linearGradient>
            </defs>
            <path
              d="M0,60L48,65C96,70,192,80,288,75C384,70,480,50,576,45C672,40,768,50,864,60C960,70,1056,80,1152,75L1200,70L1200,120L1152,120C1056,120,960,120,864,120C768,120,672,120,576,120C480,120,384,120,288,120C192,120,96,120,48,120L0,120Z"
              fill="url(#waveSeparator)"
            />
          </svg>
          
          
          {/* Animated Wave Overlay */}
          <svg
            className="absolute top-0 w-full h-24 opacity-60"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 1200 120"
            preserveAspectRatio="none"
          >
            <path
              d="M0,40L48,50C96,60,192,80,288,85C384,90,480,80,576,70C672,60,768,50,864,55C960,60,1056,80,1152,85L1200,90L1200,120L1152,120C1056,120,960,120,864,120C768,120,672,120,576,120C480,120,384,120,288,120C192,120,96,120,48,120L0,120Z"
              fill="rgba(6, 182, 212, 0.1)"
              className="animate-pulse"
            />
          </svg>
        </div>
       
        {/* Quick Actions Section */}
        <section className="w-full py-20 px-4 bg-slate-900">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-white mb-4 font-poppins">Quick Actions</h2>
              <div className="w-24 h-1 bg-gradient-to-r from-cyan-500 to-blue-500 mx-auto mb-4"></div>
              <p className="text-xl text-slate-400 max-w-2xl mx-auto">Access powerful tools for ocean data analysis</p>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              <QuickActionCard 
                icon={FaSearch} 
                title="Search Data" 
                description="Find specific ocean data with advanced filters"
                color="cyan"
              />
              <QuickActionCard 
                icon={FaBookmark} 
                title="Saved Queries" 
                description="Access your bookmarked searches"
                color="blue"
              />
              <QuickActionCard 
                icon={FaClock} 
                title="Recent Activity" 
                description="View your exploration history"
                color="purple"
              />
              <QuickActionCard 
                icon={FaCog} 
                title="Settings" 
                description="Customize your dashboard experience"
                color="green"
              />
            </div>
          </div>
        </section>

   

        {/* Features Section */}
        <section className='w-full py-20 px-4 bg-gradient-to-b from-slate-800 to-slate-900' id="features">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-white mb-4 font-poppins">Powerful Features</h2>
              <div className="w-32 h-1 bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-500 mx-auto mb-4"></div>
              <p className="text-xl text-slate-300 max-w-3xl mx-auto font-poppins leading-relaxed">
                Explore our comprehensive suite of ocean data analysis tools designed for professionals
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              <FeatureCard 
                icon={FaDatabase}
                title="Ocean Data Analytics"
                description="Access real-time ocean data and insights powered by advanced AI algorithms with comprehensive reporting tools"
                gradient="from-cyan-500 to-blue-500"
              />
              <FeatureCard 
                icon={FaFish}
                title="Marine Life Intelligence"
                description="Learn about diverse marine species and their ecosystems with detailed biological and behavioral information"
                gradient="from-blue-500 to-purple-500"
              />
              <FeatureCard 
                icon={FaLeaf}
                title="Conservation Tools"
                description="Discover how to contribute to ocean conservation efforts and sustainability with actionable insights"
                gradient="from-green-500 to-teal-500"
              />
              <FeatureCard 
                icon={FaChartLine}
                title="Advanced Analytics"
                description="Powerful analytics tools for data visualization, trend analysis, and predictive modeling capabilities"
                gradient="from-purple-500 to-pink-500"
              />
              <FeatureCard 
                icon={FaGlobe}
                title="Global Coverage"
                description="Worldwide ocean monitoring with satellite data integration and comprehensive sensor networks"
                gradient="from-orange-500 to-red-500"
              />
              <FeatureCard 
                icon={FaRobot}
                title="AI Assistant"
                description="Intelligent chatbot powered by machine learning for instant answers and personalized recommendations"
                gradient="from-indigo-500 to-cyan-500"
              />
            </div>
          </div>
        </section>

        {/* Technology Section */}
        <section className="w-full py-16 px-4 bg-slate-900">
          <div className="max-w-6xl mx-auto text-center">
            <h3 className="text-3xl font-bold text-white mb-8 font-poppins">Built with Cutting-Edge Technology</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              <TechCard title="AI/ML" description="Advanced algorithms" />
              <TechCard title="Real-time" description="Live data streams" />
              <TechCard title="Cloud" description="Scalable infrastructure" />
              <TechCard title="Security" description="Enterprise-grade" />
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}

// Statistics Card Component
const StatCard = ({ number, label, icon: Icon }) => (
  <div className="bg-slate-800/70 backdrop-blur-sm rounded-xl p-4 border border-slate-700/50 hover:border-cyan-500/30 transition-all duration-300 group hover:scale-105">
    <div className="flex items-center justify-center mb-3">
      <div className="p-2 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full group-hover:scale-110 transition-transform">
        <Icon className="text-lg text-white" />
      </div>
    </div>
    <div className="text-2xl font-bold text-white text-center mb-1">{number}</div>
    <div className="text-sm text-slate-400 text-center font-medium">{label}</div>
  </div>
);

// Quick Action Card Component
const QuickActionCard = ({ icon: Icon, title, description, color }) => {
  const colorClasses = {
    cyan: 'hover:border-cyan-500/50 hover:bg-cyan-500/10',
    blue: 'hover:border-blue-500/50 hover:bg-blue-500/10',
    purple: 'hover:border-purple-500/50 hover:bg-purple-500/10',
    green: 'hover:border-green-500/50 hover:bg-green-500/10'
  };

  return (
    <div className={`p-6 rounded-xl bg-slate-800/50 border border-slate-700 transition-all duration-300 cursor-pointer ${colorClasses[color]} group hover:scale-105`}>
      <Icon className={`text-2xl text-${color}-400 mb-3 group-hover:scale-110 transition-transform`} />
      <h3 className="text-lg font-semibold text-white mb-2">{title}</h3>
      <p className="text-slate-400">{description}</p>
    </div>
  );
};

// Feature Card Component
const FeatureCard = ({ icon: Icon, title, description, gradient }) => (
  <div className="group p-6 rounded-xl bg-gradient-to-b from-slate-800 to-slate-800/50 border border-slate-700 hover:border-cyan-500/50 transition-all duration-300 hover:scale-105">
    <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${gradient} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
      <Icon className="text-white text-xl" />
    </div>
    <h3 className="text-xl font-semibold text-white mb-3 group-hover:text-cyan-400 transition-colors">
      {title}
    </h3>
    <p className="text-slate-400 leading-relaxed">
      {description}
    </p>
  </div>
);

// Technology Card Component
const TechCard = ({ title, description }) => (
  <div className="p-4 rounded-lg bg-slate-800/50 border border-slate-700 hover:border-cyan-500/30 transition-all duration-300 group">
    <h4 className="text-lg font-semibold text-white mb-1 group-hover:text-cyan-400 transition-colors">{title}</h4>
    <p className="text-slate-400 text-sm">{description}</p>
  </div>
);
