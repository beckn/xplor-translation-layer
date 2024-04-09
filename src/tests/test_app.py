from fastapi.testclient import TestClient
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)
import sys
sys.path.append('../src/py/.')
from app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_date_check():
    response = client.get("/datecheck")
    assert response.status_code == 200
    assert "date" in response.json()
    # You can further test the format or value of the returned date if needed

def test_translate():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    # Assuming you have the necessary setup for translation and the translate endpoint
    request_data = {
        "text": "Hello",
        "from_ln": "en",
        "to_ln": "fr"
    }
    response = client.post("/translate/", json=request_data)
    assert response.status_code == 200
    assert "translated_text" in response.json()
    # You can further test the translated_text if needed



# 
# pytest -p no:warnings