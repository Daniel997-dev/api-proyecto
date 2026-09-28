import pytest
from fastapi.testclient import TestClient

from app.main import crear_app


@pytest.fixture()
def client():
    return TestClient(crear_app())


@pytest.fixture()
def auth(client):
    r = client.post("/auth/login", json={"email": "admin@example.com", "password": "Admin12345"})
    assert r.status_code == 200
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


# auth
def test_auth_flujo_completo(client, auth):
    assert client.get("/auth/me", headers=auth).json()["email"] == "admin@example.com"
    assert client.put("/auth/password", headers=auth, json={"actual": "mala", "nueva": "Nueva12345"}).status_code == 400
    assert client.put("/auth/password", headers=auth, json={"actual": "Admin12345", "nueva": "Nueva12345"}).status_code == 204
    assert client.post("/auth/login", json={"email": "admin@example.com", "password": "Admin12345"}).status_code == 401
    assert client.delete("/auth/logout", headers=auth).status_code == 204
    assert client.get("/auth/me", headers=auth).status_code == 401


def test_login_incorrecto_y_sin_token(client):
    assert client.post("/auth/login", json={"email": "admin@example.com", "password": "x"}).status_code == 401
    assert client.get("/usuarios").status_code == 401


# usuarios
def test_usuarios_crud_y_reglas(client, auth):
    nuevo = {"nombre": "Ana Ruiz", "email": "ana@correo.com", "rol": "usuario", "password": "Clave12345"}
    r = client.post("/usuarios", headers=auth, json=nuevo)
    assert r.status_code == 201 and "password" not in r.json() and "password_hash" not in r.json()
    uid = r.json()["id"]
    assert client.post("/usuarios", headers=auth, json=nuevo).status_code == 409
    assert client.get(f"/usuarios/{uid}", headers=auth).status_code == 200
    assert client.put(f"/usuarios/{uid}", headers=auth, json={"nombre": "Ana R.", "email": "ana@correo.com", "rol": "usuario"}).json()["nombre"] == "Ana R."
    # un usuario normal puede consultar pero no crear
    tok = client.post("/auth/login", json={"email": "ana@correo.com", "password": "Clave12345"}).json()["access_token"]
    normal = {"Authorization": f"Bearer {tok}"}
    assert client.get("/usuarios", headers=normal).status_code == 200
    assert client.post("/usuarios", headers=normal, json={**nuevo, "email": "b@c.com"}).status_code == 403
    assert client.delete(f"/usuarios/{uid}", headers=auth).status_code == 204
    assert client.get(f"/usuarios/{uid}", headers=auth).status_code == 404


# servicios
def test_servicios_crud(client):
    r = client.post("/servicios", json={"nombre": "Instalación", "descripcion": "En sitio", "precio": 90000})
    assert r.status_code == 201
    sid = r.json()["id"]
    assert client.get("/servicios").status_code == 200
    assert client.get(f"/servicios/{sid}").json()["activo"] is True
    assert client.put(f"/servicios/{sid}", json={"nombre": "Instalación pro", "precio": 120000, "activo": False}).json()["activo"] is False
    assert client.delete(f"/servicios/{sid}").status_code == 204
    assert client.get(f"/servicios/{sid}").status_code == 404


# productos
def test_productos_crud(client):
    assert client.post("/productos", json={"id": 7, "nombre": "Mouse", "precio": 30000}).status_code == 201
    assert client.post("/productos", json={"id": 7, "nombre": "Otro", "precio": 1}).status_code == 409
    assert client.post("/productos", json={"nombre": "Sin id", "precio": 5}).json()["id"] > 0
    assert client.get("/productos/7").json()["nombre"] == "Mouse"
    assert client.put("/productos/7", json={"id": 7, "nombre": "Mouse X", "precio": 35000}).json()["precio"] == 35000
    assert client.delete("/productos/7").status_code == 204
    assert client.get("/productos/7").status_code == 404
    assert client.post("/productos", json={"nombre": "x", "precio": -1}).status_code == 422
