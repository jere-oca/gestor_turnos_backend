import React from 'react';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Add logout logic here
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Panel de Control</h1>
        <button onClick={handleLogout} className="logout-button">
          Cerrar Sesión
        </button>
      </header>
      
      <nav className="dashboard-nav">
        <button onClick={() => navigate('/turnos')} className="nav-button">
          Gestionar Turnos
        </button>
        {/* Add more navigation buttons as needed */}
      </nav>

      <main className="dashboard-content">
        <h2>Bienvenido al Sistema</h2>
        <p>Seleccione una opción del menú para comenzar.</p>
      </main>
    </div>
  );
}

export default Dashboard; 