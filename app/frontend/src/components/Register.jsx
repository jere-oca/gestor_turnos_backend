import React from 'react';
import Base from './Base';

const Register = ({ messages, auth_form, persona_form, onSubmit }) => (
  <Base>
    <div className="register-container">
      <h2>Registro de Usuario</h2>
      {messages && messages.length > 0 && (
        <div className="messages">
          {messages.map((message, idx) => (
            <div key={idx} className={`message ${message.tags || ''}`}>{message.text}</div>
          ))}
        </div>
      )}
      <form onSubmit={onSubmit}>
        <div className="form-section">
          <h3>Información de Usuario</h3>
          {auth_form}
        </div>
        <div className="form-section">
          <h3>Información Personal</h3>
          {persona_form}
        </div>
        <button type="submit" className="register-button">Registrar Usuario</button>
      </form>
    </div>
    <style>{`
      .register-container { max-width: 600px; margin: 2rem auto; padding: 2rem; background-color: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); }
      .form-section { margin-bottom: 2rem; }
      .form-section h3 { color: #333; margin-bottom: 1rem; border-bottom: 1px solid #eee; padding-bottom: 0.5rem; }
      form p { margin-bottom: 1rem; }
      form label { display: block; margin-bottom: 0.5rem; color: #555; }
      form input, form select { width: 100%; padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px; margin-top: 0.25rem; }
      .register-button { background-color: #007bff; color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 4px; cursor: pointer; width: 100%; font-size: 1rem; }
      .register-button:hover { background-color: #0056b3; }
      .messages { margin-bottom: 1rem; }
      .message { padding: 1rem; border-radius: 4px; margin-bottom: 0.5rem; }
      .success { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
      .error { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    `}</style>
  </Base>
);

export default Register; 