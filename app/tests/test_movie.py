from fastapi.testclient import TestClient
from app.main import app


Client = TestClient(app)

def test_root():
    res = Client.get("/")
    # print(res.json().get('message'))
    assert res.json().get('message') == "This is Torah's application"
    assert res.status_code == 200
