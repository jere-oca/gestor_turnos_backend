import React from 'react';
import BaseDashboard from './BaseDashboard';

const AdminDashboard = ({ nombre, apellido, tipo_usuario, turnos, messages }) => {
  const sidebarMenu = (
    <>
      <a href="#usuarios">Gestionar Usuarios</a>
      <a href="#turnos">Gestionar Turnos</a>
      <a href="#doctores">Gestionar Doctores</a>
      <a href="#reportes">Reportes</a>
    </>
  );
  return (
    <BaseDashboard nombre={nombre} apellido={apellido} tipo_usuario={tipo_usuario} sidebarMenu={sidebarMenu} pageTitle="Dashboard Administrativo" messages={messages}>
      <div className="container-fluid">
        <div className="row">
          {/* Estadísticas Generales */}
          <div className="col-md-12 mb-4">
            <div className="card">
              <div className="card-header">
                <h5 className="card-title mb-0">Estadísticas Generales</h5>
              </div>
              <div className="card-body">
                <div className="row">
                  <div className="col-md-3 col-sm-6 mb-3">
                    <div className="card bg-primary text-white">
                      <div className="card-body">
                        <h5 className="card-title">Total Pacientes</h5>
                        <h2>0</h2>
                      </div>
                    </div>
                  </div>
                  <div className="col-md-3 col-sm-6 mb-3">
                    <div className="card bg-success text-white">
                      <div className="card-body">
                        <h5 className="card-title">Total Doctores</h5>
                        <h2>0</h2>
                      </div>
                    </div>
                  </div>
                  <div className="col-md-3 col-sm-6 mb-3">
                    <div className="card bg-info text-white">
                      <div className="card-body">
                        <h5 className="card-title">Turnos Hoy</h5>
                        <h2>0</h2>
                      </div>
                    </div>
                  </div>
                  <div className="col-md-3 col-sm-6 mb-3">
                    <div className="card bg-warning text-white">
                      <div className="card-body">
                        <h5 className="card-title">Turnos Pendientes</h5>
                        <h2>0</h2>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="row">
          {/* Últimos Usuarios Registrados */}
          <div className="col-md-6 mb-4">
            <div className="card">
              <div className="card-header d-flex justify-content-between align-items-center">
                <h5 className="card-title mb-0">Últimos Usuarios Registrados</h5>
                <button className="btn btn-primary btn-sm">Ver Todos</button>
              </div>
              <div className="card-body">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Nombre</th>
                      <th>Tipo</th>
                      <th>Fecha Registro</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td colSpan="4" className="text-center">No hay usuarios registrados</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          {/* Próximos Turnos */}
          <div className="col-md-6 mb-4">
            <div className="card">
              <div className="card-header d-flex justify-content-between align-items-center">
                <h5 className="card-title mb-0">Próximos Turnos</h5>
                <button className="btn btn-primary btn-sm">Ver Todos</button>
              </div>
              <div className="card-body">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Fecha</th>
                      <th>Doctor</th>
                      <th>Paciente</th>
                      <th>Estado</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td colSpan="4" className="text-center">No hay turnos programados</td>
                    </tr>
                    {/* {turnos.map(turno => (
                      <tr key={turno.id}>
                        <td>{turno.fecha}</td>
                        <td>{turno.doctor}</td>
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
        {/* Acciones Rápidas */}
        <div className="row">
          <div className="col-12">
            <div className="card">
              <div className="card-header">
                <h5 className="card-title mb-0">Acciones Rápidas</h5>
              </div>
              <div className="card-body">
                <div className="row">
                  <div className="col-md-3 col-sm-6 mb-3">
                    <a href="#" className="btn btn-primary w-100">
                      <i className="fas fa-user-plus"></i> Nuevo Usuario
                    </a>
                  </div>
                  <div className="col-md-3 col-sm-6 mb-3">
                    <a href="#" className="btn btn-success w-100">
                      <i className="fas fa-calendar-plus"></i> Nuevo Turno
                    </a>
                  </div>
                  <div className="col-md-3 col-sm-6 mb-3">
                    <a href="#" className="btn btn-info w-100">
                      <i className="fas fa-user-md"></i> Nuevo Doctor
                    </a>
                  </div>
                  <div className="col-md-3 col-sm-6 mb-3">
                    <a href="#" className="btn btn-warning w-100">
                      <i className="fas fa-file-alt"></i> Generar Reporte
                    </a>
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

export default AdminDashboard; 