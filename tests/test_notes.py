def _register_login(client, email="u@test.com"):
    client.post("/auth/register", json={"email": email, "password": "password123"})
    r = client.post("/auth/login", json={"email": email, "password": "password123"})
    token = r.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_notes_crud_ownership(client):
    h1 = _register_login(client, "user1@test.com")
    h2 = _register_login(client, "user2@test.com")

    # user1 creates
    r = client.post("/notes", headers=h1, json={"title": "t1", "content": "c1"})
    assert r.status_code == 201
    note_id = r.get_json()["id"]

    # user1 can read
    r = client.get(f"/notes/{note_id}", headers=h1)
    assert r.status_code == 200

    # user2 cannot read (ownership enforced)
    r = client.get(f"/notes/{note_id}", headers=h2)
    assert r.status_code == 404

    # update
    r = client.put(f"/notes/{note_id}", headers=h1, json={"title": "t1-updated"})
    assert r.status_code == 200
    assert r.get_json()["title"] == "t1-updated"

    # delete
    r = client.delete(f"/notes/{note_id}", headers=h1)
    assert r.status_code == 200
