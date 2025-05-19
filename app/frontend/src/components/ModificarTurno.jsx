import React from 'react';

const ModificarTurno = ({ form, onSubmit }) => (
  <div>
    <h2>Modificar Turno</h2>
    <form onSubmit={onSubmit}>
      {form}
      <button type="submit">Guardar Cambios</button>
    </form>
  </div>
);

export default ModificarTurno; 