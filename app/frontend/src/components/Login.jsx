import React from 'react';
import Base from './Base';

const Login = ({ success, error, form, onSubmit }) => (
  <Base>
    <div className="login-container">
      <h2>Iniciar Sesión</h2>
      {success && <div className="message success">Inicio de sesión exitoso.</div>}
      {error && <div className="message error">{error}</div>}
      <form onSubmit={onSubmit} novalidate>
        {form.non_field_errors && (
          <div className="message error">
            {form.non_field_errors.map((error, idx) => <div key={idx}>{error}</div>)}
          </div>
        )}
        <div className="form-group">
          <label htmlFor="id_username">Usuario:</label>
          {form.username}
          {form.username.errors && (
            <div className="message error">
              {form.username.errors.map((error, idx) => <div key={idx}>{error}</div>)}
            </div>
          )}
        </div>
        <div className="form-group">
          <label htmlFor="id_password">Contraseña:</label>
          {form.password}
          {form.password.errors && (
            <div className="message error">
              {form.password.errors.map((error, idx) => <div key={idx}>{error}</div>)}
            </div>
          )}
        </div>
        <button type="submit" className="login-button">Iniciar sesión</button>
      </form>
    </div>
    <style>{`
      .login-container { max-width: 400px; margin: 2rem auto; padding: 2rem; background-color: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); }
      .form-group { margin-bottom: 1rem; }
      form label { display: block; margin-bottom: 0.5rem; color: #555; }
      form input { width: 100%; padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px; margin-top: 0.25rem; }
      .login-button { background-color: #007bff; color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 4px; cursor: pointer; width: 100%; font-size: 1rem; margin-top: 1rem; }
      .login-button:hover { background-color: #0056b3; }
      .message { padding: 1rem; border-radius: 4px; margin-bottom: 1rem; }
      .success { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
      .error { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    `}</style>
  </Base>
);

export default Login; 