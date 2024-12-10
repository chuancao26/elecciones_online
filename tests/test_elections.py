from app.models import Eleccion

def test_get_elections(create_elecciones, client):
    response = client.get("/eleccion/")
    assert response.status_code == 200
    assert len(create_elecciones) == len(response.json())

def test_get_an_election(create_elecciones, client):
    response = client.get(f"/eleccion/{create_elecciones[0].id}")
    eleccion = Eleccion(**response.json())
    assert response.status_code == 200
    assert eleccion.descripcion == create_elecciones[0].descripcion

def test_delete_election(authorized_admin_client, create_elecciones):
    eleccion_id = create_elecciones[0].id
    assert authorized_admin_client.delete(f"/eleccion/{eleccion_id}").status_code == 204

def test_delete_election_already_deleted(authorized_admin_client, create_elecciones):
    eleccion_id = create_elecciones[0].id
    authorized_admin_client.delete(f"/eleccion/{eleccion_id}")
    assert authorized_admin_client.delete(f"/eleccion/{eleccion_id}").status_code == 404

def test_update_election(authorized_admin_client, create_elecciones):
    eleccion_id = create_elecciones[0].id
    updated_data = {
        "fecha": "2024-12-20",
        "hora_inicio": "08:00:00",
        "hora_fin": "17:00:00",
        "descripcion": "Elección presidencial actualizada",
    }
    response = authorized_admin_client.put(f"/eleccion/{eleccion_id}", json=updated_data)
    eleccion = Eleccion(**response.json())
    
    assert response.status_code == 202
    assert eleccion.descripcion == updated_data["descripcion"]
    assert str(eleccion.fecha) == updated_data["fecha"]
    assert str(eleccion.hora_inicio) == updated_data["hora_inicio"]
    assert str(eleccion.hora_fin) == updated_data["hora_fin"]

def test_update_unauthorized_election(client, create_elecciones):
    eleccion_id = create_elecciones[0].id
    unauthorized_data = {
        "fecha": "2024-12-20",
        "hora_inicio": "08:00:00",
        "hora_fin": "17:00:00",
        "descripcion": "Intento de actualización no autorizado",
    }
    assert client.put(f"/eleccion/{eleccion_id}", json=unauthorized_data).status_code == 401

def test_missing_election(authorized_admin_client):
    non_existent_id = 99999
    missing_data = {
        "fecha": "2024-12-20",
        "hora_inicio": "08:00:00",
        "hora_fin": "17:00:00",
        "descripcion": "Intento de actualizar elección inexistente",
    }
    assert authorized_admin_client.put(f"/eleccion/{non_existent_id}", json=missing_data).status_code == 404
