import React, { useState, useEffect } from 'react';
import axios from '../../utils/axiosConfig';

function DebugConnection() {
  const [status, setStatus] = useState('Verificando conexión...');
  const [details, setDetails] = useState({});

  useEffect(() => {
    const checkConnection = async () => {
      try {
        // Intentamos obtener el CSRF token para probar la conexión
        await axios.get('/api/csrf/');
        setStatus('Conectado al backend correctamente');
        setDetails({
          baseURL: axios.defaults.baseURL,
          timestamp: new Date().toISOString(),
          status: 'success'
        });
      } catch (err) {
        setStatus('Error al conectar con el backend');
        setDetails({
          baseURL: axios.defaults.baseURL,
          timestamp: new Date().toISOString(),
          status: 'error',
          message: err.message,
          responseData: err.response?.data
        });
      }
    };

    checkConnection();
  }, []);

  return (
    <div className="debug-container" style={{ padding: '20px', border: '1px solid #ddd', margin: '20px', borderRadius: '5px' }}>
      <h3>Información de Depuración</h3>
      <p><strong>Estado:</strong> {status}</p>
      <details>
        <summary>Detalles técnicos</summary>
        <pre>{JSON.stringify(details, null, 2)}</pre>
      </details>
    </div>
  );
}

export default DebugConnection;
