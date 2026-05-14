import pytest


def test_get_portfolio_unauthorized(client):
    response = client.get("/portfolio/")
    assert response.status_code == 403


def test_get_portfolio_empty(client, auth_headers):
    response = client.get("/portfolio/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total_value"] == 0.0
    assert data["total_profit_loss"] == 0.0


def test_get_portfolio_after_buy(client, auth_headers, test_stock):
    client.post("/transactions/buy", headers=auth_headers, json={
        "stock_symbol": "TEST",
        "type": "BUY",
        "quantity": 10
    })
    
    response = client.get("/portfolio/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    item = data["items"][0]
    assert item["stock_symbol"] == "TEST"
    assert item["quantity"] == 10
    assert item["total_value"] == 1000.00
    assert item["profit_loss"] == 0.0


def test_get_portfolio_after_sell(client, auth_headers, test_stock):
    client.post("/transactions/buy", headers=auth_headers, json={
        "stock_symbol": "TEST",
        "type": "BUY",
        "quantity": 10
    })
    
    client.post("/transactions/sell", headers=auth_headers, json={
        "stock_symbol": "TEST",
        "type": "SELL",
        "quantity": 3
    })
    
    response = client.get("/portfolio/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    item = data["items"][0]
    assert item["quantity"] == 7