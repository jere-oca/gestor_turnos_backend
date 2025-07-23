import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from '../../utils/axiosConfig';
import './Turnos.css';

function EditarTurno({ userRole }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [turno, setTurno] = useState(null);
  const [especialidades, setEspecialidades] = useState([]);
  const [medicos, setMedicos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    fecha: '',
    hora: '',
    especialidad_id: '',
    medico_id: ''
  });

  // Cargar datos del turno y especialidades
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Cargar el turno a editar
        const turnoResponse = await axios.get(`/api/turnos/${id}/`);
        setTurno(turnoResponse.data);
        
        // Preparar datos del formulario
        setFormData({
          fecha: turnoResponse.data.fecha,
          hora: turnoResponse.data.hora,
          especialidad_id: turnoResponse.data.medico?.especialidad?.id || '',
          medico_id: turnoResponse.data.medico?.id || ''
        });
        
        // Cargar especialidades
        const especialidadesResponse = await axios.get('/api/especialidades/');
        setEspecialidades(especialidadesResponse.data);
        
        // Si hay una especialidad seleccionada, cargar médicos
        if (turnoResponse.data.medico?.especialidad?.id) {
          const medicosResponse = await axios.get(`/api/medicos/?especialidad=${turnoResponse.data.medico.especialidad.id}`);
          setMedicos(medicosResponse.data);
        }
        
        setLoading(false);
      } catch (err) {
        console.error('Error al cargar datos:', err);
        setError('Error al cargar datos: ' + (err.response?.data?.detail || err.message));
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  // Cargar médicos cuando se selecciona una especialidad
  useEffect(() => {
    const fetchMedicos = async () => {
      if (!formData.especialidad_id) return;
      
      try {
        const response = await axios.get(`/api/medicos/?especialidad=${formData.especialidad_id}`);
        setMedicos(response.data);
      } catch (err) {
        console.error('Error al cargar médicos:', err);
        setError('Error al cargar médicos: ' + (err.response?.data?.detail || err.message));
      }
    };

    if (formData.especialidad_id) {
      fetchMedicos();
    }
  }, [formData.especialidad_id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    // Si cambia la especialidad, resetear el médico seleccionado
    if (name === 'especialidad_id') {
      setFormData(prevState => ({
        ...prevState,
        [name]: value,
        medico_id: '' // Resetear médico
      }));
    } else {
      setFormData(prevState => ({
        ...prevState,
        [name]: value
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      await axios.put(`/api/turnos/${id}/`, {
        fecha: formData.fecha,
        hora: formData.hora,
        medico: formData.medico_id
      });
      
      navigate('/turnos');
    } catch (err) {
      console.error('Error al actualizar turno:', err);
      setError('Error al actualizar turno: ' + (err.response?.data?.detail || err.message));
      setLoading(false);
    }
  };

  if (userRole === 'paciente') {
    return <div className="error">No tienes permiso para editar turnos.</div>;
  }
  if (loading && !turno) return <div className="loading">Cargando datos del turno...</div>;
  if (error) return <div className="error">{error}</div>;
  return (
    <div className="editar-turno-container">
      <h2>Editar Turno</h2>
      {error && <div className="error">{error}</div>}
      <form onSubmit={handleSubmit} className="turno-form">
        {/* ...existing code... */}
        <div className="form-group">
          <label htmlFor="especialidad_id">Especialidad:</label>
          <select 
            id="especialidad_id"
            name="especialidad_id"
            value={formData.especialidad_id}
            onChange={handleChange}
            required
          >
            <option value="">Seleccione una especialidad</option>
            {especialidades.map(especialidad => (
              <option key={especialidad.id} value={especialidad.id}>
                {especialidad.nombre}
              </option>
            ))}
          </select>
        </div>
        {formData.especialidad_id && (
          <div className="form-group">
            <label htmlFor="medico_id">Médico:</label>
            <select 
              id="medico_id"
              name="medico_id"
              value={formData.medico_id}
              onChange={handleChange}
              required
            >
              <option value="">Seleccione un médico</option>
              {medicos.map(medico => (
                <option key={medico.id} value={medico.id}>
                  {medico.nombre} {medico.apellido}
                </option>
              ))}
            </select>
          </div>
        )}
        <div className="form-group">
          <label htmlFor="fecha">Fecha:</label>
          <input 
            type="date"
            id="fecha"
            name="fecha"
            value={formData.fecha}
            onChange={handleChange}
            min={new Date().toISOString().split('T')[0]} // No permitir fechas pasadas
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="hora">Hora:</label>
          <input 
            type="time"
            id="hora"
            name="hora"
            value={formData.hora}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-buttons">
          <button type="button" onClick={() => navigate('/turnos')} className="btn-cancelar">
            Cancelar
          </button>
          <button type="submit" className="btn-guardar" disabled={loading}>
            {loading ? 'Guardando...' : 'Guardar Cambios'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default EditarTurno;
