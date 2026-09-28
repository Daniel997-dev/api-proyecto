"""Esquemas (Pydantic): definen y validan el JSON que entra y sale de la API."""
from typing import Literal, Optional

from pydantic import BaseModel, Field

EMAIL = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


# ---------- Productos ----------
class ProductoBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    precio: float = Field(ge=0)


class ProductoCrear(ProductoBase):
    id: Optional[int] = Field(default=None, gt=0)  # si no se envía, la API lo asigna


class Producto(ProductoBase):
    id: int


# ---------- Servicios ----------
class ServicioBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    descripcion: str = Field(default="", max_length=300)
    precio: float = Field(ge=0)
    activo: bool = True


class ServicioCrear(ServicioBase):
    id: Optional[int] = Field(default=None, gt=0)


class Servicio(ServicioBase):
    id: int


# ---------- Usuarios ----------
class UsuarioBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    email: str = Field(pattern=EMAIL)
    rol: Literal["admin", "usuario"] = "usuario"


class UsuarioCrear(UsuarioBase):
    password: str = Field(min_length=8, max_length=64)


class UsuarioPublico(UsuarioBase):
    id: int  # nunca se expone la contraseña ni su hash


# ---------- Autenticación ----------
class LoginIn(BaseModel):
    email: str = Field(pattern=EMAIL)
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CambioPassword(BaseModel):
    actual: str
    nueva: str = Field(min_length=8, max_length=64)
