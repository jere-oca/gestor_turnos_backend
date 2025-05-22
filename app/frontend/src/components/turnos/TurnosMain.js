import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import ListarTurnos from './ListarTurnos';
import CrearTurno from './CrearTurno';
import EditarTurno from './EditarTurno';
import DetalleTurno from './DetalleTurno';
import TurnosNavigation from './TurnosNavigation';
import './Turnos.css';

function TurnosMain() {
  return (
    <div className="turnos-main">
      <TurnosNavigation />
      <div className="turnos-content">
        <Routes>
          <Route path="/" element={<ListarTurnos />} />
          <Route path="/crear" element={<CrearTurno />} />
          <Route path="/editar/:id" element={<EditarTurno />} />
          <Route path="/detalle/:id" element={<DetalleTurno />} />
          <Route path="*" element={<Navigate to="/turnos" replace />} />
        </Routes>
      </div>
    </div>
  );
}

export default TurnosMain;
