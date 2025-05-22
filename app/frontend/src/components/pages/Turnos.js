import React, { useState, useEffect } from 'react';
import axios from '../../utils/axiosConfig';

function Turnos() {
  const [turnos, setTurnos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTurnos();
  }, []);

  const fetchTurnos = async () => {
    try {
      const response = await axios.get('/turnos/list/');
      setTurnos(response.data);
      setLoading(false);
    } catch (err) {
      setError('Error al cargar los turnos');
      setLoading(false);
    }
  };

  const handleEdit = async (id) => {
    // TODO: Implement edit functionality
    console.log('Edit turno:', id);
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`/turnos/${id}/`);
      fetchTurnos(); // Refresh the list after deletion
    } catch (err) {
      setError('Error al eliminar el turno');
    }
  };

  const handleAdd = () => {
    // TODO: Implement add functionality
    console.log('Add new turno');
  };

  if (loading) return <div>Cargando turnos...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="turnos-container">
      <h2>Gestión de Turnos</h2>
      
      <div className="turnos-list">
        {turnos.length === 0 ? (
          <p>No hay turnos disponibles</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Hora</th>
                <th>Paciente</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {turnos.map((turno) => (
                <tr key={turno.id}>
                  <td>{turno.fecha}</td>
                  <td>{turno.hora}</td>
                  <td>{turno.paciente}</td>
                  <td>{turno.estado}</td>
                  <td>
                    <button onClick={() => handleEdit(turno.id)}>Editar</button>
                    <button onClick={() => handleDelete(turno.id)}>Eliminar</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <button className="add-turno-button" onClick={handleAdd}>
        Agregar Nuevo Turno
      </button>
    </div>
  );
}

export default Turnos; 