def test_get_all_listas(create_elections, create_listas, authorized_admin_client):
    listas = authorized_admin_client.get('/lista/')
    print(listas.json())
    assert listas.status_code == 200
