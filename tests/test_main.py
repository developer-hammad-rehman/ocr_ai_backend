from http.client import responses
from fastapi.testclient import TestClient
from app.main import app
from sqlmodel import Session, create_engine
from app.main import app
from app.settings import TEST_DATA_BASE_URL
from app.crud import get_session

connection_string =  str(TEST_DATA_BASE_URL)

engine = create_engine(connection_string)

def get_test_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = get_test_session

client = TestClient(app=app)

def test_root_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to ocr app server"}


def register_route():
    data = {"username": "test@ai.com", "password": "test"}
    response = client.post("/register", data=data)
    assert response.status_code == 200 

def test_auth_route():
    responses = client.post("/auth" , data={"username": "demo@ai.com", "password": "demo"})
    assert responses.status_code == 200
    assert responses.json()["token_type"] == "bearer"