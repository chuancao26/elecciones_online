from app import schemas
def test_get_elector(create_elector, authorized_admin_client):
    res = authorized_admin_client.get("/elector")
    def validate_data(elector):
        return schemas.PersonaOut(**elector)
    electors = map(validate_data, res.json())
    electors_list = list(electors)
    assert res.status_code == 200
    assert len(electors_list) == 1
    assert electors_list[0].id == 1
    assert electors_list[0].nombres == create_elector['nombres']