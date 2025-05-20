import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';

// Pages
import Login from './components/pages/Login';
import Register from './components/pages/Register';
import Dashboard from './components/pages/Dashboard';
import Turnos from './components/pages/Turnos';
// Importamos el componente de depuración
import DebugConnection from './components/utils/DebugConnection';

function App() {
  return (
    <Router>
      <div className="App">
        {/* Componente de depuración - solo visible en desarrollo */}
        {process.env.NODE_ENV === 'development' && <DebugConnection />}
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/turnos" element={<Turnos />} />
          <Route path="/" element={<Navigate to="/login" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
