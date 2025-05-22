import React from 'react';

const BaseDashboard = ({ children, nombre, apellido, tipo_usuario, sidebarMenu, pageTitle, extraCss, extraJs, messages }) => (
  <div>
    <head>
      <title>Dashboard</title>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" />
      <style>{`
        .sidebar { height: 100vh; background-color: #343a40; padding-top: 20px; position: fixed; left: 0; width: 250px; }
        .sidebar a { color: white; padding: 16px; text-decoration: none; display: block; }
        .sidebar a:hover { background-color: #495057; }
        .main-content { margin-left: 250px; padding: 20px; }
        .user-info { color: white; padding: 16px; border-bottom: 1px solid #495057; margin-bottom: 20px; }
        .navbar { margin-left: 250px; padding: 15px 20px; }
      `}</style>
      {extraCss}
    </head>
    <body>
      {/* Sidebar */}
      <div className="sidebar">
        <div className="user-info">
          <h5>{nombre} {apellido}</h5>
          <p>{tipo_usuario}</p>
        </div>
        {sidebarMenu}
        <a href="/logout">Cerrar Sesión</a>
      </div>
      {/* Navbar */}
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container-fluid">
          <h4>{pageTitle || 'Dashboard'}</h4>
        </div>
      </nav>
      {/* Main Content */}
      <div className="main-content">
        {messages && messages.length > 0 && (
          <div className="messages">
            {messages.map((message, idx) => (
              <div key={idx} className={`alert alert-${message.tags}`}>{message.text}</div>
            ))}
          </div>
        )}
        {children}
      </div>
      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
      {extraJs}
    </body>
  </div>
);

export default BaseDashboard; 