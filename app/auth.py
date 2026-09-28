"""Servicio de autenticación: contraseñas con hash (PBKDF2) y tokens de sesión."""
import hashlib
import hmac
import secrets
from typing import Optional

from .repositories import RepositorioUsuarios


class ServicioAuth:
    ITERACIONES = 100_000

    def __init__(self, usuarios: RepositorioUsuarios) -> None:
        self._usuarios = usuarios
        self._tokens: dict[str, int] = {}  # token -> id de usuario

    @classmethod
    def hash_password(cls, password: str) -> str:
        sal = secrets.token_hex(16)
        h = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(sal), cls.ITERACIONES)
        return f"{sal}${h.hex()}"

    @classmethod
    def verificar_password(cls, password: str, almacenado: str) -> bool:
        sal, esperado = almacenado.split("$")
        h = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(sal), cls.ITERACIONES)
        return hmac.compare_digest(h.hex(), esperado)

    def login(self, email: str, password: str) -> Optional[str]:
        usuario = self._usuarios.buscar_por_email(email)
        if not usuario or not self.verificar_password(password, usuario["password_hash"]):
            return None
        token = secrets.token_urlsafe(32)
        self._tokens[token] = usuario["id"]
        return token

    def usuario_de(self, token: str) -> Optional[dict]:
        id_ = self._tokens.get(token)
        if id_ is None:
            return None
        try:
            return self._usuarios.obtener(id_)
        except Exception:
            self._tokens.pop(token, None)
            return None

    def logout(self, token: str) -> None:
        self._tokens.pop(token, None)

    def cambiar_password(self, usuario: dict, actual: str, nueva: str) -> bool:
        if not self.verificar_password(actual, usuario["password_hash"]):
            return False
        self._usuarios.actualizar(usuario["id"], {"password_hash": self.hash_password(nueva)})
        return True
