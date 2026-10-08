from fastapi.testclient import TestClient
from backend.api import app

client = TestClient(app)


def test_health_endpoint():
    """Verifies the /health readiness endpoint returns HTTP 200 and service metadata."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["capability"] == "image_generation"
    assert data["model"] == "cyberrealistic"


def test_missing_prompt_validation():
    """Step 7 requirement: Missing prompt must return a useful HTTP 422 error."""
    response = client.post(
        "/capabilities/image/generate",
        json={"width": 512, "height": 512, "steps": 5}
    )
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "validation_error"
    assert any("prompt" in err["field"] for err in data["details"])


def test_invalid_dimensions_validation():
    """Step 7 requirement: Dimensions not divisible by 64 or out of range must fail cleanly."""
    response = client.post(
        "/capabilities/image/generate",
        json={
            "prompt": "Cinematic wide shot of a train station",
            "width": 500,
            "height": 512,
            "steps": 5
        }
    )
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "validation_error"
    assert any("width" in err["field"] for err in data["details"])


def test_invalid_numeric_settings_validation():
    """Step 7 requirement: Negative steps or out-of-bounds guidance_scale must fail cleanly."""
    response = client.post(
        "/capabilities/image/generate",
        json={
            "prompt": "Cinematic wide shot of a train station",
            "width": 512,
            "height": 512,
            "steps": -5,
            "guidance_scale": 50.0
        }
    )
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "validation_error"