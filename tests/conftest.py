from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.config import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import get_db, Base
from app.oauth2 import create_access_token

from app import models

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
@pytest.fixture
def test_elector(client):
    data = {"nombres": "prueba1",
            "apellido_paterno": "prueba2",
            "apellido_materno": "prueba3",
            "usuario": "user1",
            "password": "123"}
    res = client.post("/elector/", json=data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = data["password"]
    return new_user
@pytest.fixture
def test_admin(client):
    data = {"nombres": "admin_1",
            "apellido_paterno": "admin_2",
            "apellido_materno": "admin_3",
            "usuario": "admin1",
            "password": "123"}
    res = client.post("/admin/", json=data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = data["password"]
    return new_user
@pytest.fixture
def authorized_elector_client(client, test_elector):
    token = create_access_token(data={"id": test_elector["id"], "type_user": "elector"})
    client.headers = {
        **client.headers,
        "Authorization" : f"Bearer {token}"
    }
    return client
@pytest.fixture
def authorized_admin_client(client, test_admin):
    token = create_access_token(data={"id": test_admin["id"], "type_user": "admin"})
    print(token)
    client.headers = {
        **client.headers,
        "Authorization" : f"Bearer {token}"
    }
    return client

@pytest.fixture
def create_elections(authorized_admin_client, session):
    data = [{"fecha": "2024-12-01 00:00:00+00",
            "hora_inicio": "08:00:00",
            "hora_fin": "01:00:00",
            "descripcion": "Eleccion de prueba 1"},
            {"fecha": "2024-12-01 00:00:00+00",
             "hora_inicio": "11:00:00",
             "hora_fin": "15:00:00",
             "descripcion": "Eleccion de prueba 2"},
            {"fecha": "2024-12-01 00:00:00+00",
             "hora_inicio": "16:00:00",
             "hora_fin": "19:00:00",
             "descripcion": "Eleccion de prueba 3"},
            {"fecha": "2024-12-01 00:00:00+00",
             "hora_inicio": "08:00:00",
             "hora_fin": "01:00:00",
             "descripcion": "Eleccion de prueba 4"}
            ]
    def make_election(election):
        return models.Eleccion(**election)
    post_election = map(make_election, data)
    elections = list(post_election)
    session.add_all(elections)
    session.commit()
    elections = session.query(models.Eleccion).all()
    return elections

@pytest.fixture
def create_listas(session):
    data = [
        {"nombre": "Lista 1", "id_eleccion": 1, "propuesta": "Propuesta 1"},
        {"nombre": "Lista 2", "id_eleccion": 1, "propuesta": "Propuesta 2"},
        {"nombre": "Lista 1", "id_eleccion": 2, "propuesta": "Propuesta 3"},
        {"nombre": "Lista 2", "id_eleccion": 2, "propuesta": "Propuesta 4"},
        {"nombre": "Lista 1", "id_eleccion": 3, "propuesta": "Propuesta 5"},
        {"nombre": "Lista 2", "id_eleccion": 3, "propuesta": "Propuesta 6"},
        {"nombre": "Lista 1", "id_eleccion": 4, "propuesta": "Propuesta 7"},
        {"nombre": "Lista 1", "id_eleccion": 4, "propuesta": "Propuesta 8"}
    ]
    listas = [models.Lista(**lista) for lista in data]
    session.add_all(listas)
    session.commit()
    listas = session.query(models.Lista).all()
    return listas
