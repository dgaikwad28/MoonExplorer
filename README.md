**# MoonExplorer

# MoonExplorer Setup Guide (Docker Compose)

This guide explains how to set up and run the MoonExplorer project using Docker Compose. It covers environment configuration, logging, Nginx, running tests, requirements, and database migrations with Alembic.

---

## 1. Prerequisites
- [Docker](https://www.docker.com/products/docker-desktop) and [Docker Compose](https://docs.docker.com/compose/) installed

---

## 2. Clone the Repository
```bash
git clone https://github.com/dgaikwad28/MoonExplorer.git
cd MoonExplorer
```

---

## 3. Environment Variables
- Copy the example environment file:
  ```bash
  cp env/example.env .env
  ```
- Edit `.env` to set your environment variables (e.g., database URL, secret keys, debug mode, etc.)

---

## 4. Logs
- Logs are written to the `logs/` directory (e.g., `logs/api.log`).
- Ensure this directory exists and is writable by the Docker container.

---

## 5. Nginx
- Nginx is configured as a reverse proxy for the FastAPI app.
- Configuration files are in the `nginx/` directory:
  - `nginx.conf`: Main config
  - `sites-available/`: Site-specific configs
  - `snippets/`: Reusable config snippets
- Nginx is started as a service in `docker-compose.yml`.

---

## 6. Requirements
- Python dependencies are listed in `requirements/requirements.txt` and `requirements/requirements.in`.
- Docker will install these automatically when building the image.

---

## 7. Alembic (Database Migrations)
- Alembic is used for managing database schema migrations.
- Migration scripts are in the `alembic/versions/` directory.
- To run migrations inside the container:
  ```bash
  docker-compose exec app alembic upgrade head
  ```
- To create a new migration after changing models:
  ```bash
  docker-compose exec app alembic revision --autogenerate -m "Your migration message"
  ```

---

## 8. Running the Application
- Build and start all services:
  ```bash
  docker-compose up --build
  ```
- The FastAPI app will be available at `http://localhost:7000` (proxied by Nginx).

---

## 9. Running Tests
- To run tests inside the container:
  ```bash
  docker-compose exec app pytest
  ```
- Test files are located in the `tests/` directory and use `pytest`.

---

## 10. Useful Docker Compose Commands
- Start services: `docker-compose up`
- Stop services: `docker-compose down`
- Rebuild images: `docker-compose build`
- View logs: `docker-compose logs`

---

## 11. Troubleshooting
- Ensure `.env` and `logs/` exist and are accessible.
- Check Docker and Nginx logs for errors.
- For database issues, verify Alembic migrations and DB connection settings.

---

## 12. Project Structure Overview
- `app/` - Main FastAPI application code
- `alembic/` - Database migration scripts
- `nginx/` - Nginx configuration
- `logs/` - Log files
- `env/` - Example environment files
- `requirements/` - Python dependency files
- `tests/` - Unit and API tests

---

