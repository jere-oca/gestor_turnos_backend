# Backend de Gestor de Turnos

> Fork personal del repositorio `gestor_turnos` ([Grupo9](https://github.com/UTN-BDA/Grupo9))

## Tecnologías

- **Backend:** Python, Django + Django REST Framework
- **Frontend:** React
- **Base de datos:** PostgreSQL
- **Contenedores:** Docker + Docker Compose
- **Control de versiones:** Git + GitHub

## Requisitos previos

- [Docker Compose](https://docs.docker.com/compose/install/) (generalmente ya incluido en Docker Desktop)

## ⚙️ Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/UTN-BDA/Grupo9.git
cd Grupo9
```

### 2. Levantar los contenedores

```bash
docker compose up -d
```

> - Las migraciones de base de datos se aplican automáticamente al iniciar el contenedor `backend` gracias al script `entrypoint.sh`.
> - Los datos de ejemplo (fixtures) se cargan automáticamente.

### 3. Acceder a la aplicación

- **Frontend:** [http://localhost:3000/](http://localhost:3000/)
- **Panel de administración:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

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

# Verificar que la API de turnos solicita autenticación
curl http://localhost:8000/api/turnos/
```

### 5. (Opcional) Crear superusuario de Django

Para acceder al panel de administración, crea un superusuario ejecutando:

```bash
docker compose exec backend python manage.py createsuperuser
```

Luego podrás ingresar al panel de administración en: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Testing

### Tests de performance

```bash
docker compose exec backend bash /app/backend/run_performance_tests.sh
```

## Solución de problemas

### Problema: "Las credenciales de autenticación no se proveyeron"
- **Causa**: Este es el comportamiento normal de la API REST
- **Solución**: Usar las credenciales de usuarios de prueba para autenticarse


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

## Restaurar Backup

Antes de restaurar la base de datos debemos ejecutar

```bash
docker compose exec backend bash
```

```bash
apt-get update && apt-get install -y dos2unix
dos2unix /app/scripts/restore_simple.sh
chmod +x /app/scripts/restore_simple.sh
/app/scripts/restore_simple.sh backup_mydatabase_20250723_155410.sql
# Podemos elegir ese archivo de backup o el ultimo que generemos
```
