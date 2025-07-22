#!/bin/bash

echo "EJECUTANDO SUITE DE TESTS - GESTOR DE TURNOS"
echo "================================================"
echo ""

# Ejecutar test de backup
echo "Ejecutando tests de Backup & Restore..."
bash /app/tests/test_backup_restore.sh

echo ""
echo "SUITE DE TESTS COMPLETADA"