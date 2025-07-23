import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from '../../utils/axiosConfig';
import './NavBar.css';

function NavBar({ isLoggedIn, userRole }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await axios.post('/api/logout/');
      // Redirigir a la página de login
      navigate('/login');
    } catch (err) {
      console.error('Error al cerrar sesión:', err);
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/dashboard" className="navbar-logo">
          <span className="logo-text">MedTurno</span>
        </Link>

        <div className="menu-icon" onClick={() => setMenuOpen(!menuOpen)}>
          <i className={menuOpen ? 'fas fa-times' : 'fas fa-bars'} />
        </div>

        <ul className={menuOpen ? 'nav-menu active' : 'nav-menu'}>
          {isLoggedIn && (
            <>
              <li className="nav-item">
                <Link 
                  to="/dashboard" 
                  className="nav-link"
                  onClick={() => setMenuOpen(false)}
                >
                  Dashboard
                </Link>
              </li>
              <li className="nav-item">
                <Link 
                  to="/turnos" 
                  className="nav-link"
                  onClick={() => setMenuOpen(false)}
                >
                  Turnos
                </Link>
              </li>
              {userRole === 'administrativo' && (
                <li className="nav-item">
                  <Link 
                    to="/admin" 
                    className="nav-link"
                    onClick={() => setMenuOpen(false)}
                  >
                    Administración
                  </Link>
                </li>
              )}
              <li className="nav-item">
                <button 
                  className="nav-link btn-logout"
                  onClick={() => {
                    handleLogout();
                    setMenuOpen(false);
                  }}
                >
                  Cerrar Sesión
                </button>
              </li>
            </>
          )}

          {!isLoggedIn && (
            <>
              <li className="nav-item">
                <Link 
                  to="/login" 
                  className="nav-link"
                  onClick={() => setMenuOpen(false)}
                >
                  Iniciar Sesión
                </Link>
              </li>
              <li className="nav-item">
                <Link 
                  to="/register" 
                  className="nav-link btn-register"
                  onClick={() => setMenuOpen(false)}
                >
                  Registrarse
                </Link>
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
}

export default NavBar;
