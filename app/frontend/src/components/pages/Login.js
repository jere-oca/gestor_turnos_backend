import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from '../../utils/axiosConfig';

function Login({ setIsLoggedIn, setUserRole }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/login/', {
        username,
        password
      });
      
      if (response.data.success) {
        setIsLoggedIn(true);
        setUserRole(response.data.tipo_usuario || '');
        navigate('/dashboard');
      }
    } catch (err) {
      console.error('Error de login:', err.response ? err.response.data : err.message);
      setError(err.response?.data?.error || 'Usuario o contraseña incorrectos');
    }
  };

  return (
    <div className="login-container">
      <h2>Iniciar Sesión</h2>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Usuario:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Contraseña:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Iniciar Sesión</button>
      </form>
      <p>
        ¿No tienes una cuenta? <a href="/register">Regístrate</a>
      </p>
    </div>
  );
}

export default Login;