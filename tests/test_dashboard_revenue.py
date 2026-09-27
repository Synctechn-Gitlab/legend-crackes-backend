def test_admin_dashboard_metrics(client, admin_headers):
    res = client.get("/api/admin/dashboard", headers=admin_headers)
    assert res.status_code == 200
    data = res.json()
    assert "total_products" in data or "totalProducts" in data
    assert "total_orders" in data or "totalOrders" in data
    assert "total_revenue" in data or "totalRevenue" in data
    assert "revenue_over_time" in data or "revenueOverTime" in data


def test_admin_dashboard_stats_alias(client, admin_headers):
    res = client.get("/api/admin/dashboard/stats", headers=admin_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["totalProducts"] is not None


def test_admin_revenue_analytics(client, admin_headers):
    res = client.get("/api/admin/revenue?range=monthly", headers=admin_headers)
    assert res.status_code == 200
    data = res.json()
    assert "revenue" in data or "totalRevenue" in data
    assert "monthly_trend" in data or "monthlyTrend" in data


def test_admin_revenue_category_sales(client, admin_headers):
    res = client.get("/api/admin/revenue/category", headers=admin_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_admin_revenue_top_products(client, admin_headers):
    res = client.get("/api/admin/revenue/top-products", headers=admin_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
