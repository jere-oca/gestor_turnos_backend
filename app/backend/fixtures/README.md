#  Fixtures - Datos de Ejemplo

Este directorio contiene datos de ejemplo para el sistema Gestor de Turnos.

## Contenido de los Fixtures

### `initial_data.json` 
Fixture consolidado que contiene todos los datos iniciales en el orden correcto:
- **3 usuarios** con autenticación
- **3 personas** (perfiles de usuario)
- **4 especialidades** médicas
- **1 médico** configurado
- **1 paciente** registrado

**Total: 12 objetos**

### Fixtures individuales 
- `initial_users.json` - Usuarios de autenticación
- `initial_personas.json` - Perfiles de personas
- `initial_especialidades.json` - Especialidades médicas
- `initial_medicos.json` - Médicos registrados
- `initial_pacientes.json` - Pacientes registrados

##  Credenciales de Prueba

### Usuarios del Sistema

| Usuario | Contraseña | Rol | Detalles |
|---------|------------|-----|----------|
| `admin` | `admin123` |  Administrativo | • Acceso completo al sistema<br>• Panel de administración<br>• Gestión de usuarios y configuración |
| `medico1` | `medico123` |  Doctor | • Dr. Juan Pérez<br>• Especialidad: Clínica Médica<br>• Matrícula: 12345<br>• Consultorio: 1 |
| `paciente1` | `paciente123` |  Paciente | • María González<br>• DNI: 12345678<br>• Fecha nacimiento: 01/01/1990<br>• Teléfono: 261-7654321 |

##  Cómo Cargar los Fixtures

```bash
docker compose exec backend python manage.py loaddata /app/backend/fixtures/initial_data.json
```

### Especialidades Disponibles
1. **Clínica Médica** - Enfermedades que afectan a adultos
2. **Pediatría** - Salud de los niños
3. **Ginecología** - Sistema reproductor femenino  
4. **Traumatología** - Lesiones del sistema musculoesquelético

## Resetear Datos

Para limpiar la base de datos y volver a cargar:

```bash
# Limpiar base de datos
docker compose exec backend python manage.py flush --no-input

# Recargar fixtures
docker compose exec backend python manage.py loaddata /app/backend/fixtures/initial_data.json
```