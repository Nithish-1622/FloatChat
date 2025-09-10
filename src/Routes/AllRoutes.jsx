import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Launch,ChatBot,CoastalLivelihood,Dashboard,MarineNavigation,MarineResearch  } from '../Pages'

export const AllRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Launch/>} />
      <Route path="/dashboard" element={<Dashboard/>} />
      <Route path='/chatbot' element={<ChatBot />} />
      <Route path='/marine-navigation' element={<MarineNavigation />} />
      <Route path='/coastal-livelihood' element={<CoastalLivelihood />} />
      <Route path='/marine-research' element={<MarineResearch />} />
    </Routes>
  )
}
