def test_list_products_pagination(client):
    response = client.get("/api/products?page=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert "total" in data
    assert "page" in data
    assert "limit" in data
    assert data["page"] == 1
    assert data["limit"] == 10
    assert len(data["products"]) >= 2


def test_product_search(client):
    response = client.get("/api/products?search=Gold")
    assert response.status_code == 200
    data = response.json()
    assert len(data["products"]) >= 1
    assert "Gold" in data["products"][0]["name"]


def test_product_category_filter(client):
    response = client.get("/api/products?category_id=1")
    assert response.status_code == 200
    data = response.json()
    for p in data["products"]:
        assert p["category_id"] == 1


def test_get_product_by_id(client):
    response = client.get("/api/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["product_code"] == "TST-101"
    # Check React compatibility alias
    assert data["code"] == "TST-101"
    assert data["price"] == 60.0


def test_get_product_by_slug(client):
    response = client.get("/api/products/slug/10cm-gold-sparkler")
    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == "10cm-gold-sparkler"


def test_admin_create_product(client, admin_headers):
    payload = {
        "product_code": "NEW-301",
        "name": "Super Colour Flower Pot",
        "slug": "super-colour-flower-pot",
        "category_id": 1,
        "description": "Fountain fireworks",
        "original_price": 250.0,
        "selling_price": 180.0,
        "discount_percentage": 28,
        "stock_quantity": 100,
        "unit": "Box",
        "is_featured": True,
        "is_active": True
    }
    response = client.post("/api/products", json=payload, headers=admin_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["product_code"] == "NEW-301"


def test_admin_update_stock_negative_fails(client, admin_headers):
    response = client.patch("/api/products/1/stock", json={"stock_quantity": -5}, headers=admin_headers)
    assert response.status_code == 422 or response.status_code == 400


def test_admin_update_stock_success(client, admin_headers):
    response = client.patch("/api/products/1/stock", json={"stock_quantity": 85}, headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["stock_quantity"] == 85
