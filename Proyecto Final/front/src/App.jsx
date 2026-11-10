import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <main style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>cafetales - Univalle</h1>
      <p>Bienvenido a la tienda cafetal.</p>
      
      <div style={{ marginTop: '1.5rem' }}>
        <button onClick={() => setCount((count) => count + 1)}>
          Contador: {count}
        </button>
      </div>
    </main>
  )
}

export default App
