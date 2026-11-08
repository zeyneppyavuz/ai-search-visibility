from fastapi.testclient import TestClient

from minipeec.api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_prompts_returns_15():
    response = client.get("/prompts")
    assert response.status_code == 200
    assert len(response.json()) == 15


def test_prompt_has_valid_intent():
    prompts = client.get("/prompts").json()
    for p in prompts:
        assert p["intent"] in ["commercial", "comparison", "informational"]


def test_brands_returns_10():
    response = client.get("/brands")
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_n26_aliases():
    brands = client.get("/brands").json()
    n26 = [b for b in brands if b["id"] == "n26"][0]
    assert "N26 Bank" in n26["aliases"]