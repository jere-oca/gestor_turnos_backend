# Script para ejecutar pruebas de carga y evaluación de rendimiento
# Guardar como run_performance_tests.ps1

Write-Host "===== INICIANDO PRUEBAS DE RENDIMIENTO =====" -ForegroundColor Green
Write-Host "Fecha: $(Get-Date)"
Write-Host ""

# 1. Ejecutar migraciones para asegurar que la base de datos está actualizada
Write-Host "Ejecutando migraciones..." -ForegroundColor Yellow
python manage.py migrate
Write-Host "✅ Migraciones completadas" -ForegroundColor Green
Write-Host ""

# 2. Generar datos de prueba
Write-Host "Generando datos de prueba..." -ForegroundColor Yellow
Write-Host "Esto puede tardar varios minutos dependiendo de la cantidad de registros."
python manage.py generate_auth_users --cantidad 10000 --batch 1000
Write-Host "✅ Datos de prueba generados" -ForegroundColor Green
Write-Host ""

# 3. Realizar benchmarks iniciales (sin índices adicionales)
Write-Host "Realizando benchmarks iniciales (sin índices adicionales)..." -ForegroundColor Yellow
python manage.py benchmark_queries --queries 100
Write-Host "✅ Benchmarks iniciales completados" -ForegroundColor Green
Write-Host ""

# 4. Aplicar la migración para añadir índices
Write-Host "Aplicando migración para añadir índices..." -ForegroundColor Yellow
python manage.py migrate
Write-Host "✅ Índices aplicados" -ForegroundColor Green
Write-Host ""

# 5. Realizar benchmarks después de añadir índices
Write-Host "Realizando benchmarks con índices..." -ForegroundColor Yellow
python manage.py benchmark_queries --queries 100
Write-Host "✅ Benchmarks con índices completados" -ForegroundColor Green
Write-Host ""

# 6. Exportar datos a CSV para análisis externos
Write-Host "Exportando datos a CSV..." -ForegroundColor Yellow
python manage.py export_auth_users_to_csv --cantidad 5000 --output csv_exports
Write-Host "✅ Datos exportados a CSV" -ForegroundColor Green
Write-Host ""

Write-Host "===== PRUEBAS DE RENDIMIENTO COMPLETADAS =====" -ForegroundColor Green
Write-Host "Revise los resultados para analizar las mejoras de rendimiento con los índices aplicados."
Write-Host ""
