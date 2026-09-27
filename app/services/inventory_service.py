from typing import Optional
from sqlalchemy.orm import Session
from app.services.product_service import product_service
from app.schemas.product import ProductCreate, ProductUpdate, ProductStockUpdate, ProductResponse, ProductPaginatedResponse


class InventoryService:
    def list_inventory(
        self,
        db: Session,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        category: Optional[str] = None,
        in_stock: Optional[bool] = None,
        sort_by: Optional[str] = "new"
    ) -> ProductPaginatedResponse:
        # Category can be ID or slug or "all"
        cat_id = int(category) if category and category.isdigit() else None
        cat_slug = category if category and not category.isdigit() and category != "all" else None

        return product_service.list_products(
            db=db,
            page=page,
            limit=limit,
            search=search,
            category_id=cat_id,
            category_slug=cat_slug,
            in_stock=in_stock,
            is_active=None,  # Return both active and inactive in inventory management
            sort_by=sort_by
        )

    def add_product(self, db: Session, data: ProductCreate, admin_username: str) -> ProductResponse:
        return product_service.create_product(db, data, admin_username)

    def update_product(self, db: Session, product_id: int, updates: ProductUpdate, admin_username: str) -> ProductResponse:
        return product_service.update_product(db, product_id, updates, admin_username)

    def update_stock(self, db: Session, product_id: int, stock_data: ProductStockUpdate, admin_username: str) -> ProductResponse:
        return product_service.update_stock(db, product_id, stock_data.stock_quantity, admin_username)

    def delete_product(self, db: Session, product_id: int, admin_username: str) -> dict:
        return product_service.delete_product(db, product_id, admin_username)


inventory_service = InventoryService()
