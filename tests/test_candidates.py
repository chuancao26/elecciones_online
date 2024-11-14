from app.models import Candidato
def test_get_candidates(create_candidates, client):
    res = client.get("/candidato/")
    assert res.status_code == 200
    assert len(create_candidates) == len(res.json())

def test_get_a_candidate(create_candidates, client):
    res = client.get(f"/candidato/{create_candidates[0].id}")
    candidate = Candidato(**res.json())
    assert res.status_code == 200
    assert candidate.nombres == create_candidates[0].nombres

def test_delete_candidate(authorized_admin_client, create_candidates):
    res = authorized_admin_client.delete(f"/candidato/{create_candidates[0].id}")
    assert res.status_code == 204

def test_delete_candidate_eliminated(authorized_admin_client, create_candidates):
    res = authorized_admin_client.delete(f"/candidato/{create_candidates[0].id}")
    res = authorized_admin_client.delete(f"/candidato/{create_candidates[0].id}")
    assert res.status_code == 404

def test_update_candidate(authorized_admin_client, create_candidates):
    data = {"nombres": "Carmelo",
            "apellido_paterno": "Rodrigez",
            "apellido_materno": "Malta",
            "id_lista": 1}
    res = authorized_admin_client.put(f"/candidato/{create_candidates[0].id}",json=data)
    assert res.status_code == 202
def test_update_unauthorized_candidate(client, create_candidates):
    data = {"nombres": "Carmelo",
            "apellido_paterno": "Rodrigez",
            "apellido_materno": "Malta",
            "id_lista": 1}
    res = client.put(f"/candidato/{create_candidates[0].id}",json=data)
    assert res.status_code == 401

def test_update_unauthorized_candidate(authorized_admin_client, create_candidates):
    data = {"nombres": "Carmelo",
            "apellido_paterno": "Rodrigez",
            "apellido_materno": "Malta",
            "id_lista": 1}
    res = authorized_admin_client.put(f"/candidato/{65656}",json=data)
    assert res.status_code == 404
