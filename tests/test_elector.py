from app import schemas

def validate_data(elector):
    return schemas.PersonaOut(**elector)

def test_get_elector(create_elector, authorized_admin_client):
    res = authorized_admin_client.get("/elector")
    electors = map(validate_data, res.json())
    electors_list = list(electors)
    assert res.status_code == 200
    assert len(electors_list) == 1
    assert electors_list[0].id == 1
    assert electors_list[0].nombres == create_elector['nombres']

def test_get_group_electors(create_group_electors, authorized_admin_client):
    res = authorized_admin_client.get("/elector")
    electors = map(validate_data, res.json())
    electors_list = list(electors)
    assert res.status_code == 200
    for number, elector in enumerate(electors_list):
        assert elector.id == create_group_electors[number]['id']
        assert elector.nombres == create_group_electors[number]['nombres']

def test_update_elector(authorized_elector_client):
    new_data = {
        "nombres": "NewName",
        "apellido_paterno": "NewFirstName",
        "apellido_materno": "NewSecondName",
    }
    res = authorized_elector_client.put('/elector', json=new_data)
    response_persona = schemas.PersonaOut(**res.json())
    assert res.status_code == 200
    assert response_persona.nombres == new_data['nombres']
    assert response_persona.apellido_paterno == new_data['apellido_paterno']
    assert response_persona.apellido_materno == new_data['apellido_materno']
#def test_update_elector(create_elector, client):
#    data = {
#        "username": create_elector['usuario'],
#        "password": create_elector['password']
#    }
#    res = client.post("/login", data=data)
#    token = schemas.TokenCreated(**res.json())
#    client.headers = {
#        **client.headers,
#        "Authorization": f"Bearer {token.access_token}"
#    }
#    new_data = {
#           "nombres": "New Name",
#           "apellido_paterno": "New First Name",
#           "apellido_materno": "New Second Name",
#       }
#    res = client.put('/elector', json=new_data)
#    response_persona = schemas.PersonaOut(**res.json())
#    assert res.status_code == 200
#    assert response_persona.nombres == new_data['nombres']
#    assert response_persona.apellido_paterno == new_data['apellido_paterno']
#    assert response_persona.apellido_materno == new_data['apellido_materno']
