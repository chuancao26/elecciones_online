from app import schemas

def test_get_all_listas(create_listas, client):
    listas = client.get('/lista/')
    assert listas.status_code == 200

def test_get_a_list(create_listas, authorized_admin_client, ):
    res = authorized_admin_client.get('/lista/1')
    assert res.status_code == 200

def test_get_nonexistent_list(authorized_admin_client):
    res = authorized_admin_client.get('/lista/2')
    assert res.status_code == 404
    assert res.json() == {"detail": "Lista with id: 2 not found"}
    

def test_create_list_invalid_data(authorized_admin_client):
    data = {"nombre": "", "id_eleccion": 1}  
    res = authorized_admin_client.post('/lista', json=data)
    assert res.status_code == 422  
    
def test_create_list(authorized_admin_client, create_elections):
    data = {"nombre": "Lista 2", "id_eleccion": 1, "propuesta": "Propuesta 2"}
    res = authorized_admin_client.post('/lista', json=data)
    assert res.status_code == 201
    created_list = res.json()
    
    res = authorized_admin_client.get(f'/lista/{created_list["id"]}')
    assert res.status_code == 200
    retrieved_list = res.json()
    assert retrieved_list == created_list

def test_delete_list(authorized_admin_client, create_listas):
    res = authorized_admin_client.delete('/lista/1')
    assert res.status_code == 204  
    
    res = authorized_admin_client.get('/lista/1')
    assert res.status_code == 404


