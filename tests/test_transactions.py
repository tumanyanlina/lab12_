import pytest


def test_buy_stock_unauthorized(client):
    response = client.post("/transactions/buy", json={
        "stock_symbol": "TEST",
        "type": "BUY",
        "quantity": 10
    })
    assert response.status_code == 403


def test_buy_stock_success(client, auth_headers, test_stock):
    response = client.post("/transactions/buy", headers=auth_headers, json={
        "stock_symbol": "TEST",
        "type": "BUY",
        "quantity": 5
    })
    assert response.status_code == 201
    data = response.json()
    assert data["stock_symbol"] == "TEST"
    assert data["type"] == "BUY"
    assert data["quantity"] == 5
    assert data["total_amount"] == 500.00


def test_buy_stock_wrong_type(client, auth_headers, test_stock):
    response = client.post("/transactions/buy", headers=auth_headers, json={
        "stock_symbol": "TEST",
        "type": "SELL",
        "quantity": 5
    })
    assert response.status_code == 400
    assert "Invalid transaction type" in response.text


def test_buy_stock_insufficient_funds(client, auth_headers, test_stock):
    response = client.post("/transactions/buy", headers=auth_headers, json={
        "stock_symbol": "TEST",
        "type": "BUY",
        "quantity": 2000
    })
    assert response.status_code == 400
    assert "Insufficient funds" in response.text


def test_buy_stock_zero_quantity(client, auth_headers, test_stock):
    response = client.post("/transactions/buy", headers=auth_headers, json={
        "stock_symbol": "TEST",
        "type": "BUY",
        "quantity": 0
    })
    assert response.status_code == 422


def test_buy_stock_negative_quantity(client, auth_headers, test_stock):
    response = client.post("/transactions/buy", headers=auth_headers, json={
        "stock_symbol": "TEST",
        "type": "BUY",
        "quantity": -5
    })
    assert response.status_code == 422


def test_sell_stock_success(client, auth_headers, test_stock):
    client.post("/transactions/buy", headers=auth_headers, json={
        "stock_symbol": "TEST",
        "type": "BUY",
        "quantity": 10
    })
    
    response = client.post("/transactions/sell", headers=auth_headers, json={
        "stock_symbol": "TEST",
        "type": "SELL",
        "quantity": 5
    })
    assert response.status_code == 201
    data = response.json()
    assert data["stock_symbol"] == "TEST"
    assert data["type"] == "SELL"
    assert data["quantity"] == 5


def test_sell_more_than_owned(client, auth_headers, test_stock):
    client.post("/transactions/buy", headers=auth_headers, json={
        "stock_symbol": "TEST",
        "type": "BUY",
        "quantity": 5
    })
    
    response = client.post("/transactions/sell", headers=auth_headers, json={
        "stock_symbol": "TEST",
        "type": "SELL",
        "quantity": 10
    })
    assert response.status_code == 400
    assert "Not enough shares" in response.text


def test_transaction_history(client, auth_headers, test_stock):
    client.post("/transactions/buy", headers=auth_headers, json={
        "stock_symbol": "TEST",
        "type": "BUY",
        "quantity": 5
    })
    client.post("/transactions/buy", headers=auth_headers, json={
        "stock_symbol": "TEST",
        "type": "BUY",
        "quantity": 3
    })
    
    response = client.get("/transactions/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
