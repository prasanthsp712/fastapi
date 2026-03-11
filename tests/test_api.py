from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

# ----------------------
# HEALTH CHECK
# ----------------------
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

# ----------------------
# GET ALL ITEMS
# ----------------------
def test_get_items():
    response = client.get("/api/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ----------------------
# GET ITEM SUCCESS
# ----------------------
def test_get_single_item():
    response = client.get("/api/items/1")
    if response.status_code == 200:
        assert "id" in response.json()
    else:
        # If DB is empty, ensure correct error
        assert response.status_code in [200, 404]

# ----------------------
# GET ITEM NOT FOUND
# ----------------------
def test_get_item_not_found():
    response = client.get("/api/items/9999")
    assert response.status_code == 404