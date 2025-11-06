import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.models import Base
from sqlalchemy import StaticPool
TEST_DB_URL = "sqlite+pysqlite:///:memory:"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool,)
TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
Base.metadata.create_all(bind=engine)

@pytest.fixture
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        # hand the client to the test
        yield c
        # --- teardown happens when the 'with' block exits ---


def test_create_user(client):
    r = client.post("/api/users", json={"name":"Paul","email":"pl@atu.ie","age":25,"student_id":"S1234567"})
    assert r.status_code == 201

#Test update user with a non-existant id. 404 expected
def test_put_user(client):
    r = client.put("/api/users/10", json={"id": 10, "name":"Paul","email":"pl@atu.ie","age":25,"student_id":"S1234567"})
    assert r.status_code == 404

#Test update user with an existant id. 200 expected
def test_put_user(client):
    r = client.put("/api/users/1", json={"id": 1, "name":"Pero","email":"pl@atu.ie","age":25,"student_id":"S1234567"})
    assert r.status_code == 200

#Test patch with an existant id. 200 expected
def test_patch_user(client):
    r = client.patch("/api/users/1", json={"id": 1, "name":"Paul","email":"pl@atu.ie","age":25})
    assert r.status_code == 200

#Test update user with an existant id. 200 expected
def test_put_project_pass(client):
    client.post("/api/users", json={"name":"Paul","email":"joe@atu.ie","age":25,"student_id":"S1234564"})
    client.post("/api/users/1/projects", json={"name":"Project1"})
    r = client.put("/api/users/project_put/1", json={"id":1,"name":"ProjectDiff","owner_id":1})
    assert r.status_code == 200

#Test patch with an existant id. 200 expected
def test_patch_project_pass(client):
    client.post("/api/users", json={"name":"Paul","email":"jim@atu.ie","age":25,"student_id":"S1234563"})
    client.post("/api/users/1/projects", json={"name":"Project2"})
    r = client.patch("/api/users/project_patch/1", json={"name":"ProjectDiff"})
    assert r.status_code == 200