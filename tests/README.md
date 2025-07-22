# Tests - Sistema de Backup & Restore

## Archivos

- `test_backup_restore.sh` - Tests principales del sistema de backup y restore
- `run_all_tests.sh` - Ejecuta todos los tests

## Comandos de Ejecución

### Ejecutar tests individuales
```bash
docker compose exec backend bash /app/tests/test_backup_restore.sh
```

### Ejecutar suite completa
```bash
docker compose exec backend bash /app/tests/run_all_tests.sh
```

## Requisitos

- Contenedores Docker activos
- Variables de entorno configuradas para base de datos