import pytest


def station_payload(
    code="ST-01",
    name="Centre",
    capacity=10,
    status="open",
):
    return {
        "code": code,
        "name": name,
        "capacity": capacity,
        "status": status,
    }


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_then_get_by_id(client):
    payload = station_payload()

    create_response = client.post(
        "/stations",
        json=payload,
    )

    assert create_response.status_code == 201

    created = create_response.json()

    assert "id" in created
    assert created["code"] == payload["code"]
    assert created["name"] == payload["name"]
    assert created["capacity"] == payload["capacity"]
    assert created["status"] == payload["status"]

    station_id = created["id"]

    get_response = client.get(
        f"/stations/{station_id}"
    )

    assert get_response.status_code == 200

    station = get_response.json()

    assert station["id"] == station_id
    assert station["code"] == payload["code"]
    assert station["name"] == payload["name"]
    assert station["capacity"] == payload["capacity"]
    assert station["status"] == payload["status"]


def test_filter_status_open(client):
    client.post(
        "/stations",
        json=station_payload(
            code="ST-OPEN",
            name="Station ouverte",
            status="open",
        ),
    )

    client.post(
        "/stations",
        json=station_payload(
            code="ST-CLOSED",
            name="Station fermée",
            status="closed",
        ),
    )

    response = client.get(
        "/stations",
        params={"status": "open"},
    )

    assert response.status_code == 200

    stations = response.json()

    assert len(stations) == 1
    assert stations[0]["code"] == "ST-OPEN"
    assert stations[0]["status"] == "open"

    assert all(
        station["status"] == "open"
        for station in stations
    )


def test_patch_name_only(client):
    payload = station_payload(
        code="ST-PATCH",
        name="Ancien nom",
        capacity=25,
        status="maintenance",
    )

    create_response = client.post(
        "/stations",
        json=payload,
    )

    assert create_response.status_code == 201

    created = create_response.json()
    station_id = created["id"]

    patch_response = client.patch(
        f"/stations/{station_id}",
        json={
            "name": "Nouveau nom",
        },
    )

    assert patch_response.status_code == 200

    patched = patch_response.json()

    assert patched["name"] == "Nouveau nom"

    assert patched["code"] == payload["code"]
    assert patched["capacity"] == payload["capacity"]
    assert patched["status"] == payload["status"]


def test_unknown_station_returns_404(client):
    response = client.get("/stations/999")

    assert response.status_code == 404

    data = response.json()

    assert isinstance(data, dict)
    assert "detail" in data


@pytest.mark.parametrize(
    "payload",
    [
        station_payload(
            code="BAD-CAPACITY",
            capacity=0,
        ),
        station_payload(
            code="BAD-STATUS",
            status="flying",
        ),
    ],
)
def test_invalid_station_returns_422_and_creates_nothing(
    client,
    payload,
):
    response = client.post(
        "/stations",
        json=payload,
    )

    assert response.status_code == 422

    stations_response = client.get("/stations")

    assert stations_response.status_code == 200
    assert stations_response.json() == []


def test_duplicate_code_returns_409(client):
    payload = station_payload(
        code="ST-UNIQUE",
        name="Première station",
    )

    first_response = client.post(
        "/stations",
        json=payload,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/stations",
        json=payload,
    )

    assert second_response.status_code == 409

    stations_response = client.get("/stations")

    assert stations_response.status_code == 200

    stations = stations_response.json()

    assert len(stations) == 1
    assert stations[0]["code"] == "ST-UNIQUE"