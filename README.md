# API del proyecto

API REST hecha con FastAPI. Tiene 4 módulos: autenticación, usuarios, servicios y productos.
Los datos se guardan en memoria (o sea que se pierden si apagas el servidor) y las contraseñas se guardan con hash, no en texto plano.

## Cómo correrla

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8000
```

Documentación interactiva (Swagger): http://localhost:8000/docs

También se puede correr con Docker:
```bash
docker build -t api-proyecto .
docker run -p 8000:8000 api-proyecto
```

## Pruebas

```bash
pytest -q
```

Para probar los endpoints protegidos en Swagger: primero haz `POST /auth/login` con `admin@example.com` / `Admin12345`, copia el `access_token` que te devuelve, dale click a **Authorize** arriba y pégalo ahí.

## Endpoints

- `/auth` — login, ver sesión actual, cambiar contraseña, logout
- `/usuarios` — requiere estar logueado; crear/editar/borrar requiere rol admin
- `/servicios` — CRUD normal
- `/productos` — CRUD normal (el mismo que usa el frontend)

## Estructura

- `app/main.py` — arma la app, CORS, manejo de errores
- `app/models.py` — los esquemas (validación de lo que entra y sale)
- `app/repositories.py` — donde se guardan los datos, por ahora en memoria
- `app/auth.py` — login, hash de contraseñas, tokens
- `app/dependencias.py` — cosas que se inyectan en los endpoints (repos, sesión, roles)
- `app/routers/` — un archivo por módulo
- `tests/` — pruebas con pytest
