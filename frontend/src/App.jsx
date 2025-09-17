import React, { useState } from 'react'
import './App.css'

export default function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="app">
      <h1>Простой React‑проект</h1>
      <p>Счётчик: {count}</p>
      <div className="row">
        <button onClick={() => setCount((c) => c + 1)}>+1</button>
        <button onClick={() => setCount(0)}>Сброс</button>
      </div>
      <p className="hint">Измени src/App.jsx и сохрани — HMR обновит страницу.</p>
    </div>
  )
}

