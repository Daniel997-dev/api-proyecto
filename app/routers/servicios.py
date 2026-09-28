from fastapi import APIRouter, Depends, Response

from ..dependencias import repo_servicios
from ..models import Servicio, ServicioBase, ServicioCrear

router = APIRouter(prefix="/servicios", tags=["Servicios"])


@router.get("", response_model=list[Servicio], summary="Listar servicios")
def listar(repo=Depends(repo_servicios)):
    return repo.listar()


@router.get("/{servicio_id}", response_model=Servicio, summary="Obtener un servicio")
def obtener(servicio_id: int, repo=Depends(repo_servicios)):
    return repo.obtener(servicio_id)


@router.post("", response_model=Servicio, status_code=201, summary="Crear un servicio")
def crear(datos: ServicioCrear, repo=Depends(repo_servicios)):
    return repo.crear(datos.model_dump())


@router.put("/{servicio_id}", response_model=Servicio, summary="Modificar un servicio")
def actualizar(servicio_id: int, datos: ServicioBase, repo=Depends(repo_servicios)):
    return repo.actualizar(servicio_id, datos.model_dump())


@router.delete("/{servicio_id}", status_code=204, summary="Eliminar un servicio")
def eliminar(servicio_id: int, repo=Depends(repo_servicios)):
    repo.eliminar(servicio_id)
    return Response(status_code=204)
