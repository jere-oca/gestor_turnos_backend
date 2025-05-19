import React from 'react';
import BaseDashboard from './BaseDashboard';

const DoctorDashboard = ({ nombre, apellido, tipo_usuario, turnos, messages }) => {
  const sidebarMenu = (
    <>
      <a href="#mis-turnos">Mis Turnos</a>
      <a href="#mis-pacientes">Mis Pacientes</a>
      <a href="#horarios">Gestionar Horarios</a>
      <a href="#historial">Historial Médico</a>
    </>
  );
  return (
    <BaseDashboard nombre={nombre} apellido={apellido} tipo_usuario={tipo_usuario} sidebarMenu={sidebarMenu} pageTitle="Dashboard Doctor" messages={messages}>
      <div className="container-fluid">
        <div className="row">
          {/* Resumen de Turnos */}
          <div className="col-md-6 mb-4">
            <div className="card">
              <div className="card-header">
                <h5 className="card-title mb-0">Turnos del Día</h5>
              </div>
              <div className="card-body">
                <div className="list-group">
                  {/* Aquí se listarán los turnos */}
                  <p className="text-muted">No hay turnos programados para hoy.</p>
                </div>
                <a href="/crear-turno" className="btn btn-primary mt-3">Crear Turno</a>
              </div>
            </div>
          </div>
          {/* Estadísticas */}
          <div className="col-md-6 mb-4">
            <div className="card">
              <div className="card-header">
                <h5 className="card-title mb-0">Estadísticas</h5>
              </div>
              <div className="card-body">
                <div className="row">
                  <div className="col-6 mb-3">
                    <h6>Pacientes Totales</h6>
                    <h2>0</h2>
                  </div>
                  <div className="col-6 mb-3">
                    <h6>Turnos Pendientes</h6>
                    <h2>0</h2>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        {/* Próximos Turnos */}
        <div className="row">
          <div className="col-12">
            <div className="card">
              <div className="card-header">
                <h5 className="card-title mb-0">Próximos Turnos</h5>
              </div>
              <div className="card-body">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Fecha</th>
                      <th>Hora</th>
                      <th>Paciente</th>
                      <th>Estado</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td colSpan="5" className="text-center">No hay turnos próximos</td>
                    </tr>
                    {/* {turnos.map(turno => (
                      <tr key={turno.id}>
                        <td>{turno.fecha}</td>
                        <td>{turno.hora}</td>
                        <td>{turno.paciente}</td>
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
      </div>
    </BaseDashboard>
  );
};

export default DoctorDashboard; 