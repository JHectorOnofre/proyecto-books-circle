from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest
from app.database import Base
from main import app, get_db
from app import models, schemas
from app.core import security

# Setup in-memory DB
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_protected_routes():
    # 1. Setup Data: Register and Login to get Token
    user_data = {"email": "secure@example.com", "username": "secureuser", "password": "password", "fullName": "Secure User"}
    client.post("/auth/register", json=user_data)
    
    login_res = client.post("/token", data={"username": "secureuser", "password": "password"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Test Protected Route WITHOUT Token (Should Fail)
    res_no_token = client.get("/clubs")
    assert res_no_token.status_code == 401
    assert res_no_token.json()["detail"] == "Not authenticated"

    # 3. Test Protected Route WITH Token (Should Succeed - initially empty list)
    res_with_token = client.get("/clubs", headers=headers)
    assert res_with_token.status_code == 200
    assert res_with_token.json() == []

    # 4. Create Club (Protected)
    club_data = {"name": "Test Club", "description": "desc"}
    res_create = client.post("/clubs", json=club_data, headers=headers)
    assert res_create.status_code == 201
    
    # 5. Verify Club Created
    res_list = client.get("/clubs", headers=headers)
    assert len(res_list.json()) == 1
