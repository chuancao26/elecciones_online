def test_get_elections(client, create_elections):
    res = client.get("/eleccion/")
    print(res.json())
    assert res.status_code == 200
def test_get_a_election(authorized_admin_client, create_elections):
    res = authorized_admin_client.get(f"/eleccion/{create_elections[0].id}")
    election = res.json()
    assert res.status_code == 200
    assert election['id'] == create_elections[0].id