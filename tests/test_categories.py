def test_list_categories(client):
    res = client.get("/api/categories")
    assert res.status_code == 200
    cats = res.json()
    assert len(cats) >= 2
    assert any(c["slug"] == "sparklers" for c in cats)


def test_get_category_by_id(client):
    res = client.get("/api/categories/1")
    assert res.status_code == 200
    cat = res.json()
    assert cat["id"] == 1
    assert cat["slug"] == "sparklers"


def test_admin_create_and_delete_category(client, admin_headers):
    # 1. Create new category
    payload = {
        "name": "Giant Sky Lanterns",
        "slug": "giant-sky-lanterns",
        "description": "Illuminated hot-air paper lanterns",
        "is_active": True
    }
    res = client.post("/api/categories", json=payload, headers=admin_headers)
    assert res.status_code == 201
    cat_data = res.json()
    cat_id = cat_data["id"]
    assert cat_data["name"] == "Giant Sky Lanterns"

    # 2. Update the category
    update_payload = {"name": "Super Sky Lanterns"}
    res_update = client.put(f"/api/categories/{cat_id}", json=update_payload, headers=admin_headers)
    assert res_update.status_code == 200
    assert res_update.json()["name"] == "Super Sky Lanterns"

    # 3. Delete the category
    res_del = client.delete(f"/api/categories/{cat_id}", headers=admin_headers)
    assert res_del.status_code == 200
    assert res_del.json()["success"] is True

    # 4. Verify category no longer exists
    res_get = client.get(f"/api/categories/{cat_id}")
    assert res_get.status_code == 404

