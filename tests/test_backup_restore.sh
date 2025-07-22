#!/bin/bash

# Tests para Sistema de Backup & Restore

echo "EJECUTANDO TESTS DE BACKUP & RESTORE"
echo "======================================="
echo ""

# Configuración
TEST_START_TIME=$(date +%s)
BACKUP_DIR="/app/backups"
TESTS_PASSED=0
TESTS_FAILED=0
TEST_DB_NAME="${DATABASE_NAME:-gestor_turnos}"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funcion para ejecutar un test
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_result="$3"
    
    echo -n " Test: $test_name... "
    
    # Ejecutar el comando y capturar resultado
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN} PASS${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED} FAIL${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

# Funcion para verificar archivos
check_file_exists() {
    local file_path="$1"
    [ -f "$file_path" ]
}

# Funcion para contar registros en BD
count_users() {
    PGPASSWORD="$DATABASE_PASSWORD" psql \
        -h ${DATABASE_HOST:-db} -p ${DATABASE_PORT:-5432} -U ${DATABASE_USERNAME:-postgres} -d $TEST_DB_NAME \
        -t -c "SELECT COUNT(*) FROM authentification_authuser;" 2>/dev/null | xargs
}

echo "TESTS BÁSICOS DE INFRAESTRUCTURA"
echo "-----------------------------------"

# Test 1: Verificar que el directorio de backups existe
run_test "Directorio de backups existe" "[ -d '$BACKUP_DIR' ]"

# Test 2: Verificar que los scripts existen
run_test "Script de backup existe" "[ -f '/app/scripts/backup_simple.sh' ]"
run_test "Script de restore existe" "[ -f '/app/scripts/restore_simple.sh' ]"

# Test 3: Verificar permisos de ejecución
run_test "Script backup es ejecutable" "[ -x '/app/scripts/backup_simple.sh' ]"
run_test "Script restore es ejecutable" "[ -x '/app/scripts/restore_simple.sh' ]"

echo ""
echo "TESTS FUNCIONALES DE BACKUP"
echo "------------------------------"

# Test 4: Crear backup y verificar que se crea el archivo
INITIAL_USER_COUNT=$(count_users)
echo "Usuarios iniciales en BD: $INITIAL_USER_COUNT"

run_test "Crear backup exitoso" "bash /app/scripts/backup_simple.sh"

# Test 5: Verificar que se creo un archivo de backup
LATEST_BACKUP=$(find $BACKUP_DIR -name "backup_*.sql" -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)
run_test "Archivo de backup creado" "check_file_exists '$LATEST_BACKUP'"

# Test 6: Verificar que el backup no esta vacio
run_test "Backup no esta vacio" "[ -s '$LATEST_BACKUP' ]"

# Test 7: Verificar contenido del backup
run_test "Backup contiene SQL valido" "grep -q 'PostgreSQL database dump' '$LATEST_BACKUP'"

echo ""
echo "TESTS FUNCIONALES DE RESTORE"
echo "-------------------------------"

# Test 8: Agregar datos de prueba
echo "Agregando usuario de prueba para validar restore..."
PGPASSWORD="$DATABASE_PASSWORD" psql \
    -h ${DATABASE_HOST:-db} -p ${DATABASE_PORT:-5432} -U ${DATABASE_USERNAME:-postgres} -d $TEST_DB_NAME \
    -c "INSERT INTO authentification_authuser (username, password) VALUES ('test_user_$(date +%s)', 'test123');" > /dev/null 2>&1

NEW_USER_COUNT=$(count_users)
echo "Usuarios despues de agregar prueba: $NEW_USER_COUNT"

# Test 9: Verificar que se agrego el usuario
run_test "Usuario de prueba agregado" "[ $NEW_USER_COUNT -gt $INITIAL_USER_COUNT ]"

# Test 10: Listar backups disponibles
run_test "Listar backups funciona" "bash /app/scripts/restore_simple.sh --list"

# Test 11: Restore desde backup (automatico para test)
echo "Ejecutando restore automatico..."
echo "y" | bash /app/scripts/restore_simple.sh $(basename "$LATEST_BACKUP") > /dev/null 2>&1
RESTORED_USER_COUNT=$(count_users)

run_test "Restore ejecutado correctamente" "[ $? -eq 0 ]"
run_test "Datos restaurados correctamente" "[ $RESTORED_USER_COUNT -eq $INITIAL_USER_COUNT ]"

echo ""
echo "TESTS DE RENDIMIENTO"
echo "----------------------"

# Test 12: Tiempo de backup
echo -n "Test: Tiempo de backup... "
START_TIME=$(date +%s)
bash /app/scripts/backup_simple.sh > /dev/null 2>&1
END_TIME=$(date +%s)
BACKUP_TIME=$((END_TIME - START_TIME))

if [ $BACKUP_TIME -lt 30 ]; then
    echo -e "${GREEN} PASS (${BACKUP_TIME}s < 30s)${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${YELLOW} SLOW (${BACKUP_TIME}s >= 30s)${NC}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 13: Tamaño del backup
BACKUP_SIZE=$(du -k "$LATEST_BACKUP" | cut -f1)
echo -n "Test: Tamaño del backup... "
if [ $BACKUP_SIZE -gt 10 ]; then
    echo -e "${GREEN} PASS (${BACKUP_SIZE}KB > 10KB)${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED} FAIL (${BACKUP_SIZE}KB <= 10KB)${NC}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

echo ""
echo "TESTS DE LIMPIEZA"
echo "-------------------"

# Test 14: Limpiar backups de prueba más antiguos
BACKUP_COUNT_BEFORE=$(find $BACKUP_DIR -name "backup_*.sql" | wc -l)
# Simular limpieza (mantener últimos 3)
find $BACKUP_DIR -name "backup_*.sql" -type f -printf '%T@ %p\n' | sort -n | head -n -3 | cut -d' ' -f2- | while read file; do
    [ -n "$file" ] && rm -f "$file"
done
BACKUP_COUNT_AFTER=$(find $BACKUP_DIR -name "backup_*.sql" | wc -l)

run_test "Limpieza de backups antiguos" "[ $BACKUP_COUNT_AFTER -le $BACKUP_COUNT_BEFORE ]"

echo ""
echo "RESUMEN DE TESTS"
echo "=================="

TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED))
if [ $TOTAL_TESTS -gt 0 ]; then
    SUCCESS_RATE=$((TESTS_PASSED * 100 / TOTAL_TESTS))
else
    SUCCESS_RATE=0
fi
TEST_DURATION=$(($(date +%s) - TEST_START_TIME))

echo "Tests ejecutados: $TOTAL_TESTS"
echo "Tests exitosos: $TESTS_PASSED"
echo "Tests fallidos: $TESTS_FAILED"
echo "Tasa de exito: $SUCCESS_RATE%"
echo "Duración total: ${TEST_DURATION}s"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "\n ${GREEN}TODOS LOS TESTS PASARON EXITOSAMENTE${NC}"
    exit 0
else
    echo -e "\n  ${YELLOW}ALGUNOS TESTS FALLARON${NC}"
    exit 1
fi
