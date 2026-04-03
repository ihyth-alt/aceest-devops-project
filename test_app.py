import pytest
from app import app, PROGRAMS


# ── Fixture ───────────────────────────────────────────────────────────────────

@pytest.fixture
def client():
    """Create a Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ── Home route ────────────────────────────────────────────────────────────────

def test_home_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_home_returns_json(client):
    response = client.get("/")
    data = response.get_json()
    assert data is not None


def test_home_message(client):
    response = client.get("/")
    data = response.get_json()
    assert "ACEest" in data["message"]


def test_home_status_running(client):
    response = client.get("/")
    data = response.get_json()
    assert data["status"] == "running"


# ── /programs route ───────────────────────────────────────────────────────────

def test_get_programs_returns_200(client):
    response = client.get("/programs")
    assert response.status_code == 200


def test_get_programs_contains_fat_loss(client):
    response = client.get("/programs")
    data = response.get_json()
    assert "Fat Loss (FL)" in data["programs"]


def test_get_programs_contains_muscle_gain(client):
    response = client.get("/programs")
    data = response.get_json()
    assert "Muscle Gain (MG)" in data["programs"]


def test_get_programs_contains_beginner(client):
    response = client.get("/programs")
    data = response.get_json()
    assert "Beginner (BG)" in data["programs"]


def test_get_programs_returns_three_programs(client):
    response = client.get("/programs")
    data = response.get_json()
    assert len(data["programs"]) == 3


# ── /programs/<name> route ────────────────────────────────────────────────────

def test_program_detail_fat_loss(client):
    response = client.get("/programs/Fat Loss (FL)")
    assert response.status_code == 200


def test_program_detail_has_workout(client):
    response = client.get("/programs/Fat Loss (FL)")
    data = response.get_json()
    assert "workout" in data["details"]


def test_program_detail_has_diet(client):
    response = client.get("/programs/Fat Loss (FL)")
    data = response.get_json()
    assert "diet" in data["details"]


def test_program_detail_invalid_returns_404(client):
    response = client.get("/programs/InvalidProgram")
    assert response.status_code == 404


# ── /calculate route ──────────────────────────────────────────────────────────

def test_calculate_fat_loss(client):
    payload = {"program": "Fat Loss (FL)", "weight": 70}
    response = client.post("/calculate", json=payload)
    assert response.status_code == 200


def test_calculate_fat_loss_correct_value(client):
    payload = {"program": "Fat Loss (FL)", "weight": 70}
    response = client.post("/calculate", json=payload)
    data = response.get_json()
    assert data["estimated_calories"] == 70 * 22  # 1540


def test_calculate_muscle_gain_correct_value(client):
    payload = {"program": "Muscle Gain (MG)", "weight": 80}
    response = client.post("/calculate", json=payload)
    data = response.get_json()
    assert data["estimated_calories"] == 80 * 35  # 2800


def test_calculate_beginner_correct_value(client):
    payload = {"program": "Beginner (BG)", "weight": 60}
    response = client.post("/calculate", json=payload)
    data = response.get_json()
    assert data["estimated_calories"] == 60 * 26  # 1560


def test_calculate_returns_program_name(client):
    payload = {"program": "Fat Loss (FL)", "weight": 70}
    response = client.post("/calculate", json=payload)
    data = response.get_json()
    assert data["program"] == "Fat Loss (FL)"


def test_calculate_missing_program_returns_400(client):
    payload = {"weight": 70}
    response = client.post("/calculate", json=payload)
    assert response.status_code == 400


def test_calculate_missing_weight_returns_400(client):
    payload = {"program": "Fat Loss (FL)"}
    response = client.post("/calculate", json=payload)
    assert response.status_code == 400


def test_calculate_invalid_program_returns_400(client):
    payload = {"program": "NonExistent", "weight": 70}
    response = client.post("/calculate", json=payload)
    assert response.status_code == 400


def test_calculate_zero_weight_returns_400(client):
    payload = {"program": "Fat Loss (FL)", "weight": 0}
    response = client.post("/calculate", json=payload)
    assert response.status_code == 400


def test_calculate_negative_weight_returns_400(client):
    payload = {"program": "Fat Loss (FL)", "weight": -10}
    response = client.post("/calculate", json=payload)
    assert response.status_code == 400


def test_calculate_no_body_returns_400(client):
    response = client.post("/calculate")
    assert response.status_code in (400, 415)


# ── /clients route ────────────────────────────────────────────────────────────

def test_add_client_returns_201(client):
    payload = {"name": "Arjun", "age": 25, "weight": 72, "program": "Fat Loss (FL)"}
    response = client.post("/clients", json=payload)
    assert response.status_code == 201


def test_add_client_name_in_response(client):
    payload = {"name": "Priya", "age": 22, "weight": 55, "program": "Beginner (BG)"}
    response = client.post("/clients", json=payload)
    data = response.get_json()
    assert data["client"]["name"] == "Priya"


def test_add_client_calories_calculated(client):
    payload = {"name": "Karthik", "age": 30, "weight": 85, "program": "Muscle Gain (MG)"}
    response = client.post("/clients", json=payload)
    data = response.get_json()
    assert data["client"]["estimated_calories"] == 85 * 35  # 2975


def test_add_client_missing_name_returns_400(client):
    payload = {"age": 25, "weight": 72, "program": "Fat Loss (FL)"}
    response = client.post("/clients", json=payload)
    assert response.status_code == 400


def test_add_client_missing_program_returns_400(client):
    payload = {"name": "Test", "age": 25, "weight": 72}
    response = client.post("/clients", json=payload)
    assert response.status_code == 400


def test_add_client_invalid_program_returns_400(client):
    payload = {"name": "Test", "age": 25, "weight": 72, "program": "Wrong"}
    response = client.post("/clients", json=payload)
    assert response.status_code == 400


# ── PROGRAMS data integrity ───────────────────────────────────────────────────

def test_programs_data_fat_loss_factor():
    assert PROGRAMS["Fat Loss (FL)"]["calorie_factor"] == 22


def test_programs_data_muscle_gain_factor():
    assert PROGRAMS["Muscle Gain (MG)"]["calorie_factor"] == 35


def test_programs_data_beginner_factor():
    assert PROGRAMS["Beginner (BG)"]["calorie_factor"] == 26


def test_all_programs_have_workout_key():
    for name, data in PROGRAMS.items():
        assert "workout" in data, f"Missing workout in {name}"


def test_all_programs_have_diet_key():
    for name, data in PROGRAMS.items():
        assert "diet" in data, f"Missing diet in {name}"
