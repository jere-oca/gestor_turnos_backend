import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from '../../utils/axiosConfig';
import './Turnos.css';

function CrearTurno({ userRole }) {
  const navigate = useNavigate();
  const [especialidades, setEspecialidades] = useState([]);
  const [medicos, setMedicos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    fecha: '',
    hora: '',
    especialidad_id: '',
    medico_id: '',
    paciente_id: ''
  });

  // Si el usuario es paciente, obtener su paciente_id automáticamente
  useEffect(() => {
    const fetchPacienteId = async () => {
      if (userRole && userRole.toLowerCase() === 'paciente') {
        try {
          const response = await axios.get('/api/pacientes/?propios=1');
          if (Array.isArray(response.data) && response.data.length > 0) {
            setFormData(prev => ({ ...prev, paciente_id: response.data[0].id }));
          }
        } catch (err) {
          // No bloquear el flujo si falla
          console.error('No se pudo obtener paciente_id:', err);
        }
      }
    };
    fetchPacienteId();
  }, [userRole]);

  // Generar próximos 30 días hábiles (lunes a viernes)
  const getDiasHabiles = () => {
    const dias = [];
    let fecha = new Date();
    for (let i = 0; dias.length < 30 && i < 60; i++) { // máximo 60 días para encontrar 30 hábiles
      const day = fecha.getDay();
      if (day !== 0 && day !== 6) {
        dias.push(new Date(fecha));
      }
      fecha.setDate(fecha.getDate() + 1);
    }
    return dias;
  };

  const diasHabiles = getDiasHabiles();

  // Generar horarios válidos (08:00 a 18:00, cada 15 minutos)
  const getHorariosValidos = () => {
    const horarios = [];
    for (let h = 8; h <= 18; h++) {
      for (let m = 0; m < 60; m += 15) {
        if (h === 18 && m > 0) break;
        const hora = h.toString().padStart(2, '0');
        const min = m.toString().padStart(2, '0');
        horarios.push(`${hora}:${min}`);
      }
    }
    return horarios;
  };

  const horariosValidos = getHorariosValidos();

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


  // Nuevo handleChange para selects personalizados
  const handleChange = (e) => {
    const { name, value } = e.target;
    setError('');
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };


  const handleSubmit = async (e) => {
    e.preventDefault();
    // Validación redundante, pero por seguridad
    if (!diasHabiles.some(d => d.toISOString().split('T')[0] === formData.fecha)) {
      setError('Solo se pueden seleccionar fechas de lunes a viernes.');
      return;
    }
    if (!horariosValidos.includes(formData.hora)) {
      setError('Solo se permiten turnos entre 08:00 y 18:00, en intervalos de 15 minutos.');
      return;
    }
    try {
      setLoading(true);
      // Construir el body del turno
      const turnoData = {
        fecha: formData.fecha,
        hora: formData.hora,
        medico_id: formData.medico_id
      };
      // Si hay paciente_id, agregarlo
      if (formData.paciente_id) {
        turnoData.paciente_id = formData.paciente_id;
      }
      await axios.post('/api/turnos/', turnoData);
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
          <select
            id="fecha"
            name="fecha"
            value={formData.fecha}
            onChange={handleChange}
            required
          >
            <option value="">Seleccione un día</option>
            {diasHabiles.map(dia => {
              const iso = dia.toISOString().split('T')[0];
              const label = dia.toLocaleDateString('es-AR', { weekday: 'long', year: 'numeric', month: '2-digit', day: '2-digit' });
              return (
                <option key={iso} value={iso}>{label}</option>
              );
            })}
          </select>
          <small style={{ color: '#888' }}>Solo se permiten días de lunes a viernes.</small>
        </div>

        <div className="form-group">
          <label htmlFor="hora">Hora:</label>
          <select
            id="hora"
            name="hora"
            value={formData.hora}
            onChange={handleChange}
            required
          >
            <option value="">Seleccione un horario</option>
            {horariosValidos.map(hora => (
              <option key={hora} value={hora}>{hora}</option>
            ))}
          </select>
          <small style={{ color: '#888' }}>Solo entre 08:00 y 18:00, cada 15 minutos.</small>
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
