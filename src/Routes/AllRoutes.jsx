import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Launch } from '../Pages/Launch'
import { Dashboard } from '../Pages/Dashboard'
import { ChatBot } from '../Pages/ChatBot'

export const AllRoutes = () => {
  return (
    <div className="min-h-screen bg-blue-900">
      <Routes>
        <Route path="/" element={<Launch />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/chatbot" element={<ChatBot />} />
      </Routes>
    </div>
  )
}
