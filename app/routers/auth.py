from fastapi import APIRouter, Depends, HTTPException, Response

from ..dependencias import servicio_auth, token_actual, usuario_actual
from ..models import CambioPassword, LoginIn, TokenOut, UsuarioPublico

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenOut, summary="Iniciar sesión (crea un token)")
def login(datos: LoginIn, auth=Depends(servicio_auth)):
    token = auth.login(datos.email, datos.password)
    if token is None:
        raise HTTPException(401, "Correo o contraseña incorrectos.")
    return TokenOut(access_token=token)


@router.get("/me", response_model=UsuarioPublico, summary="Ver el usuario de la sesión actual")
def me(usuario: dict = Depends(usuario_actual)):
    return usuario


@router.put("/password", status_code=204, summary="Cambiar la contraseña")
def cambiar_password(datos: CambioPassword, usuario: dict = Depends(usuario_actual), auth=Depends(servicio_auth)):
    if not auth.cambiar_password(usuario, datos.actual, datos.nueva):
        raise HTTPException(400, "La contraseña actual no es correcta.")
    return Response(status_code=204)


@router.delete("/logout", status_code=204, summary="Cerrar sesión (elimina el token)")
def logout(token: str = Depends(token_actual), auth=Depends(servicio_auth)):
    auth.logout(token)
    return Response(status_code=204)
