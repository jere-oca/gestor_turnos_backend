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
> Las migraciones de base de datos se aplican automáticamente al iniciar el contenedor del backend gracias al script `entrypoint.sh`. No es necesario ejecutar `python manage.py migrate` de forma manual.

### 3. (Opcional) Cargar datos de ejemplo

```bash
docker compose exec web python manage.py loaddata fixtures/initial_data.json
```

### 4. Acceder a la aplicación

- Frontend: [http://localhost:3000/](http://localhost:3000/)
- Backend (API): [http://localhost:8000/](http://localhost:8000/)

## 🧪 Testing

### Tests de performance

```bash
docker compose exec backend /app/backend/run_performance_tests.sh
```