#!/bin/bash
# Script para ejecutar pruebas de carga y evaluación de rendimiento
# Guardar como run_performance_tests.sh

echo "===== INICIANDO PRUEBAS DE RENDIMIENTO ====="
echo "Fecha: $(date)"
echo ""

# 1. Ejecutar migraciones para asegurar que la base de datos está actualizada
echo "Ejecutando migraciones..."
python manage.py migrate
echo "✅ Migraciones completadas"
echo ""

# 2. Generar datos de prueba
echo "Generando datos de prueba..."
echo "Esto puede tardar varios minutos dependiendo de la cantidad de registros."
python manage.py generate_auth_users --cantidad 100 --batch 10
echo "✅ Datos de prueba generados"
echo ""

# 3. Realizar benchmarks iniciales (sin índices adicionales)
echo "Realizando benchmarks iniciales (sin índices adicionales)..."
python manage.py benchmark_queries --queries 100
echo "✅ Benchmarks iniciales completados"
echo ""

# 4. Aplicar la migración para añadir índices
echo "Aplicando migración para añadir índices..."
python manage.py migrate
echo "✅ Índices aplicados"
echo ""

# 5. Realizar benchmarks después de añadir índices
echo "Realizando benchmarks con índices..."
python manage.py benchmark_queries --queries 100
echo "✅ Benchmarks con índices completados"
echo ""

# 6. Exportar datos a CSV para análisis externos
echo "Exportando datos a CSV..."
python manage.py export_auth_users_to_csv --cantidad 100 --output csv_exports
echo "✅ Datos exportados a CSV"
echo ""

echo "===== PRUEBAS DE RENDIMIENTO COMPLETADAS ====="
echo "Revise los resultados para analizar las mejoras de rendimiento con los índices aplicados."
echo ""
