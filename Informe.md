### 🗃️ Aplicar migraciones de base de datos
```bash
docker-compose exec web bash
python manage.py makemigrations turnos
python manage.py migrate
pip install Faker
python manage.py cargar_clientes
```
