# 🗓️ Gestor de Turnos - UTN

Aplicación web para la gestión de turnos médicos, desarrollada como proyecto académico para la UTN. Permite a pacientes, profesionales y personal administrativo gestionar reservas de turnos, agendas y atención de manera eficiente.

## 🚀 Tecnologías principales

- **Backend:** Python 3.12, Django 5.2
- **Frontend:** React
- **Base de datos:** PostgreSQL
- **Contenedores:** Docker + Docker Compose
- **Control de versiones:** Git + GitHub

## ⚠️ Requisitos previos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (generalmente ya incluido en Docker Desktop)

## 🗂️ Estructura del repositorio

- `/app/` - Código fuente del backend (Django)
  - `/fixtures/` - Datos iniciales de ejemplo (fixtures)
  - `/frontend/` - Aplicación frontend en React

## 👨‍💻 Miembros del equipo

- Jeremias Ocaña
- Lautaro Sanz
- Santiago Sabio

## ⚙️ Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/UTN-BDA/Grupo9.git
cd Grupo9
```

### 2. Levantar los contenedores

```bash
docker-compose up -d --build
```

> **Nota:**  
> - Las migraciones de base de datos se aplican automáticamente al iniciar el contenedor del backend gracias al script `entrypoint.sh`. 
> - Los datos de ejemplo (fixtures) se cargan automáticamente
> - Las contraseñas se configuran automáticamente de forma segura
> - No es necesario ejecutar comandos adicionales

#### 2.1. (Opcional) Configuración manual

Si por algún motivo la configuración automática no funciona, puedes ejecutar estos comandos manualmente:

```bash
# Aplicar migraciones de base de datos
docker exec backend python manage.py migrate

# Cargar datos de ejemplo
docker exec backend python manage.py loaddata /app/backend/fixtures/initial_data.json

# Configurar contraseñas de forma segura
docker exec backend python manage.py setup_passwords
```

### 3. Acceder a la aplicación

- **Frontend:** [http://localhost:3000/](http://localhost:3000/)
- **Backend (API):** [http://localhost:8000/](http://localhost:8000/)
- **Panel de administración:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

#### 3.1. Endpoints principales de la API

- `POST /api/login/` - Autenticación de usuarios
- `POST /api/logout/` - Cerrar sesión
- `GET /api/turnos/` - Listar turnos (requiere autenticación)
- `POST /api/turnos/` - Crear nuevo turno (requiere autenticación)
- `GET /api/medicos/` - Listar médicos (requiere autenticación)
- `GET /api/pacientes/` - Listar pacientes (requiere autenticación)
- `GET /api/especialidades/` - Listar especialidades (requiere autenticación)

### 4. Usuarios de prueba

Una vez iniciado el sistema, puedes usar estos usuarios para probar:

| Tipo | Username | Password | Descripción |
|------|----------|----------|-------------|
| Admin | `admin` | `admin123` | Personal administrativo |
| Médico | `medico1` | `medico123` | Profesional médico |
| Paciente | `paciente1` | `paciente123` | Paciente del sistema |

#### 4.1. Verificación del sistema

Para verificar que todo funciona correctamente:

```bash
# Verificar que todos los contenedores están corriendo
docker-compose ps

# Probar el login de API (debe devolver respuesta exitosa)
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Verificar que la API de turnos está protegida (debe pedir autenticación)
curl http://localhost:8000/api/turnos/
```

### 5. (Opcional) Crear superusuario de Django

Para acceder al panel de administración, crea un superusuario ejecutando:

```bash
docker compose exec backend python manage.py createsuperuser
```

Luego podrás ingresar al panel de administración en: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## 🧪 Testing

### Tests de performance

```bash
docker compose exec backend bash /app/backend/run_performance_tests.sh
```

## 🔧 Solución de problemas

### Problema: "Las credenciales de autenticación no se proveyeron"
- **Causa**: Este es el comportamiento normal de la API REST
- **Solución**: Usar las credenciales de usuarios de prueba para autenticarse

### Problema: Los contenedores no se inician correctamente
```bash
# Verificar el estado de los contenedores
docker-compose ps

# Ver logs en caso de errores
docker-compose logs backend
docker-compose logs db
```

### Problema: Error "No se puede conectar a la base de datos"
```bash
# Reiniciar todos los servicios
docker-compose down
docker-compose up -d --build
```

### Problema: Los datos de ejemplo no aparecen
```bash
# Ejecutar manualmente la configuración
docker exec backend python manage.py migrate
docker exec backend python manage.py loaddata /app/backend/fixtures/initial_data.json
docker exec backend python manage.py setup_passwords
```

### Limpieza completa del sistema
Si necesitas empezar desde cero:
```bash
# Detener y eliminar todo (incluyendo volúmenes)
docker-compose down -v --remove-orphans

# Volver a construir todo
docker-compose up -d --build
```