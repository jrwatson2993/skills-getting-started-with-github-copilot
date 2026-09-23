from pathlib import Path

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_frontend_refreshes_activity_data_without_cache_staleness():
    app_js = Path("src/static/app.js").read_text()

    assert 'fetch("/activities", { cache: "no-store" }' in app_js
    assert 'cache: "no-store"' in app_js


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_missing_participant_returns_404():
    activity_name = "Gym Class"
    email = "missing.student@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 404
