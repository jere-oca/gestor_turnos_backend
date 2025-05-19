import React from 'react';

const Base = ({ children }) => (
  <div>
    <head>
      <meta charSet="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>Sistema de Gestión de Turnos</title>
      <style>{`
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0; background-color: #f8f9fa; }
        .container { width: 100%; max-width: 1200px; margin: 0 auto; padding: 1rem; }
        .navbar { background-color: #343a40; padding: 1rem; color: white; }
        .navbar a { color: white; text-decoration: none; margin-right: 1rem; }
        .navbar a:hover { color: #007bff; }
        .content { padding: 2rem 0; }
      `}</style>
    </head>
    <body>
      <nav className="navbar">
        <div className="container">
          <a href="/login">Iniciar Sesión</a>
          <a href="/register">Registrarse</a>
        </div>
      </nav>
      <div className="container">
        <div className="content">
          {children}
        </div>
      </div>
    </body>
  </div>
);

export default Base; 