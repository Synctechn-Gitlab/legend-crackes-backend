from app.routers.auth import router as auth_router
from app.routers.products import router as products_router
from app.routers.categories import router as categories_router
from app.routers.orders import router as orders_router
from app.routers.admin_orders import router as admin_orders_router
from app.routers.admin_inventory import router as admin_inventory_router
from app.routers.admin_dashboard import router as admin_dashboard_router
from app.routers.admin_revenue import router as admin_revenue_router

__all__ = [
    "auth_router",
    "products_router",
    "categories_router",
    "orders_router",
    "admin_orders_router",
    "admin_inventory_router",
    "admin_dashboard_router",
    "admin_revenue_router",
]
