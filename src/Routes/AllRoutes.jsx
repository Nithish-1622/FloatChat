import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Launch } from '../Pages/Launch.jsx'
import { Dashboard } from '../Pages/Dashboard.jsx'
import { ChatBot } from '../Pages/ChatBot.jsx'

export const AllRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Launch/>} />
      <Route path="/dashboard" element={<Dashboard/>} />
      <Route path='/chatbot' element={<ChatBot />} />
    </Routes>
  )
}
