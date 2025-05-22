import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from '../../utils/axiosConfig';
import './Turnos.css';

function CrearTurno() {
  const navigate = useNavigate();
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

  // Cargar especialidades al montar el componente
  useEffect(() => {
    const fetchEspecialidades = async () => {
      try {
        const response = await axios.get('/api/especialidades/');
        setEspecialidades(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error al cargar especialidades:', err);
        setError('Error al cargar especialidades: ' + (err.response?.data?.detail || err.message));
        setLoading(false);
      }
    };

    fetchEspecialidades();
  }, []);

  // Cargar médicos cuando se selecciona una especialidad
  useEffect(() => {
    const fetchMedicos = async () => {
      if (!formData.especialidad_id) return;
      
      try {
        setLoading(true);
        const response = await axios.get(`/api/medicos/?especialidad=${formData.especialidad_id}`);
        setMedicos(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error al cargar médicos:', err);
        setError('Error al cargar médicos: ' + (err.response?.data?.detail || err.message));
        setLoading(false);
      }
    };

    fetchMedicos();
  }, [formData.especialidad_id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      await axios.post('/api/turnos/', {
        fecha: formData.fecha,
        hora: formData.hora,
        medico: formData.medico_id
      });
      
      navigate('/turnos');
    } catch (err) {
      console.error('Error al crear turno:', err);
      setError('Error al crear turno: ' + (err.response?.data?.detail || err.message));
      setLoading(false);
    }
  };

  if (loading && especialidades.length === 0) return <div className="loading">Cargando...</div>;

  return (
    <div className="crear-turno-container">
      <h2>Crear Nuevo Turno</h2>
      
      {error && <div className="error">{error}</div>}
      
      <form onSubmit={handleSubmit} className="turno-form">
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
            {loading ? 'Guardando...' : 'Guardar Turno'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default CrearTurno;
