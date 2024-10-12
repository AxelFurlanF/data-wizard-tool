from fastapi.testclient import TestClient
from app.main import create_app  # Import your FastAPI app

app = create_app()
client = TestClient(app)


def test_upload_gcp_credentials():
    with open("data-wizard-tool-sa.json", "rb") as cred_file:
        response = client.post("/auth/gcp_credentials", files={"credentials_file": cred_file})
    assert response.status_code == 200
    assert response.json() == {"message": "GCP credentials uploaded successfully!"}
