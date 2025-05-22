import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './TurnosNavigation.css';

function TurnosNavigation() {
  const location = useLocation();
  const currentPath = location.pathname;

  return (
    <nav className="turnos-navigation">
      <ul>
        <li className={currentPath === '/turnos' ? 'active' : ''}>
          <Link to="/turnos">
            <i className="fas fa-calendar-alt"></i>
            Mis Turnos
          </Link>
        </li>
        <li className={currentPath === '/turnos/crear' ? 'active' : ''}>
          <Link to="/turnos/crear">
            <i className="fas fa-plus-circle"></i>
            Crear Turno
          </Link>
        </li>
      </ul>
    </nav>
  );
}

export default TurnosNavigation;
