from app.models import Candidato

def test_get_candidates(create_candidates, client):
    response = client.get("/candidato/")
    assert response.status_code == 200
    assert len(create_candidates) == len(response.json())

def test_get_a_candidate(create_candidates, client):
    response = client.get(f"/candidato/{create_candidates[0].id}")
    candidate = Candidato(**response.json())
    assert response.status_code == 200
    assert candidate.nombres == create_candidates[0].nombres

def test_delete_candidate(authorized_admin_client, create_candidates):
    candidate_id = create_candidates[0].id
    assert authorized_admin_client.delete(f"/candidato/{candidate_id}").status_code == 204

def test_delete_candidate_eliminated(authorized_admin_client, create_candidates):
    candidate_id = create_candidates[0].id
    authorized_admin_client.delete(f"/candidato/{candidate_id}")
    assert authorized_admin_client.delete(f"/candidato/{candidate_id}").status_code == 404

def test_update_candidate(authorized_admin_client, create_candidates):
    candidate_id = create_candidates[0].id
    updated_data = {
        "nombres": "Carmelo",
        "apellido_paterno": "Rodrigez",
        "apellido_materno": "Malta",
        "id_lista": 1,
    }
    response = authorized_admin_client.put(f"/candidato/{candidate_id}", json=updated_data)
    candidate = Candidato(**response.json())
    
    assert response.status_code == 202
    assert candidate.nombres == updated_data["nombres"]
    assert candidate.apellido_paterno == updated_data["apellido_paterno"]
    assert candidate.apellido_materno == updated_data["apellido_materno"]

def test_update_unauthorized_candidate(client, create_candidates):
    candidate_id = create_candidates[0].id
    unauthorized_data = {
        "nombres": "Carmelo",
        "apellido_paterno": "Rodrigez",
        "apellido_materno": "Malta",
        "id_lista": 1,
    }
    assert client.put(f"/candidato/{candidate_id}", json=unauthorized_data).status_code == 401

def test_missing_candidate(authorized_admin_client):
    non_existent_id = 65656
    missing_data = {
        "nombres": "Carmelo",
        "apellido_paterno": "Rodrigez",
        "apellido_materno": "Malta",
        "id_lista": 1,
    }
    assert authorized_admin_client.put(f"/candidato/{non_existent_id}", json=missing_data).status_code == 404
