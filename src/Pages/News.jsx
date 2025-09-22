import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  FaNewspaper, 
  FaSearch, 
  FaFilter, 
  FaTimes, 
  FaExternalLinkAlt, 
  FaCalendarAlt,
  FaGlobe,
  FaFish,
  FaWater,
  FaLeaf,
  FaShip,
  FaRecycle,
  FaEye,
  FaRedo,
  FaClock,
  FaBookmark,
  FaShare,
  FaChevronDown,
  FaChevronUp
} from 'react-icons/fa';

const OceanNews = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    topic: 'all',
    daysBack: 7,
    maxArticles: 20,
    minRelevanceScore: 5.0,
    sources: '',
    excludeTerms: ''
  });
  const [searchQuery, setSearchQuery] = useState('');
  const [showFilters, setShowFilters] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [bookmarkedArticles, setBookmarkedArticles] = useState([]);
  const [sortBy, setSortBy] = useState('publishedAt');
  const [viewMode, setViewMode] = useState('grid'); // grid or list

  const API_BASE_URL = 'http://localhost:8001';
  
  // Ocean topics with icons and colors
  const oceanTopics = [
    { value: 'all', label: 'All News', icon: FaGlobe, color: 'from-blue-500 to-cyan-500' },
    { value: 'marine_biology', label: 'Marine Biology', icon: FaFish, color: 'from-green-500 to-emerald-500' },
    { value: 'ocean_pollution', label: 'Ocean Pollution', icon: FaRecycle, color: 'from-red-500 to-orange-500' },
    { value: 'coral_reefs', label: 'Coral Reefs', icon: FaLeaf, color: 'from-pink-500 to-rose-500' },
    { value: 'deep_sea', label: 'Deep Sea', icon: FaWater, color: 'from-indigo-500 to-purple-500' },
    { value: 'marine_conservation', label: 'Conservation', icon: FaLeaf, color: 'from-green-600 to-teal-600' },
    { value: 'ocean_technology', label: 'Ocean Tech', icon: FaShip, color: 'from-blue-600 to-indigo-600' }
  ];

  useEffect(() => {
    fetchOceanNews();
  }, [filters, selectedCategory]);

  const fetchOceanNews = async () => {
    setLoading(true);
    setError(null);

    try {
      const queryParams = new URLSearchParams({
        topic: selectedCategory,
        days_back: filters.daysBack,
        max_articles: filters.maxArticles,
        min_relevance_score: filters.minRelevanceScore,
        ...(filters.sources && { sources: filters.sources }),
        ...(filters.excludeTerms && { exclude_terms: filters.excludeTerms })
      });

      const response = await fetch(`${API_BASE_URL}/ocean-news?${queryParams}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.status === 'ok') {
        setArticles(data.articles || []);
      } else {
        throw new Error(data.message || 'Failed to fetch news');
      }
    } catch (err) {
      console.error('Error fetching ocean news:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleBookmark = (articleUrl) => {
    setBookmarkedArticles(prev => 
      prev.includes(articleUrl) 
        ? prev.filter(url => url !== articleUrl)
        : [...prev, articleUrl]
    );
  };

  const handleShare = async (article) => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: article.title,
          text: article.description,
          url: article.url,
        });
      } catch (err) {
        console.log('Error sharing:', err);
      }
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(article.url);
      alert('Article URL copied to clipboard!');
    }
  };

  const filteredArticles = articles
    .filter(article => 
      searchQuery === '' || 
      article.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      article.description.toLowerCase().includes(searchQuery.toLowerCase())
    )
    .sort((a, b) => {
      switch (sortBy) {
        case 'relevance':
          return (b.ocean_relevance_score || 0) - (a.ocean_relevance_score || 0);
        case 'publishedAt':
          return new Date(b.publishedAt) - new Date(a.publishedAt);
        default:
          return 0;
      }
    });

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getRelevanceColor = (score) => {
    if (score >= 80) return 'text-green-500';
    if (score >= 60) return 'text-yellow-500';
    if (score >= 40) return 'text-orange-500';
    return 'text-red-500';
  };

  const getRelevanceBadge = (score) => {
    if (score >= 80) return 'bg-green-100 text-green-800';
    if (score >= 60) return 'bg-yellow-100 text-yellow-800';
    if (score >= 40) return 'bg-orange-100 text-orange-800';
    return 'bg-red-100 text-red-800';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Header */}
      <div className="bg-slate-900/80 backdrop-blur-xl border-b border-slate-700/50">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-xl">
                <FaNewspaper className="text-2xl text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-white">Ocean News</h1>
                <p className="text-slate-400">Latest updates from the marine world</p>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <div className="flex items-center space-x-2">
                <span className="text-sm text-slate-400">Sort by:</span>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="bg-slate-800 text-white rounded-lg px-3 py-2 text-sm border border-slate-600 focus:border-cyan-400 focus:outline-none"
                >
                  <option value="publishedAt">Latest</option>
                  <option value="relevance">Relevance</option>
                </select>
              </div>

              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`p-2 rounded-lg transition-colors ${
                    viewMode === 'grid' 
                      ? 'bg-cyan-500 text-white' 
                      : 'bg-slate-800 text-slate-400 hover:text-white'
                  }`}
                >
                  <div className="w-4 h-4 grid grid-cols-2 gap-0.5">
                    <div className="bg-current rounded-sm"></div>
                    <div className="bg-current rounded-sm"></div>
                    <div className="bg-current rounded-sm"></div>
                    <div className="bg-current rounded-sm"></div>
                  </div>
                </button>
                
                <button
                  onClick={() => setViewMode('list')}
                  className={`p-2 rounded-lg transition-colors ${
                    viewMode === 'list' 
                      ? 'bg-cyan-500 text-white' 
                      : 'bg-slate-800 text-slate-400 hover:text-white'
                  }`}
                >
                  <div className="w-4 h-4 flex flex-col gap-1">
                    <div className="h-0.5 bg-current rounded"></div>
                    <div className="h-0.5 bg-current rounded"></div>
                    <div className="h-0.5 bg-current rounded"></div>
                  </div>
                </button>
              </div>
            </div>
          </div>

          {/* Search and Filters */}
          <div className="mt-6 space-y-4">
            <div className="flex flex-col lg:flex-row gap-4">
              {/* Search Bar */}
              <div className="flex-1 relative">
                <FaSearch className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search ocean news..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-12 pr-4 py-3 bg-slate-800/50 border border-slate-600 rounded-xl text-white placeholder-slate-400 focus:border-cyan-400 focus:outline-none transition-colors"
                />
              </div>

              {/* Filter Toggle */}
              <button
                onClick={() => setShowFilters(!showFilters)}
                className="flex items-center space-x-2 px-6 py-3 bg-slate-800/50 border border-slate-600 rounded-xl text-white hover:border-cyan-400 transition-colors"
              >
                <FaFilter />
                <span>Filters</span>
                {showFilters ? <FaChevronUp /> : <FaChevronDown />}
              </button>

              {/* Refresh Button */}
              <button
                onClick={fetchOceanNews}
                disabled={loading}
                className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-xl text-white hover:from-cyan-400 hover:to-blue-400 disabled:opacity-50 transition-colors"
              >
                <FaRedo className={loading ? 'animate-spin' : ''} />
                <span>{loading ? 'Loading...' : 'Refresh'}</span>
              </button>
            </div>

            {/* Category Tabs */}
            <div className="flex flex-wrap gap-2">
              {oceanTopics.map((topic) => {
                const IconComponent = topic.icon;
                return (
                  <button
                    key={topic.value}
                    onClick={() => setSelectedCategory(topic.value)}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all ${
                      selectedCategory === topic.value
                        ? `bg-gradient-to-r ${topic.color} text-white shadow-lg`
                        : 'bg-slate-800/50 text-slate-300 hover:bg-slate-700/50'
                    }`}
                  >
                    <IconComponent className="text-sm" />
                    <span className="text-sm font-medium">{topic.label}</span>
                  </button>
                );
              })}
            </div>

            {/* Advanced Filters */}
            <AnimatePresence>
              {showFilters && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="overflow-hidden"
                >
                  <div className="bg-slate-800/50 border border-slate-600 rounded-xl p-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">
                          Days Back
                        </label>
                        <select
                          value={filters.daysBack}
                          onChange={(e) => setFilters(prev => ({ ...prev, daysBack: Number(e.target.value) }))}
                          className="w-full bg-slate-700 text-white rounded-lg px-3 py-2 border border-slate-600 focus:border-cyan-400 focus:outline-none"
                        >
                          <option value={1}>1 Day</option>
                          <option value={3}>3 Days</option>
                          <option value={7}>1 Week</option>
                          <option value={14}>2 Weeks</option>
                          <option value={30}>1 Month</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">
                          Max Articles
                        </label>
                        <select
                          value={filters.maxArticles}
                          onChange={(e) => setFilters(prev => ({ ...prev, maxArticles: Number(e.target.value) }))}
                          className="w-full bg-slate-700 text-white rounded-lg px-3 py-2 border border-slate-600 focus:border-cyan-400 focus:outline-none"
                        >
                          <option value={10}>10</option>
                          <option value={20}>20</option>
                          <option value={50}>50</option>
                          <option value={100}>100</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">
                          Min Relevance Score
                        </label>
                        <select
                          value={filters.minRelevanceScore}
                          onChange={(e) => setFilters(prev => ({ ...prev, minRelevanceScore: Number(e.target.value) }))}
                          className="w-full bg-slate-700 text-white rounded-lg px-3 py-2 border border-slate-600 focus:border-cyan-400 focus:outline-none"
                        >
                          <option value={0}>Any Score</option>
                          <option value={5}>5+</option>
                          <option value={10}>10+</option>
                          <option value={15}>15+</option>
                          <option value={20}>20+</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">
                          Sources (comma-separated)
                        </label>
                        <input
                          type="text"
                          placeholder="bbc.co.uk, cnn.com"
                          value={filters.sources}
                          onChange={(e) => setFilters(prev => ({ ...prev, sources: e.target.value }))}
                          className="w-full bg-slate-700 text-white rounded-lg px-3 py-2 border border-slate-600 focus:border-cyan-400 focus:outline-none"
                        />
                      </div>
                    </div>

                    <div className="mt-4">
                      <label className="block text-sm font-medium text-slate-300 mb-2">
                        Exclude Terms (comma-separated)
                      </label>
                      <input
                        type="text"
                        placeholder="tourism, hotel, restaurant"
                        value={filters.excludeTerms}
                        onChange={(e) => setFilters(prev => ({ ...prev, excludeTerms: e.target.value }))}
                        className="w-full bg-slate-700 text-white rounded-lg px-3 py-2 border border-slate-600 focus:border-cyan-400 focus:outline-none"
                      />
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Loading State */}
        {loading && (
          <div className="flex flex-col items-center justify-center py-20">
            <div className="relative">
              <div className="w-16 h-16 border-4 border-slate-600 border-t-cyan-500 rounded-full animate-spin"></div>
              <FaWater className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-cyan-500" />
            </div>
            <p className="mt-4 text-slate-400">Fetching latest ocean news...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-900/50 border border-red-500/50 rounded-xl p-6 mb-8">
            <div className="flex items-center space-x-3">
              <FaTimes className="text-red-400" />
              <div>
                <h3 className="text-red-400 font-semibold">Error Loading News</h3>
                <p className="text-red-300">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Articles */}
        {!loading && !error && (
          <>
            {/* Results Info */}
            <div className="flex items-center justify-between mb-6">
              <p className="text-slate-400">
                {filteredArticles.length} articles found
                {searchQuery && ` for "${searchQuery}"`}
              </p>
              
              <div className="flex items-center space-x-2 text-sm text-slate-400">
                <FaClock />
                <span>Last updated: {new Date().toLocaleTimeString()}</span>
              </div>
            </div>

            {/* Articles Grid/List */}
            <div className={
              viewMode === 'grid' 
                ? "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
                : "space-y-6"
            }>
              <AnimatePresence>
                {filteredArticles.map((article, index) => (
                  <motion.article
                    key={article.url}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className={`bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl overflow-hidden hover:border-cyan-400/50 transition-all duration-300 ${
                      viewMode === 'list' ? 'flex' : ''
                    }`}
                  >
                    {/* Article Image */}
                    {article.urlToImage && (
                      <div className={`relative ${viewMode === 'list' ? 'w-48 flex-shrink-0' : 'h-48'}`}>
                        <img
                          src={article.urlToImage}
                          alt={article.title}
                          className="w-full h-full object-cover"
                          onError={(e) => {
                            e.target.style.display = 'none';
                          }}
                        />
                        
                        {/* Relevance Score Badge */}
                        {article.ocean_relevance_score && (
                          <div className={`absolute top-3 right-3 px-2 py-1 rounded-full text-xs font-bold ${getRelevanceBadge(article.ocean_relevance_score)}`}>
                            {Math.round(article.ocean_relevance_score)}%
                          </div>
                        )}
                      </div>
                    )}

                    {/* Article Content */}
                    <div className="p-6 flex-1">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center space-x-2 text-sm text-slate-400">
                          <span>{article.source?.name}</span>
                          <span>•</span>
                          <span>{formatDate(article.publishedAt)}</span>
                        </div>
                        
                        <div className="flex items-center space-x-2">
                          <button
                            onClick={() => handleBookmark(article.url)}
                            className={`p-1 rounded transition-colors ${
                              bookmarkedArticles.includes(article.url)
                                ? 'text-yellow-400'
                                : 'text-slate-400 hover:text-yellow-400'
                            }`}
                          >
                            <FaBookmark />
                          </button>
                          
                          <button
                            onClick={() => handleShare(article)}
                            className="p-1 text-slate-400 hover:text-cyan-400 transition-colors"
                          >
                            <FaShare />
                          </button>
                        </div>
                      </div>

                      <h3 className="text-xl font-bold text-white mb-3 line-clamp-2 leading-tight">
                        {article.title}
                      </h3>
                      
                      <p className="text-slate-300 text-sm mb-4 line-clamp-3">
                        {article.description}
                      </p>

                      {/* Ocean Topics */}
                      {article.ocean_topics && article.ocean_topics.length > 0 && (
                        <div className="flex flex-wrap gap-2 mb-4">
                          {article.ocean_topics.slice(0, 3).map((topic, idx) => (
                            <span
                              key={idx}
                              className="px-2 py-1 bg-cyan-500/20 text-cyan-300 text-xs rounded-full"
                            >
                              {topic}
                            </span>
                          ))}
                        </div>
                      )}

                      <div className="flex items-center justify-between">
                        <a
                          href={article.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-lg hover:from-cyan-400 hover:to-blue-400 transition-colors text-sm"
                        >
                          <span>Read More</span>
                          <FaExternalLinkAlt />
                        </a>

                        {article.ocean_relevance_score && (
                          <div className="flex items-center space-x-2">
                            <FaEye className="text-slate-400" />
                            <span className={`text-sm font-semibold ${getRelevanceColor(article.ocean_relevance_score)}`}>
                              {Math.round(article.ocean_relevance_score)}%
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
                  </motion.article>
                ))}
              </AnimatePresence>
            </div>

            {/* No Results */}
            {filteredArticles.length === 0 && !loading && (
              <div className="text-center py-20">
                <FaNewspaper className="text-6xl text-slate-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-slate-400 mb-2">No Articles Found</h3>
                <p className="text-slate-500">
                  {searchQuery 
                    ? `No articles match your search for "${searchQuery}"`
                    : 'No articles available for the selected filters'
                  }
                </p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default OceanNews;