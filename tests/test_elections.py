def test_get_elections(client):
    res = client.get("/eleccion/")
    print(res.json())
    assert res.status_code == 200

