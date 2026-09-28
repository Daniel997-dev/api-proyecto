from fastapi import APIRouter, Depends, Response

from ..auth import ServicioAuth
from ..dependencias import repo_usuarios, requiere_admin, usuario_actual
from ..models import UsuarioBase, UsuarioCrear, UsuarioPublico

# Todo el módulo exige sesión iniciada; crear, modificar y eliminar exigen rol admin.
router = APIRouter(prefix="/usuarios", tags=["Usuarios"], dependencies=[Depends(usuario_actual)])


@router.get("", response_model=list[UsuarioPublico], summary="Listar usuarios")
def listar(repo=Depends(repo_usuarios)):
    return repo.listar()


@router.get("/{usuario_id}", response_model=UsuarioPublico, summary="Obtener un usuario")
def obtener(usuario_id: int, repo=Depends(repo_usuarios)):
    return repo.obtener(usuario_id)


@router.post("", response_model=UsuarioPublico, status_code=201, dependencies=[Depends(requiere_admin)], summary="Crear un usuario")
def crear(datos: UsuarioCrear, repo=Depends(repo_usuarios)):
    d = datos.model_dump(exclude={"password"})
    d["password_hash"] = ServicioAuth.hash_password(datos.password)
    return repo.crear(d)


@router.put("/{usuario_id}", response_model=UsuarioPublico, dependencies=[Depends(requiere_admin)], summary="Modificar un usuario")
def actualizar(usuario_id: int, datos: UsuarioBase, repo=Depends(repo_usuarios)):
    return repo.actualizar(usuario_id, datos.model_dump())


@router.delete("/{usuario_id}", status_code=204, dependencies=[Depends(requiere_admin)], summary="Eliminar un usuario")
def eliminar(usuario_id: int, repo=Depends(repo_usuarios)):
    repo.eliminar(usuario_id)
    return Response(status_code=204)
