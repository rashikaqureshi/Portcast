from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}


def test_fetch():
    mock_response = Mock()
    mock_response.text = "This is a test paragraph."
    mock_response.status_code = 200

    with patch("app.services.requests.get", return_value=mock_response):
        response = client.get("/fetch")

    assert response.status_code == 200
    data = response.json()
    assert "content" in data


def test_search_or():
    mock_response = Mock()
    mock_response.text = "cloud sky blue"
    mock_response.status_code = 200

    with patch("app.services.requests.get", return_value=mock_response):
        client.get("/fetch")  

    response = client.get("/search?words=cloud,sky&operator=or")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_dictionary():
    mock_fetch = Mock()
    mock_fetch.text = "cloud sky blue"
    mock_fetch.status_code = 200

    mock_dict = Mock()
    mock_dict.status_code = 200
    mock_dict.json.return_value = [
        {
            "meanings": [
                {
                    "definitions": [
                        {"definition": "mock definition"}
                    ]
                }
            ]
        }
    ]

    def mock_requests_get(url):
        if "metaphorpsum" in url:
            return mock_fetch
        else:
            return mock_dict

    with patch("app.services.requests.get", side_effect=mock_requests_get):
        client.get("/fetch")
        response = client.get("/dictionary")

    assert response.status_code == 200
    assert isinstance(response.json(), list)