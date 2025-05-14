# 🗓️ Gestor de Turnos - Proyecto Django

Este proyecto es una aplicación web para gestionar turnos

## 🚀 Tecnologías utilizadas

- **Backend:** Python 3.12, Django 5.2
- **Base de datos:** PostgreSQL
- **Control de versiones:** Git + GitHub

## 👨‍💻 Miembros del equipo

- Jeremias Ocaña
- Lautaro Sanz
- Santiago Sabio

## 🔧 Cómo ejecutar el proyecto

### 📥 Clonar el repositorio
```bash
git clone https://github.com/UTN-BDA/Grupo9.git
cd Grupo9
```
### 🐳 Levantar los contenedores
```bash
docker-compose up -d --build
```
### 🗃️ Aplicar migraciones de base de datos
```bash
docker compose exec web bash
python manage.py migrate
```
### 🌐 Acceder a la aplicación
```bash
http://localhost:8000/
```
