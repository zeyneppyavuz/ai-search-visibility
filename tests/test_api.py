def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_prompts(client):
    response = client.get("/prompts")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_prompt(client):
    response = client.get("/prompts/t1")
    assert response.status_code == 200
    assert response.json()["text"] == "Best bank for expats?"


def test_get_missing_prompt_returns_404(client):
    response = client.get("/prompts/nope")
    assert response.status_code == 404


def test_create_prompt(client):
    new = {"id": "t3", "text": "Wise fees?", "intent": "informational", "language": "en"}
    response = client.post("/prompts", json=new)
    assert response.status_code == 201
    assert client.get("/prompts/t3").status_code == 200


def test_create_duplicate_returns_409(client):
    dup = {"id": "t1", "text": "Again", "intent": "commercial", "language": "en"}
    response = client.post("/prompts", json=dup)
    assert response.status_code == 409


def test_create_invalid_intent_returns_422(client):
    bad = {"id": "t4", "text": "Hi", "intent": "shopping", "language": "en"}
    response = client.post("/prompts", json=bad)
    assert response.status_code == 422


def test_delete_prompt(client):
    response = client.delete("/prompts/t1")
    assert response.status_code == 204
    assert client.get("/prompts/t1").status_code == 404


def test_brands_returns_10(client):
    response = client.get("/brands")
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_n26_aliases(client):
    brands = client.get("/brands").json()
    n26 = [b for b in brands if b["id"] == "n26"][0]
    assert "N26 Bank" in n26["aliases"]