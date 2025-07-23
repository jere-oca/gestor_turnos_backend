import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import ListarTurnos from './ListarTurnos';
import CrearTurno from './CrearTurno';
import EditarTurno from './EditarTurno';
import DetalleTurno from './DetalleTurno';
import TurnosNavigation from './TurnosNavigation';
import './Turnos.css';

function TurnosMain({ userRole }) {
  return (
    <div className="turnos-main">
      <TurnosNavigation />
      <div className="turnos-content">
        <Routes>
          <Route path="/" element={<ListarTurnos userRole={userRole} />} />
          <Route path="/crear" element={<CrearTurno userRole={userRole} />} />
          {/* Solo permitir ruta de edición si NO es paciente */}
          {userRole !== 'paciente' && <Route path="/editar/:id" element={<EditarTurno userRole={userRole} />} />}
          <Route path="/detalle/:id" element={<DetalleTurno userRole={userRole} />} />
          <Route path="*" element={<Navigate to="/turnos" replace />} />
        </Routes>
      </div>
    </div>
  );
}

export default TurnosMain;
