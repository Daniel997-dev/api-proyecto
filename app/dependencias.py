"""Dependencias inyectadas en los endpoints (repositorios, sesión y roles)."""
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer = HTTPBearer(auto_error=False)


def repo_productos(request: Request):
    return request.app.state.productos


def repo_servicios(request: Request):
    return request.app.state.servicios


def repo_usuarios(request: Request):
    return request.app.state.usuarios


def servicio_auth(request: Request):
    return request.app.state.auth


def token_actual(cred: HTTPAuthorizationCredentials = Depends(bearer)) -> str:
    if cred is None:
        raise HTTPException(401, "Falta el token. Inicia sesión en /auth/login.", headers={"WWW-Authenticate": "Bearer"})
    return cred.credentials


def usuario_actual(token: str = Depends(token_actual), auth=Depends(servicio_auth)) -> dict:
    usuario = auth.usuario_de(token)
    if usuario is None:
        raise HTTPException(401, "Token inválido o sesión cerrada.", headers={"WWW-Authenticate": "Bearer"})
    return usuario


def requiere_admin(usuario: dict = Depends(usuario_actual)) -> dict:
    if usuario["rol"] != "admin":
        raise HTTPException(403, "Solo un administrador puede realizar esta acción.")
    return usuario
