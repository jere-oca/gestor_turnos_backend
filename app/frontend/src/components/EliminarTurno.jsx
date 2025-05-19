import React from 'react';

const EliminarTurno = ({ turno, onSubmit }) => (
  <div>
    <h2>Eliminar Turno</h2>
    <p>¿Estás seguro de que deseas eliminar el turno para {turno.usuario} el {turno.fecha} a las {turno.hora}?</p>
    <form onSubmit={onSubmit}>
      <button type="submit">Eliminar</button>
    </form>
  </div>
);

export default EliminarTurno; 