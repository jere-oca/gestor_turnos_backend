import React, { useState, useEffect } from 'react';
import axios from '../../utils/axiosConfig';
import { Link, useNavigate } from 'react-router-dom';
import './Turnos.css';

function ListarTurnos({ userRole }) {
  const navigate = useNavigate();
  const [turnos, setTurnos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTurnos();
    // eslint-disable-next-line
  }, []);

  const fetchTurnos = async () => {
    try {
      setLoading(true);
      // Ya no necesitamos parámetros especiales, el backend filtra automáticamente
      const response = await axios.get('/api/turnos/');
      console.log('Respuesta de API:', response.data);
      setTurnos(Array.isArray(response.data) ? response.data : []);
      setLoading(false);
    } catch (err) {
      console.error('Error al cargar los turnos:', err);
      setError('Error al cargar los turnos: ' + (err.response?.data?.detail || err.message));
      setLoading(false);
    }
  };

  const handleCancelar = async (id) => {
    try {
      await axios.post(`/api/turnos/${id}/cancelar/`);
      fetchTurnos(); // Actualizar la lista después de cancelar
    } catch (err) {
      setError('Error al cancelar el turno: ' + (err.response?.data?.detail || err.message));
    }
  };
  if (loading) return (
    <div className="turnos-container">
      <h2>Mis Turnos</h2>
      <div className="loading-container">
        <div className="loading">Cargando turnos...</div>
        <div className="loader"></div>
      </div>
    </div>
  );

  return (
    <div className="turnos-container">
      <h2>Mis Turnos</h2>
      <Link to="/turnos/crear" className="btn-crear">Crear Nuevo Turno</Link>
      
      {error && <div className="error">{error}</div>}
      
      {turnos.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📅</div>
          <p className="no-turnos">No tienes turnos programados.</p>
          <p className="empty-message">Puedes crear un nuevo turno con el botón "Crear Nuevo Turno"</p>
        </div>
      ) : (
        <table className="turnos-table">
          <thead>
            <tr>
              <th>Fecha</th>
              <th>Hora</th>
              <th>Médico</th>
              <th>Especialidad</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {turnos.map(turno => (              <tr 
                key={turno.id} 
                className={`estado-${turno.estado}`}
                onClick={() => navigate(`/turnos/detalle/${turno.id}`)}
                style={{ cursor: 'pointer' }}
              >
                <td>{new Date(turno.fecha).toLocaleDateString()}</td>
                <td>{turno.hora}</td>
                <td>{turno.medico?.nombre ? `${turno.medico.nombre} ${turno.medico.apellido}` : 'No asignado'}</td>
                <td>{turno.medico?.especialidad?.nombre || 'No asignado'}</td>
                <td>
                  <span className={`badge-${turno.estado}`}>
                    {turno.estado === 'pendiente' ? 'Pendiente' : 
                     turno.estado === 'confirmado' ? 'Confirmado' : 
                     turno.estado === 'cancelado' ? 'Cancelado' : 
                     turno.estado}
                  </span>
                </td>
                <td className="acciones" onClick={(e) => e.stopPropagation()}>
                  {turno.estado !== 'cancelado' && (
                    <>
                      {userRole !== 'paciente' && (
                        <Link to={`/turnos/editar/${turno.id}`} className="btn-editar">
                          Editar
                        </Link>
                      )}
                      <button 
                        onClick={() => handleCancelar(turno.id)} 
                        className="btn-cancelar"
                      >
                        Cancelar
                      </button>
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default ListarTurnos;
