"""API REST del proyecto: autenticación, usuarios, servicios y productos.

Ejecutar:  uvicorn app.main:app --reload --port 8000
Swagger:   http://localhost:8000/docs
"""
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .auth import ServicioAuth
from .repositories import Duplicado, NoEncontrado, RepositorioProductos, RepositorioServicios, RepositorioUsuarios
from .routers import auth, productos, servicios, usuarios


def crear_app() -> FastAPI:
    app = FastAPI(
        title="API del proyecto",
        version="1.0.0",
        description="API REST para pequeñas y medianas empresas: autenticación, usuarios, servicios y productos.",
    )
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

    app.state.usuarios = RepositorioUsuarios()
    app.state.servicios = RepositorioServicios()
    app.state.productos = RepositorioProductos()
    app.state.auth = ServicioAuth(app.state.usuarios)
    _datos_iniciales(app)

    @app.exception_handler(NoEncontrado)
    async def _404(_: Request, exc: NoEncontrado):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(Duplicado)
    async def _409(_: Request, exc: Duplicado):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.get("/", tags=["Estado"], summary="Comprobar que la API está activa")
    def estado():
        return {"mensaje": "API del proyecto funcionando", "documentacion": "/docs"}

    for r in (auth.router, usuarios.router, servicios.router, productos.router):
        app.include_router(r)
    return app


def _datos_iniciales(app: FastAPI) -> None:
    """Datos de demostración. Cambia el administrador con las variables ADMIN_EMAIL y ADMIN_PASSWORD."""
    app.state.usuarios.crear({
        "nombre": "Administrador",
        "email": os.getenv("ADMIN_EMAIL", "admin@example.com"),
        "rol": "admin",
        "password_hash": ServicioAuth.hash_password(os.getenv("ADMIN_PASSWORD", "Admin12345")),
    })
    app.state.servicios.crear({"nombre": "Soporte técnico", "descripcion": "Atención remota", "precio": 60000, "activo": True})
    app.state.productos.crear({"nombre": "Teclado mecánico", "precio": 185000})
    app.state.productos.crear({"nombre": "Memoria USB 64 GB", "precio": 40000})


app = crear_app()
