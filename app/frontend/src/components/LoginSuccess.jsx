import React from 'react';

const LoginSuccess = ({ nombre, apellido, tipo_usuario }) => (
  <div>
    <head>
      <title>Login Exitoso</title>
      <style>{`
        .success-message { text-align: center; margin-top: 50px; padding: 20px; background-color: #e8f5e9; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #2e7d32; margin-bottom: 10px; }
        .user-info { font-size: 1.2em; color: #1b5e20; margin: 10px 0; }
      `}</style>
    </head>
    <body>
      <div className="success-message">
        <h1>¡Inicio de sesión exitoso!</h1>
        <p className="user-info">Bienvenido/a: {nombre} {apellido}</p>
        <p className="user-info">Tipo de usuario: {tipo_usuario}</p>
      </div>
    </body>
  </div>
);

export default LoginSuccess; 