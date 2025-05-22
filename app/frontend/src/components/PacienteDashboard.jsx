import React from 'react';
import BaseDashboard from './BaseDashboard';

const PacienteDashboard = ({ nombre, apellido, tipo_usuario, turnos, messages }) => {
  const sidebarMenu = (
    <>
      <a href="#mis-turnos">Mis Turnos</a>
      <a href="#nuevo-turno">Solicitar Turno</a>
      <a href="#historial">Mi Historial</a>
      <a href="#perfil">Mi Perfil</a>
    </>
  );
  return (
    <BaseDashboard nombre={nombre} apellido={apellido} tipo_usuario={tipo_usuario} sidebarMenu={sidebarMenu} pageTitle="Dashboard Paciente" messages={messages}>
      <div className="container-fluid">
        <div className="row">
          {/* Próximo Turno */}
          <div className="col-md-6 mb-4">
            <div className="card">
              <div className="card-header">
                <h5 className="card-title mb-0">Próximo Turno</h5>
              </div>
              <div className="card-body">
                <div className="text-center">
                  <p className="text-muted">No tienes turnos programados</p>
                  <a href="#nuevo-turno" className="btn btn-primary">Solicitar Turno</a>
                </div>
              </div>
            </div>
          </div>
          {/* Información Personal */}
          <div className="col-md-6 mb-4">
            <div className="card">
              <div className="card-header">
                <h5 className="card-title mb-0">Información Personal</h5>
              </div>
              <div className="card-body">
                <div className="row">
                  <div className="col-12">
                    <p><strong>Nombre:</strong> {nombre} {apellido}</p>
                    <p><strong>Tipo de Usuario:</strong> {tipo_usuario}</p>
                    {/* Agregar más información personal aquí */}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        {/* Historial de Turnos */}
        <div className="row">
          <div className="col-12">
            <div className="card">
              <div className="card-header">
                <h5 className="card-title mb-0">Historial de Turnos</h5>
              </div>
              <div className="card-body">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Fecha</th>
                      <th>Doctor</th>
                      <th>Especialidad</th>
                      <th>Estado</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td colSpan="5" className="text-center">No hay turnos en el historial</td>
                    </tr>
                    {/* {turnos.map(turno => (
                      <tr key={turno.id}>
                        <td>{turno.fecha}</td>
                        <td>{turno.doctor}</td>
                        <td>{turno.especialidad}</td>
                        <td>{turno.estado}</td>
                        <td>
                          <a href={`/eliminar-turno/${turno.id}`} className="btn btn-danger btn-sm">Eliminar</a>
                          <a href={`/modificar-turno/${turno.id}`} className="btn btn-warning btn-sm">Modificar</a>
                        </td>
                      </tr>
                    ))} */}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
        {/* Doctores Disponibles */}
        <div className="row mt-4">
          <div className="col-12">
            <div className="card">
              <div className="card-header">
                <h5 className="card-title mb-0">Doctores Disponibles</h5>
              </div>
              <div className="card-body">
                <div className="row">
                  <div className="col-12">
                    <p className="text-muted text-center">No hay doctores disponibles en este momento</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </BaseDashboard>
  );
};

export default PacienteDashboard; 