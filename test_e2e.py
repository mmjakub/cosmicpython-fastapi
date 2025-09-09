import httpx


def test_allocation_endpoint_is_up():
    line = {"order_id": "ord-1", "sku": "not-found-in-db", "quantity": 42}
    r = httpx.post(f"http://localhost/allocate", json=line)

    assert r.status_code == 400
    assert r.json() == {"detail": "Not enough stock to allocate 42 not-found-in-db"}
