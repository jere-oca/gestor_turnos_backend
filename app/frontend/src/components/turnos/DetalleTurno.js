import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from '../../utils/axiosConfig';
import './Turnos.css';

function DetalleTurno({ userRole }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [turno, setTurno] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchTurno = async () => {
      try {
        const response = await axios.get(`/api/turnos/${id}/`);
        setTurno(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error al cargar detalle del turno:', err);
        setError('Error al cargar detalle del turno: ' + (err.response?.data?.detail || err.message));
        setLoading(false);
      }
    };

    fetchTurno();
  }, [id]);

  const handleCancelar = async () => {
    try {
      await axios.post(`/api/turnos/${id}/cancelar/`);
      // Actualizar el estado local
      setTurno(prevTurno => ({
        ...prevTurno,
        estado: 'cancelado'
      }));
    } catch (err) {
      console.error('Error al cancelar turno:', err);
      setError('Error al cancelar turno: ' + (err.response?.data?.detail || err.message));
    }
  };

  if (loading) return <div className="loading">Cargando detalles del turno...</div>;

  if (error) return <div className="error">{error}</div>;

  if (!turno) return <div className="error">No se encontró el turno</div>;

  return (
    <div className="detalle-turno-container">
      <h2>Detalle del Turno</h2>
      
      <div className="turno-card">
        <div className="turno-header">
          <span className={`badge-${turno.estado}`}>
            {turno.estado === 'pendiente' ? 'Pendiente' : 
             turno.estado === 'confirmado' ? 'Confirmado' : 
             turno.estado === 'cancelado' ? 'Cancelado' : 
             turno.estado}
          </span>
        </div>
        
        <div className="turno-body">
          <div className="turno-detail">
            <span className="label">Fecha:</span>
            <span className="value">{new Date(turno.fecha).toLocaleDateString()}</span>
          </div>
          
          <div className="turno-detail">
            <span className="label">Hora:</span>
            <span className="value">{turno.hora}</span>
          </div>
          
          <div className="turno-detail">
            <span className="label">Médico:</span>
            <span className="value">
              {turno.medico ? `${turno.medico.nombre} ${turno.medico.apellido}` : 'No asignado'}
            </span>
          </div>
          
          <div className="turno-detail">
            <span className="label">Especialidad:</span>
            <span className="value">
              {turno.medico?.especialidad?.nombre || 'No especificada'}
            </span>
          </div>
          
          {turno.paciente && (
            <div className="turno-detail">
              <span className="label">Paciente:</span>
              <span className="value">{turno.paciente.nombre} {turno.paciente.apellido}</span>
            </div>
          )}
        </div>
        
        <div className="turno-footer">
          <button 
            onClick={() => navigate('/turnos')} 
            className="btn-volver"
          >
            Volver a la lista
          </button>
          
          {turno.estado !== 'cancelado' && (
            <>
              {userRole !== 'paciente' && (
                <button 
                  onClick={() => navigate(`/turnos/editar/${id}`)} 
                  className="btn-editar"
                >
                  Editar Turno
                </button>
              )}
              <button 
                onClick={handleCancelar} 
                className="btn-cancelar"
              >
                Cancelar Turno
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default DetalleTurno;
