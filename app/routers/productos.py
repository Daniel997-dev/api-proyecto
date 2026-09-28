from fastapi import APIRouter, Depends, Response

from ..dependencias import repo_productos
from ..models import Producto, ProductoBase, ProductoCrear

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("", response_model=list[Producto], summary="Listar productos")
def listar(repo=Depends(repo_productos)):
    return repo.listar()


@router.get("/{producto_id}", response_model=Producto, summary="Obtener un producto")
def obtener(producto_id: int, repo=Depends(repo_productos)):
    return repo.obtener(producto_id)


@router.post("", response_model=Producto, status_code=201, summary="Crear un producto")
def crear(datos: ProductoCrear, repo=Depends(repo_productos)):
    return repo.crear(datos.model_dump())


@router.put("/{producto_id}", response_model=Producto, summary="Modificar un producto")
def actualizar(producto_id: int, datos: ProductoBase, repo=Depends(repo_productos)):
    return repo.actualizar(producto_id, datos.model_dump())


@router.delete("/{producto_id}", status_code=204, summary="Eliminar un producto")
def eliminar(producto_id: int, repo=Depends(repo_productos)):
    repo.eliminar(producto_id)
    return Response(status_code=204)
