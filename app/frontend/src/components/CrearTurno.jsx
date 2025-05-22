import React from 'react';

const CrearTurno = ({ form, onSubmit }) => (
  <div>
    <h2>Crear Turno</h2>
    <form onSubmit={onSubmit}>
      {form}
      <button type="submit">Guardar turno</button>
    </form>
  </div>
);

export default CrearTurno; 