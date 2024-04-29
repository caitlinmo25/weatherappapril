import pytest
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index_page(client):
    """Test the index page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Weather App" in response.data

def test_get_weather_valid_location(client):
    """Test the /get_weather route with a valid location."""
    response = client.post('/get_weather', data={'location': 'New York'})
    assert response.status_code == 200
    assert b"Weather for New York" in response.data

def test_get_weather_invalid_location(client):
    """Test the /get_weather route with an invalid location."""
    response = client.post('/get_weather', data={'location': 'Fakeville'})
    assert response.status_code == 200
    # Assuming your application's error handling sends the user back to the index with an error
    assert b"Unable to fetch weather data" in response.data or b"Please provide a location" in response.data

def test_get_weather_no_location(client):
    """Test the /get_weather route with no location provided."""
    response = client.post('/get_weather', data={'location': ''})
    assert response.status_code == 200
    assert b"Please provide a location" in response.data
