from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest

# Adjust import based on project structure
from app.database import Base
from main import app, get_db
from app import models

# Setup in-memory DB for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
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

def test_auth_flow():
    # 1. Register User
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "securepassword123",
        "fullName": "Test User"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data

    # 2. Verify Password is Hashed in DB
    db = TestingSessionLocal()
    db_user = db.query(models.User).filter(models.User.email == "test@example.com").first()
    assert db_user is not None
    assert db_user.hashed_password != "securepassword123"
    assert db_user.hashed_password.startswith("$2") # bcrypt prefix
    db.close()

    # 3. Login Success
    login_data = {
        "username": "testuser",
        "password": "securepassword123"
    }
    response = client.post("/token", data=login_data)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    # 4. Login Fails - Wrong Password
    login_data_wrong = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    response = client.post("/token", data=login_data_wrong)
    assert response.status_code == 401

    # 5. Login Fails - Wrong Username
    login_data_wrong_user = {
        "username": "wronguser",
        "password": "securepassword123"
    }
    response = client.post("/token", data=login_data_wrong_user)
    assert response.status_code == 401
