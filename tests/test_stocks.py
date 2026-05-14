import pytest


def test_get_stocks_unauthorized(client):
    response = client.get("/stocks/")
    assert response.status_code == 401


def test_get_stocks_success(client, auth_headers, test_stock):
    response = client.get("/stocks/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(stock["symbol"] == "TEST" for stock in data)


def test_get_stock_by_symbol_success(client, auth_headers, test_stock):
    response = client.get("/stocks/TEST", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "TEST"
    assert data["name"] == "Test Stock"
    assert data["current_price"] == 100.00


def test_get_stock_by_symbol_not_found(client, auth_headers):
    response = client.get("/stocks/NONEXISTENT", headers=auth_headers)
    assert response.status_code == 404