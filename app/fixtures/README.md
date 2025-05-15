# Fixtures para Gestor de Turnos

Este directorio contiene los datos iniciales para la aplicación.

## Cómo cargar los datos

Para cargar los datos en tu base de datos local, ejecuta:

```bash
# Si estás usando Docker:
docker compose exec web python manage.py loaddata fixtures/initial_data.json

# Si estás en desarrollo local:
python manage.py loaddata fixtures/initial_data.json
```

## Cómo actualizar los fixtures

Para actualizar los datos con los cambios más recientes de tu base de datos:

```bash
# Si estás usando Docker:
docker compose exec web python manage.py dumpdata --exclude auth.permission --exclude contenttypes --exclude admin.logentry --indent 2 > fixtures/initial_data.json

# Si estás en desarrollo local:
python manage.py dumpdata --exclude auth.permission --exclude contenttypes --exclude admin.logentry --indent 2 > fixtures/initial_data.json
```

## Contenido

El archivo `initial_data.json` contiene:
- Usuarios y sus roles
- Datos de personas (doctores, pacientes, administrativos)
- Turnos y configuraciones del sistema 