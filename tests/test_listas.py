from app import schemas

def test_get_all_listas(create_listas, client):
    listas = client.get('/lista/')
    assert listas.status_code == 200
def test_get_a_list(create_listas, authorized_admin_client, ):
    res = authorized_admin_client.get('/lista/1')
    assert res.status_code == 200
def test_create_list(authorized_admin_client, create_elections):
    data ={"nombre": "Lista 1",
           "id_eleccion": 1,
           "propuesta": "Propuesta 1"}
    res = authorized_admin_client.post('/lista', json=data)
    respuesta = res.json()
    print(type(respuesta))
    print("prueba")
    lista_creada = schemas.ListaOut(**respuesta)
    assert lista_creada.id == 1
    assert res.status_code == 201


