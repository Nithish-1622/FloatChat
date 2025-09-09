import { useState } from 'react'
import './App.css'
import { AllRoutes } from './Routes/AllRoutes.jsx'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>

        
        <AllRoutes />
      </div>
    </>
  )
}

export default App
