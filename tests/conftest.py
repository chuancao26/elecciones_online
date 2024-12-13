import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

from app import models
from app.main import app
from app.config import settings


from app.database import get_db, Base
from app.oauth2 import create_access_token
from app.config import settings

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

@pytest.fixture()
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(10)

    yield driver
    driver.quit()

@pytest.fixture
def test_elector(client):
    data = {"nombres": "prueba1",
            "apellido_paterno": "prueba2",
            "apellido_materno": "prueba3",
            "usuario": "user1",
            "password": settings.general_password}
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
            "password": settings.general_password}
    res = client.post("/admin/", json=data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = data["password"]
    return new_user

@pytest.fixture
def token_elector(test_elector):
    return create_access_token(data={"id": test_elector["id"], "type_user": "elector"})

@pytest.fixture
def token_admin(test_admin):
    return create_access_token(data={"id": test_admin["id"], "type_user": "admin"})

@pytest.fixture
def authorized_elector_client(client, token_elector):
    client.headers = {
        **client.headers,
        "Authorization" : f"Bearer {token_elector}"
    }
    return client

@pytest.fixture
def authorized_admin_client(client, token_admin):
    client.headers = {
        **client.headers,
        "Authorization" : f"Bearer {token_admin}"
    }
    return client

@pytest.fixture
def create_elections(session):
    data = [{"fecha": "2024-12-01 00:00:00+00",
            "hora_inicio": "08:00:00",
            "hora_fin": "01:00:00",
            "descripcion": "Eleccion de prueba 1"},
            {"fecha": "2024-11-01 00:00:00+00",
             "hora_inicio": "11:00:00",
             "hora_fin": "15:00:00",
             "descripcion": "Eleccion de prueba 2"},
            {"fecha": "2024-10-01 00:00:00+00",
             "hora_inicio": "16:00:00",
             "hora_fin": "19:00:00",
             "descripcion": "Eleccion de prueba 3"},
            {"fecha": "2024-09-01 00:00:00+00",
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
def create_listas(create_elections, session):
    nombre1 = "Lista 1"
    nombre2 = "Lista 2"
    data = [
        {"nombre": nombre1, "id_eleccion": 1, "propuesta": "Propuesta 1"},
        {"nombre": nombre2, "id_eleccion": 1, "propuesta": "Propuesta 2"},
        {"nombre": nombre1, "id_eleccion": 2, "propuesta": "Propuesta 3"},
        {"nombre": nombre2, "id_eleccion": 2, "propuesta": "Propuesta 4"},
        {"nombre": nombre1, "id_eleccion": 3, "propuesta": "Propuesta 5"},
        {"nombre": nombre2, "id_eleccion": 3, "propuesta": "Propuesta 6"},
        {"nombre": nombre1, "id_eleccion": 4, "propuesta": "Propuesta 7"},
        {"nombre": nombre2, "id_eleccion": 4, "propuesta": "Propuesta 8"}
    ]
    def make_list(list):
        return models.Lista(**list)
    list_lists = map(make_list, data)
    session.add_all(list_lists)
    session.commit()
    listas = session.query(models.Lista).all()
    return listas

@pytest.fixture
def create_candidates(session, create_listas):
    data = [
        {"nombres": "Juan", "apellido_paterno": "Rodrigez","apellido_materno": "Malta", "id_lista": 1},
        {"nombres": "Julian", "apellido_paterno": "Pedro", "apellido_materno": "Duque", "id_lista": 1},
        {"nombres": "Pedro", "apellido_paterno": "Arauco", "apellido_materno": "Espinoza", "id_lista": 1},
        {"nombres": "Jerke", "apellido_paterno": "Brion", "apellido_materno": "Miraflores", "id_lista": 1},
        {"nombres": "Cristhian", "apellido_paterno": "Siene", "apellido_materno": "Gregorio", "id_lista": 1},
    ]
    def make_candidate(candidate):
        return models.Candidato(**candidate)
    candidates_list = map(make_candidate, data)
    session.add_all(candidates_list)
    session.commit()
    return session.query(models.Candidato).all()
@pytest.fixture
def create_elector(client):
    data = {
        "nombres": "Juan Carlos",
        "apellido_paterno": "Gómez",
        "apellido_materno": "Martínez",
        "usuario": "elector1",
        "password": settings.general_password
    }
    res = client.post("/elector", json=data)
    assert res.status_code == 201
    new_elector = res.json()
    new_elector["usuario"] = data['usuario']
    new_elector["password"] = data["password"]
    return new_elector
@pytest.fixture
def create_group_electors(client):
    list_electors = [
        {
            "nombres": "Juan Carlos",
            "apellido_paterno": "Gómez",
            "apellido_materno": "Martínez",
            "usuario": "elector2",
            "password": settings.general_password
        },
        {
            "nombres": "Juan Carlos",
            "apellido_paterno": "Gómez",
            "apellido_materno": "Martínez",
            "usuario": "elector3",
            "password": settings.general_password
        },
        {
            "nombres": "Juan Carlos",
            "apellido_paterno": "Gómez",
            "apellido_materno": "Martínez",
            "usuario": "elector4",
            "password": settings.general_password
        },
        {
            "nombres": "Juan Carlos",
            "apellido_paterno": "Gómez",
            "apellido_materno": "Martínez",
            "usuario": "elector5",
            "password": settings.general_password
        },
        {
            "nombres": "Juan Carlos",
            "apellido_paterno": "Gómez",
            "apellido_materno": "Martínez",
            "usuario": "elector6",
            "password": settings.general_password
        },
    ]
    electors_info = []
    for data in list_electors:
        res = client.post("/elector", json=data)
        assert res.status_code == 201
        new_elector = res.json()
        new_elector["password"] = data["password"]
        electors_info.append(new_elector)
    return electors_info