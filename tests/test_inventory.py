def test_admin_inventory_list(client, admin_headers):
    res = client.get("/api/admin/inventory?page=1&limit=10", headers=admin_headers)
    assert res.status_code == 200
    data = res.json()
    assert "products" in data
    assert "total" in data


def test_admin_inventory_create_and_delete(client, admin_headers):
    # Create
    create_payload = {
        "product_code": "INV-777",
        "name": "Inventory Special Sound Cracker",
        "slug": "inv-special-sound-cracker",
        "category_id": 1,
        "description": "High decibel cracker",
        "original_price": 300.0,
        "selling_price": 200.0,
        "discount_percentage": 33,
        "stock_quantity": 40,
        "unit": "Box",
        "is_featured": False,
        "is_active": True
    }
    create_res = client.post("/api/admin/inventory/products", json=create_payload, headers=admin_headers)
    assert create_res.status_code == 201
    prod = create_res.json()
    new_id = prod["id"]

    # Delete
    del_res = client.delete(f"/api/admin/inventory/products/{new_id}", headers=admin_headers)
    assert del_res.status_code == 200


def test_admin_inventory_frontend_format(client, admin_headers):
    # Tests the exact payload structure sent by the React Admin UI
    frontend_payload = {
        "name": "Frontend Cracker Test",
        "code": "",
        "category": "sparklers",
        "categoryName": "Sparklers",
        "originalPrice": 250.0,
        "sellingPrice": 180.0,
        "stock": 85,
        "piecesPerBox": "10 Pieces per Pack",
        "soundLevel": "Zero Sound / Light",
        "duration": "45 Seconds",
        "image": "https://images.unsplash.com/photo-1513151233558-d860c5398176",
        "description": "Premium sparkler from frontend",
        "isFeatured": True,
        "isActive": True,
        "discount": 28
    }
    create_res = client.post("/api/admin/inventory", json=frontend_payload, headers=admin_headers)
    assert create_res.status_code == 201
    prod = create_res.json()
    assert prod["name"] == "Frontend Cracker Test"
    assert prod["stock"] == 85
    assert prod["sellingPrice"] == 180.0
    assert prod["originalPrice"] == 250.0
    assert prod["isFeatured"] is True
    assert prod["isActive"] is True
    assert prod["code"].startswith("SPK-")
    
    # Update with camelCase
    update_res = client.put(f"/api/admin/inventory/{prod['id']}", json={"stock": 120, "isActive": False}, headers=admin_headers)
    assert update_res.status_code == 200
    updated_prod = update_res.json()
    assert updated_prod["stock"] == 120
    assert updated_prod["isActive"] is False
