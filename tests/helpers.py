"""
Helper functions for tests
"""

def make_user(client, name="Alice", email="alice@example.com", phone="0712345678", pwd="secret123"):
    resp = client.post("/users/", json={
        "name": name,
        "phone_number": phone,
        "email": email,
        "password": pwd,
    })
    assert resp.status_code == 200
    return resp.json()

def make_show(client, title="Rock Night", venue="Arena", starts_at="2030-01-01T20:00:00Z"):
    resp = client.post("/shows/", json={
        "title": title,
        "venue": venue,
        "starts_at": starts_at
    })
    assert resp.status_code == 200
    return resp.json()

def add_seats(client, show_id: int, labels: list[str]):
    resp = client.post(f"/shows/{show_id}/seats", json={"seat_numbers": labels})
    return resp

def hold(client, user_id: int, show_id: int, seat_label: str, minutes: int = 10):
    return client.post(f"/reservations/{user_id}/hold", json={
        "seat_number": seat_label,
        "show_id": show_id,
        "hold_minutes": minutes
    })

def confirm_reservation(client, reservation_id: int):
    return client.post(f"/reservations/{reservation_id}/confirm")