import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import axios from './utils/axiosConfig';
import './App.css';

// Pages
import Login from './components/pages/Login';
import Register from './components/pages/Register';
import Dashboard from './components/pages/Dashboard';
// Importamos los componentes de turnos
import TurnosMain from './components/turnos/TurnosMain';
// Componentes de UI
import NavBar from './components/ui/NavBar';
// Importamos el componente de depuración
import DebugConnection from './components/utils/DebugConnection';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userRole, setUserRole] = useState('');
  const [loading, setLoading] = useState(true);

  // Verificar el estado de autenticación al cargar la aplicación
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const response = await axios.get('/api/user/');
        if (response.data.isAuthenticated) {
          setIsLoggedIn(true);
          setUserRole(response.data.role || '');
        } else {
          setIsLoggedIn(false);
          setUserRole('');
        }
      } catch (err) {
        console.error('Error al verificar autenticación:', err);
        setIsLoggedIn(false);
        setUserRole('');
      } finally {
        setLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  if (loading) {
    return <div className="loading-app">Cargando...</div>;
  }

  return (
    <Router>
      <div className="App">
        {/* Componente de depuración - solo visible en desarrollo */}
        {process.env.NODE_ENV === 'development' && <DebugConnection />}
        
        <NavBar isLoggedIn={isLoggedIn} userRole={userRole} />
        
        <main className="app-content">
          <Routes>
            <Route 
              path="/login" 
              element={
                isLoggedIn 
                  ? <Navigate to="/dashboard" replace /> 
                  : <Login setIsLoggedIn={setIsLoggedIn} setUserRole={setUserRole} />
              } 
            />
            <Route path="/register" element={isLoggedIn ? <Navigate to="/dashboard" replace /> : <Register />} />
            <Route path="/dashboard" element={isLoggedIn ? <Dashboard /> : <Navigate to="/login" replace />} />
            <Route path="/turnos/*" element={isLoggedIn ? <TurnosMain /> : <Navigate to="/login" replace />} />
            <Route path="/" element={<Navigate to={isLoggedIn ? "/dashboard" : "/login"} replace />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
