# Backend Hackathon

## Tabla de Contenidos 📑

- [Acerca de la aplicación](#acerca-de-la-aplicacion)
- [Tecnologías](#tecnologias)
- [Instalación](#instalacion)

## Acerca de la aplicación 📚

Proyecto de backend para el **Hackathon**

## Tecnologías ☕️ ⚛️

- **FastAPI** 🚀
- **SQLModel**
- **FastAPI Users** 🔑
- **Casbin**
- **PostgreSQL** 🐘

## Instalación ⚙️

1. Tener instalado **PostgreSQL**
2. Crear la base de datos `hackathon_backend`
3. Crear un esquema llamado `security`
4. Tener instalado **Python >= 3.13**
5. Clonar este repositorio
6. Instalar **Poetry** → [Guía oficial](https://python-poetry.org/docs/#installing-with-the-official-installer)
7. Instalar dependencias:
   ```bash
   poetry install
   ```
8. Configurar el archivo de entorno:
   ```bash
   cp .env.example .env
   ```
   Luego, establecer los valores de las variables de entorno según corresponda.
9. Aplicar las migraciones de base de datos:
   ```bash
   poetry run alembic upgrade head
   ```
10. Iniciar el servidor de desarrollo:
    ```bash
    poetry run fastapi dev src/hackathon_backend/main.py
    ```
