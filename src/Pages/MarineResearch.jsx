import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  FaDatabase, FaArrowLeft, FaChartBar, FaLeaf, FaFlask, 
  FaFileExport, FaSearch, FaMicroscope, FaGraduationCap,
  FaBook, FaCode, FaDownload, FaShare, FaCog, FaFilter,
  FaPlay, FaPause, FaExpand, FaCompress, FaLayerGroup,
  FaGlobe, FaLightbulb, FaRocket, FaUsers, FaShieldAlt,
  FaLanguage, FaWifi, FaLock, FaEye, FaChartLine,
  FaTable, FaMap, FaBrain, FaAtom, FaDna, FaTree,
  FaThermometerHalf, FaWater, FaFish, FaClipboardList,
  FaSyncAlt, FaCloudDownloadAlt, FaExternalLinkAlt,
  FaStar, FaHeart, FaBookmark, FaInfoCircle, FaBell,
  FaCalendarAlt, FaClock, FaUserFriends, FaAward,
  FaChevronRight, FaChevronDown, FaTags, FaHashtag
} from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

export const MarineResearch = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('datasets');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [isNotebookOpen, setIsNotebookOpen] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const tabs = [
    { id: 'datasets', name: 'Curated Datasets', icon: FaDatabase, color: 'from-blue-500 to-cyan-500' },
    { id: 'visualizations', name: 'Data Visualizations', icon: FaChartBar, color: 'from-purple-500 to-pink-500' },
    { id: 'biodiversity', name: 'Biodiversity Indices', icon: FaLeaf, color: 'from-green-500 to-teal-500' },
    { id: 'sandbox', name: 'Research Sandbox', icon: FaFlask, color: 'from-orange-500 to-red-500' },
    { id: 'exports', name: 'FAIR Exports', icon: FaFileExport, color: 'from-indigo-500 to-purple-500' }
  ];

  const datasetCategories = [
    { id: 'all', name: 'All Datasets', count: 1247, icon: FaGlobe },
    { id: 'climate', name: 'Climate Data', count: 324, icon: FaThermometerHalf },
    { id: 'fisheries', name: 'Fisheries', count: 189, icon: FaFish },
    { id: 'biodiversity', name: 'Biodiversity', count: 567, icon: FaDna },
    { id: 'coastal', name: 'Coastal Change', count: 167, icon: FaWater }
  ];

  const featuredDatasets = [
    {
      id: 1,
      title: 'Indian Ocean Temperature Trends 2000-2024',
      description: 'Comprehensive temperature analysis with climate change indicators',
      format: ['NetCDF', 'CSV'],
      size: '2.4 GB',
      downloads: 1247,
      stars: 89,
      category: 'climate',
      lastUpdated: '2 days ago',
      doi: '10.5194/essd-2024-001',
      tags: ['temperature', 'climate', 'trends', 'indian-ocean']
    },
    {
      id: 2,
      title: 'Coral Reef Biodiversity Mapping - Bay of Bengal',
      description: 'Species distribution and ecosystem health assessment',
      format: ['JSON', 'GeoJSON'],
      size: '856 MB',
      downloads: 623,
      stars: 67,
      category: 'biodiversity',
      lastUpdated: '1 week ago',
      doi: '10.1038/s41597-024-002',
      tags: ['coral', 'biodiversity', 'bay-of-bengal', 'ecosystem']
    },
    {
      id: 3,
      title: 'Fisheries Production Analysis - Arabian Sea',
      description: 'Commercial fishing data with sustainability metrics',
      format: ['CSV', 'Excel'],
      size: '1.2 GB',
      downloads: 934,
      stars: 45,
      category: 'fisheries',
      lastUpdated: '3 days ago',
      doi: '10.1016/j.dib.2024.003',
      tags: ['fisheries', 'arabian-sea', 'sustainability', 'production']
    }
  ];

  const visualizationTools = [
    {
      id: 1,
      name: 'Ocean Temperature Heatmap',
      description: 'Interactive temperature visualization across Indian Ocean',
      type: 'Heatmap',
      datasets: 3,
      icon: FaThermometerHalf,
      color: 'from-red-500 to-orange-500'
    },
    {
      id: 2,
      name: 'Species Distribution Maps',
      description: 'Biodiversity hotspots and species migration patterns',
      type: 'Choropleth',
      datasets: 8,
      icon: FaDna,
      color: 'from-green-500 to-emerald-500'
    },
    {
      id: 3,
      name: 'Time Series Analysis',
      description: 'Temporal trends in ocean parameters',
      type: 'Line Chart',
      datasets: 12,
      icon: FaChartLine,
      color: 'from-blue-500 to-cyan-500'
    },
    {
      id: 4,
      name: 'Ecosystem Stress Dashboard',
      description: 'Real-time monitoring of ecosystem health indicators',
      type: 'Dashboard',
      datasets: 6,
      icon: FaLeaf,
      color: 'from-purple-500 to-pink-500'
    }
  ];

  const biodiversityMetrics = [
    { label: 'Species Richness Index', value: '847', status: 'stable', trend: 'neutral', icon: FaDna },
    { label: 'Ecosystem Health Score', value: '7.2/10', status: 'moderate', trend: 'declining', icon: FaLeaf },
    { label: 'Habitat Vulnerability', value: 'Medium', status: 'warning', trend: 'increasing', icon: FaTree },
    { label: 'Ocean Acidification', value: '8.1 pH', status: 'critical', trend: 'declining', icon: FaAtom }
  ];

  const researchProjects = [
    {
      id: 1,
      title: 'Climate Impact on Coral Ecosystems',
      author: 'Dr. Priya Sharma, INCOIS',
      language: 'Python',
      notebooks: 12,
      stars: 89,
      forks: 23,
      lastActive: '2 hours ago',
      description: 'Analyzing temperature stress on coral reef systems using ML models'
    },
    {
      id: 2,
      title: 'Fisheries Sustainability Assessment',
      author: 'Prof. Raj Kumar, IIT Chennai',
      language: 'R',
      notebooks: 8,
      stars: 67,
      forks: 15,
      lastActive: '1 day ago',
      description: 'Predictive modeling for sustainable fishing practices'
    },
    {
      id: 3,
      title: 'Ocean Pollution Tracking',
      author: 'Dr. Anita Singh, NIO Goa',
      language: 'Python',
      notebooks: 15,
      stars: 134,
      forks: 45,
      lastActive: '3 hours ago',
      description: 'Machine learning approaches to pollution source identification'
    }
  ];

  const getStatusColor = (status) => {
    const colors = {
      stable: 'text-green-400',
      moderate: 'text-yellow-400',
      warning: 'text-orange-400',
      critical: 'text-red-400'
    };
    return colors[status] || 'text-slate-400';
  };

  const getTrendIcon = (trend) => {
    if (trend === 'increasing') return '↗️';
    if (trend === 'declining') return '↘️';
    return '→';
  };

  const renderDatasets = () => (
    <div className="space-y-8">
      {/* Dataset Categories */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        {datasetCategories.map((category, index) => (
          <motion.button
            key={category.id}
            onClick={() => setSelectedCategory(category.id)}
            className={`p-4 rounded-xl border transition-all duration-300 ${
              selectedCategory === category.id
                ? 'bg-cyan-500/20 border-cyan-400/50'
                : 'bg-slate-800/50 border-slate-700/50 hover:border-cyan-400/30'
            }`}
            whileHover={{ scale: 1.02 }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <category.icon className="text-2xl text-cyan-400 mx-auto mb-2" />
            <div className="text-sm font-medium text-white">{category.name}</div>
            <div className="text-xs text-slate-400">{category.count} datasets</div>
          </motion.button>
        ))}
      </div>

      {/* Featured Datasets */}
      <div className="space-y-4">
        <h3 className="text-2xl font-bold text-white flex items-center">
          <FaStar className="text-yellow-400 mr-3" />
          Featured Datasets
        </h3>
        <div className="grid gap-6">
          {featuredDatasets.map((dataset, index) => (
            <motion.div
              key={dataset.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="bg-slate-800/60 backdrop-blur-xl rounded-2xl p-6 border border-slate-600/50 hover:border-cyan-400/50 transition-all duration-300"
            >
              <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-4">
                <div className="flex-1">
                  <h4 className="text-xl font-semibold text-white mb-2">{dataset.title}</h4>
                  <p className="text-slate-300 mb-3">{dataset.description}</p>
                  <div className="flex flex-wrap gap-2 mb-3">
                    {dataset.tags.map((tag, i) => (
                      <span key={i} className="px-2 py-1 bg-cyan-500/20 text-cyan-300 text-xs rounded-md">
                        #{tag}
                      </span>
                    ))}
                  </div>
                </div>
                <div className="flex flex-col items-end space-y-2">
                  <div className="flex items-center space-x-4 text-sm text-slate-400">
                    <span className="flex items-center">
                      <FaDownload className="mr-1" /> {dataset.downloads}
                    </span>
                    <span className="flex items-center">
                      <FaStar className="mr-1 text-yellow-400" /> {dataset.stars}
                    </span>
                  </div>
                  <div className="text-xs text-slate-500">DOI: {dataset.doi}</div>
                </div>
              </div>
              
              <div className="flex flex-wrap items-center justify-between pt-4 border-t border-slate-600/50">
                <div className="flex items-center space-x-4 text-sm text-slate-400">
                  <span>Size: {dataset.size}</span>
                  <span>Updated: {dataset.lastUpdated}</span>
                  <div className="flex space-x-1">
                    {dataset.format.map((fmt, i) => (
                      <span key={i} className="px-2 py-1 bg-blue-500/20 text-blue-300 text-xs rounded">
                        {fmt}
                      </span>
                    ))}
                  </div>
                </div>
                <div className="flex space-x-2">
                  <button className="px-4 py-2 bg-cyan-600 text-white rounded-lg hover:bg-cyan-500 transition-colors duration-300 flex items-center space-x-2">
                    <FaDownload />
                    <span>Download</span>
                  </button>
                  <button className="px-4 py-2 bg-slate-600 text-white rounded-lg hover:bg-slate-500 transition-colors duration-300">
                    <FaEye />
                  </button>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderVisualizations = () => (
    <div className="grid md:grid-cols-2 gap-6">
      {visualizationTools.map((tool, index) => (
        <motion.div
          key={tool.id}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: index * 0.1 }}
          className="bg-gradient-to-br from-slate-800/60 to-slate-700/60 backdrop-blur-xl rounded-2xl p-6 border border-slate-600/50 hover:shadow-2xl transition-all duration-300"
        >
          <div className={`w-16 h-16 bg-gradient-to-r ${tool.color} rounded-xl flex items-center justify-center mb-4`}>
            <tool.icon className="text-3xl text-white" />
          </div>
          <h3 className="text-xl font-semibold text-white mb-2">{tool.name}</h3>
          <p className="text-slate-300 mb-4">{tool.description}</p>
          <div className="flex items-center justify-between mb-4">
            <span className="text-sm text-slate-400">Type: {tool.type}</span>
            <span className="text-sm text-slate-400">{tool.datasets} datasets</span>
          </div>
          <button className="w-full py-3 bg-gradient-to-r from-cyan-500 to-teal-600 text-white rounded-xl font-semibold hover:from-cyan-400 hover:to-teal-500 transition-all duration-300">
            Launch Visualization
          </button>
        </motion.div>
      ))}
    </div>
  );

  const renderBiodiversity = () => (
    <div className="space-y-8">
      {/* Biodiversity Metrics */}
      <div className="grid md:grid-cols-2 xl:grid-cols-4 gap-6">
        {biodiversityMetrics.map((metric, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: index * 0.1 }}
            className="bg-slate-800/60 backdrop-blur-xl rounded-2xl p-6 border border-slate-600/50"
          >
            <div className="flex items-center justify-between mb-4">
              <metric.icon className="text-3xl text-cyan-400" />
              <span className="text-2xl">{getTrendIcon(metric.trend)}</span>
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
      </div>

      {/* Ecosystem Map */}
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="bg-slate-800/60 backdrop-blur-xl rounded-3xl p-8 border border-slate-600/50"
      >
        <h3 className="text-2xl font-bold text-white mb-6 flex items-center">
          <FaMap className="text-cyan-400 mr-3" />
          Interactive Ecosystem Map
        </h3>
        <div className="h-96 bg-slate-700/50 rounded-2xl flex items-center justify-center">
          <div className="text-center">
            <FaGlobe className="text-6xl text-cyan-400 mx-auto mb-4" />
            <p className="text-xl text-slate-300">Interactive map loading...</p>
            <p className="text-slate-400">Click to explore biodiversity hotspots</p>
          </div>
        </div>
      </motion.div>
    </div>
  );

  const renderSandbox = () => (
    <div className="space-y-8">
      {/* Notebook Interface */}
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="bg-slate-800/60 backdrop-blur-xl rounded-3xl p-8 border border-slate-600/50"
      >
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-2xl font-bold text-white flex items-center">
            <FaCode className="text-cyan-400 mr-3" />
            Jupyter Notebook Environment
          </h3>
          <button
            onClick={() => setIsNotebookOpen(!isNotebookOpen)}
            className="px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl font-semibold hover:from-green-400 hover:to-emerald-500 transition-all duration-300"
          >
            {isNotebookOpen ? 'Close Notebook' : 'Launch Notebook'}
          </button>
        </div>

        {isNotebookOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            className="bg-slate-900 rounded-2xl p-6 border border-slate-600"
          >
            <div className="flex items-center space-x-4 mb-4">
              <div className="flex space-x-2">
                <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              </div>
              <span className="text-slate-400 text-sm">ocean_research_notebook.ipynb</span>
            </div>
            <div className="bg-slate-800 rounded-lg p-4 font-mono text-sm">
              <div className="text-green-400"># Ocean Data Analysis Notebook</div>
              <div className="text-blue-400">import pandas as pd</div>
              <div className="text-blue-400">import oceaniq as oiq</div>
              <div className="text-slate-300">
                <br />
                <span className="text-yellow-400"># Load Indian Ocean temperature data</span>
                <br />
                data = oiq.load_dataset('indian_ocean_temp_2024')
                <br />
                print(f"Dataset shape: {data.shape}")
              </div>
            </div>
          </motion.div>
        )}
      </motion.div>

      {/* Research Projects */}
      <div className="space-y-4">
        <h3 className="text-2xl font-bold text-white flex items-center">
          <FaUsers className="text-cyan-400 mr-3" />
          Collaborative Research Projects
        </h3>
        <div className="grid gap-4">
          {researchProjects.map((project, index) => (
            <motion.div
              key={project.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="bg-slate-800/60 backdrop-blur-xl rounded-2xl p-6 border border-slate-600/50 hover:border-cyan-400/50 transition-all duration-300"
            >
              <div className="flex justify-between items-start mb-4">
                <div className="flex-1">
                  <h4 className="text-xl font-semibold text-white mb-2">{project.title}</h4>
                  <p className="text-slate-300 mb-2">{project.description}</p>
                  <p className="text-slate-400 text-sm">{project.author}</p>
                </div>
                <div className="flex items-center space-x-4 text-sm text-slate-400">
                  <span className="flex items-center">
                    <FaStar className="mr-1 text-yellow-400" /> {project.stars}
                  </span>
                  <span className="flex items-center">
                    <FaCodeBranch className="mr-1" /> {project.forks}
                  </span>
                </div>
              </div>
              
              <div className="flex items-center justify-between pt-4 border-t border-slate-600/50">
                <div className="flex items-center space-x-4 text-sm text-slate-400">
                  <span className="px-2 py-1 bg-blue-500/20 text-blue-300 rounded">{project.language}</span>
                  <span>{project.notebooks} notebooks</span>
                  <span>Active {project.lastActive}</span>
                </div>
                <button className="px-4 py-2 bg-cyan-600 text-white rounded-lg hover:bg-cyan-500 transition-colors duration-300">
                  Fork Project
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderExports = () => (
    <div className="space-y-8">
      {/* FAIR Compliance */}
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="bg-gradient-to-br from-indigo-900/40 to-purple-900/40 backdrop-blur-xl rounded-3xl p-8 border border-indigo-600/50"
      >
        <h3 className="text-3xl font-bold text-white mb-6 flex items-center">
          <FaAward className="text-indigo-400 mr-4" />
          FAIR Data Principles
        </h3>
        <div className="grid md:grid-cols-2 xl:grid-cols-4 gap-6">
          {[
            { label: 'Findable', icon: FaSearch, desc: 'Metadata and identifiers' },
            { label: 'Accessible', icon: FaDownload, desc: 'Retrievable protocols' },
            { label: 'Interoperable', icon: FaSyncAlt, desc: 'Standard vocabularies' },
            { label: 'Reusable', icon: FaRecycle, desc: 'Clear usage licenses' }
          ].map((principle, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="text-center p-6 bg-slate-800/50 rounded-2xl"
            >
              <principle.icon className="text-4xl text-indigo-400 mx-auto mb-3" />
              <h4 className="text-lg font-semibold text-white mb-2">{principle.label}</h4>
              <p className="text-slate-300 text-sm">{principle.desc}</p>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* DOI Assignment */}
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.2 }}
        className="bg-slate-800/60 backdrop-blur-xl rounded-3xl p-8 border border-slate-600/50"
      >
        <h3 className="text-2xl font-bold text-white mb-6 flex items-center">
          <FaExternalLinkAlt className="text-cyan-400 mr-3" />
          DOI Assignment & Publication
        </h3>
        <div className="grid md:grid-cols-2 gap-8">
          <div className="space-y-4">
            <h4 className="text-lg font-semibold text-white">Dataset Publishing</h4>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg">
                <span className="text-slate-300">Title & Description</span>
                <span className="text-green-400">✓ Complete</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg">
                <span className="text-slate-300">Metadata Schema</span>
                <span className="text-green-400">✓ Validated</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg">
                <span className="text-slate-300">License Assignment</span>
                <span className="text-yellow-400">⚠ Pending</span>
              </div>
            </div>
            <button className="w-full py-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-xl font-semibold hover:from-indigo-400 hover:to-purple-500 transition-all duration-300">
              Generate DOI
            </button>
          </div>
          
          <div className="space-y-4">
            <h4 className="text-lg font-semibold text-white">Export Formats</h4>
            <div className="grid grid-cols-2 gap-3">
              {['BibTeX', 'EndNote', 'RIS', 'DataCite XML'].map((format, i) => (
                <button
                  key={i}
                  className="p-3 bg-slate-700/50 text-slate-300 rounded-lg hover:bg-slate-600/50 transition-colors duration-300"
                >
                  {format}
                </button>
              ))}
            </div>
            <div className="mt-6 p-4 bg-slate-900 rounded-lg">
              <div className="text-xs text-slate-400 mb-2">Citation Preview:</div>
              <div className="text-sm text-slate-300 font-mono">
                Sharma, P. et al. (2024). Indian Ocean Temperature Trends 2000-2024. 
                OceanIQ Research Platform. DOI: 10.5194/essd-2024-001
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );

  const getTabContent = () => {
    switch (activeTab) {
      case 'datasets': return renderDatasets();
      case 'visualizations': return renderVisualizations();
      case 'biodiversity': return renderBiodiversity();
      case 'sandbox': return renderSandbox();
      case 'exports': return renderExports();
      default: return renderDatasets();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-indigo-950 to-purple-950 relative overflow-hidden">
      
      {/* Background Elements */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-900/20 via-transparent to-transparent"></div>
      <div className="absolute top-0 left-0 w-full h-full">
        <div className="absolute top-20 left-20 w-64 h-64 bg-indigo-500/5 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-purple-500/5 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      {/* Header */}
      <header className="relative bg-gradient-to-r from-slate-900/95 via-indigo-900/95 to-slate-900/95 backdrop-blur-xl border-b border-slate-700/50 shadow-2xl">
        <div className="container mx-auto px-6 py-8">
          
          {/* Back Button */}
          <motion.button
            onClick={() => navigate(-1)}
            className="inline-flex items-center space-x-3 text-indigo-400 hover:text-indigo-300 transition-all duration-300 mb-10 p-3 rounded-xl hover:bg-slate-800/50"
            whileHover={{ x: -8, scale: 1.05 }}
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            <FaArrowLeft className="text-lg" />
            <span className="font-semibold">Back to Dashboard</span>
          </motion.button>

          {/* Header Content */}
          <div className="flex flex-col xl:flex-row justify-center items-center xl:items-center">
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="flex-1"
            >
              <div className="flex items-center space-x-6 mb-6">
                <div className="relative w-20 h-20 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 backdrop-blur-xl rounded-3xl flex items-center justify-center border border-indigo-400/30 shadow-2xl">
                  <FaMicroscope className="text-4xl text-indigo-400" />
                </div>
                <div>
                  <h1 className="text-5xl xl:text-6xl font-bold bg-gradient-to-r from-white via-indigo-100 to-purple-200 bg-clip-text text-transparent">
                    Research & Academia
                  </h1>
                  <p className="text-xl text-indigo-400 font-semibold mt-2">Unlocking Knowledge from Ocean Data</p>
                  
                </div>
              </div>
              <p className="text-xl text-slate-300 max-w-4xl mb-10 leading-relaxed">
                Empowering scientists and researchers with curated datasets, advanced visualization tools, 
                and reproducible workflows. Transform raw ocean data into publication-ready insights with 
                FAIR compliance and DOI assignment capabilities.
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
                className="group px-8 py-4 bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-2xl font-semibold hover:from-indigo-400 hover:to-purple-500 transition-all duration-300 flex items-center space-x-3 shadow-2xl border border-indigo-400/30"
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.95 }}
              >
                <FaBrain className="text-lg group-hover:animate-pulse" />
                <span>Research Assistant</span>
              </motion.button>

            </motion.div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <section className="py-8 bg-gradient-to-r from-slate-800/30 to-indigo-800/30 backdrop-blur-sm">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="flex flex-wrap gap-4 justify-center"
          >
            {tabs.map((tab, index) => (
              <motion.button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-3 px-6 py-4 rounded-2xl border transition-all duration-300 ${
                  activeTab === tab.id
                    ? `bg-gradient-to-r ${tab.color}/20 border-indigo-400/50 shadow-2xl`
                    : 'bg-slate-800/50 border-slate-700/50 hover:border-indigo-400/30'
                }`}
                whileHover={{ scale: 1.02, y: -2 }}
                whileTap={{ scale: 0.98 }}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.1 * index }}
              >
                <tab.icon className="text-xl text-indigo-400" />
                <span className="font-medium text-white">{tab.name}</span>
                {activeTab === tab.id && (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="w-2 h-2 bg-green-400 rounded-full"
                  />
                )}
              </motion.button>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Search Bar */}
      <section className="py-6 bg-slate-800/20">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="relative max-w-2xl mx-auto"
          >
            <FaSearch className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400 text-lg" />
            <input
              type="text"
              placeholder="Search datasets, research projects, or publications..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-4 bg-slate-800/60 backdrop-blur-xl text-white placeholder-slate-400 rounded-2xl border border-slate-600/50 focus:border-indigo-400/50 focus:outline-none transition-all duration-300"
            />
          </motion.div>
        </div>
      </section>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-12">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -40 }}
            transition={{ duration: 0.6 }}
          >
            {getTabContent()}
          </motion.div>
        </AnimatePresence>
      </main>

      {/* CTA Section */}
      <section className="py-16">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="relative text-center bg-gradient-to-br from-indigo-900/30 via-purple-900/20 to-slate-900/30 backdrop-blur-xl rounded-4xl p-16 border border-indigo-500/30 shadow-2xl overflow-hidden"
          >
            <div className="absolute top-0 left-0 w-full h-full">
              <div className="absolute top-10 left-10 w-32 h-32 bg-indigo-500/10 rounded-full blur-2xl"></div>
              <div className="absolute bottom-10 right-10 w-48 h-48 bg-purple-500/10 rounded-full blur-3xl"></div>
            </div>
            
            <div className="relative z-10">
              <motion.div
                animate={{ 
                  rotate: [0, 360],
                  scale: [1, 1.1, 1]
                }}
                transition={{ 
                  duration: 20,
                  repeat: Infinity,
                  ease: "linear"
                }}
                className="w-24 h-24 bg-gradient-to-r from-indigo-400 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-8 shadow-2xl"
              >
                <FaGraduationCap className="text-4xl text-white" />
              </motion.div>
              
              <h2 className="text-5xl font-bold bg-gradient-to-r from-white via-indigo-200 to-purple-300 bg-clip-text text-transparent mb-6">
                Accelerate Ocean Research
              </h2>
              <p className="text-xl text-slate-300 mb-12 max-w-4xl mx-auto leading-relaxed">
                Join India's premier ocean research platform. Access curated datasets, collaborate with 
                global researchers, and publish FAIR-compliant studies that drive scientific discovery and policy impact.
              </p>
              
              <motion.button
                onClick={() => navigate('/chatbot')}
                className="group relative px-12 py-6 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-bold text-xl rounded-2xl transition-all duration-300 hover:from-indigo-400 hover:to-purple-500 shadow-2xl border border-indigo-400/50"
                whileHover={{ scale: 1.05, y: -3 }}
                whileTap={{ scale: 0.95 }}
              >
                <div className="flex items-center space-x-4">
                  <FaRocket className="text-2xl group-hover:animate-bounce" />
                  <span>Start Research Journey</span>
                  <FaLightbulb className="text-2xl group-hover:animate-pulse" />
                </div>
                
                <div className="absolute inset-0 bg-gradient-to-r from-indigo-400/20 to-purple-500/20 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-300"></div>
              </motion.button>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
};