"""Guarda los datos en memoria (diccionarios). Las clases de abajo heredan de esta."""
from typing import Optional


class NoEncontrado(Exception):
    """El recurso pedido no existe (HTTP 404)."""


class Duplicado(Exception):
    """El recurso ya existe (HTTP 409)."""


class RepositorioMemoria:
    nombre_recurso = "Recurso"

    def __init__(self) -> None:
        self._datos: dict[int, dict] = {}
        self._siguiente = 1

    def listar(self) -> list[dict]:
        return [dict(d) for d in self._datos.values()]

    def obtener(self, id: int) -> dict:
        if id not in self._datos:
            raise NoEncontrado(f"{self.nombre_recurso} no encontrado")
        return dict(self._datos[id])

    def crear(self, datos: dict) -> dict:
        id_ = datos.get("id") or self._siguiente
        if id_ in self._datos:
            raise Duplicado(f"Ya existe un {self.nombre_recurso.lower()} con ese ID")
        self._validar_unicos(datos)
        self._datos[id_] = {**datos, "id": id_}
        self._siguiente = max(self._siguiente, id_ + 1)
        return dict(self._datos[id_])

    def actualizar(self, id: int, datos: dict) -> dict:
        actual = self.obtener(id)
        self._validar_unicos(datos, ignorar_id=id)
        self._datos[id] = {**actual, **datos, "id": id}
        return dict(self._datos[id])

    def eliminar(self, id: int) -> None:
        self.obtener(id)
        del self._datos[id]

    def _validar_unicos(self, datos: dict, ignorar_id: Optional[int] = None) -> None:
        """Las subclases lo sobrescriben si tienen campos únicos."""


class RepositorioProductos(RepositorioMemoria):
    nombre_recurso = "Producto"


class RepositorioServicios(RepositorioMemoria):
    nombre_recurso = "Servicio"


class RepositorioUsuarios(RepositorioMemoria):
    nombre_recurso = "Usuario"

    def buscar_por_email(self, email: str) -> Optional[dict]:
        return next((dict(u) for u in self._datos.values() if u["email"].lower() == email.lower()), None)

    def _validar_unicos(self, datos: dict, ignorar_id: Optional[int] = None) -> None:
        if "email" in datos:
            otro = self.buscar_por_email(datos["email"])
            if otro and otro["id"] != ignorar_id:
                raise Duplicado("Ya existe un usuario con ese correo")
