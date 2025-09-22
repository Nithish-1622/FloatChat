import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Launch } from '../Pages/Launch'
import { Dashboard } from '../Pages/Dashboard'
import { ChatBot } from '../Pages/ChatBot'
import  Virtual   from '../components/Virtual.jsx'
import { MarineNavigation } from '../Pages/MarineNavigation'
import { CoastalLivelihood }from '../components/CoastalLivelihood.jsx'
import { MarineResearch } from '../Pages/MarineResearch'
import  News  from '../Pages/News'

export const AllRoutes = () => {
  return (
    <div className="min-h-screen bg-blue-900">
      <Routes>
        <Route path="/" element={<Launch />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/chatbot" element={<ChatBot />} />
        <Route path="/virtual" element={<Virtual />} />
        <Route path='/marine-navigation' element={<MarineNavigation />} />
        <Route path='/coastal-livelihood' element={<CoastalLivelihood />} />
        <Route path='/marine-research' element={<MarineResearch />} />
        <Route path='/news' element={<News />} />

      </Routes>
    </div>
  )
}
