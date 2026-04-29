from fastapi.testclient import TestClient

from app_builder_ai.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generate_project_endpoint() -> None:
    response = client.post(
        "/api/projects/generate",
        json={
            "prompt": "Create an AI project builder with schema validation and a review workflow.",
            "target_stack": "react-fastapi",
            "include_tests": True,
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["blueprint"]["core_features"]
    assert body["files"]
    assert body["workflow_trace"]


def test_project_manifest_endpoint() -> None:
    created = client.post(
        "/api/projects/generate",
        json={
            "prompt": "Create an AI project builder with schema validation and manifest downloads.",
            "target_stack": "react-fastapi",
        },
    ).json()

    response = client.get(f"/api/projects/{created['id']}/manifest")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]
