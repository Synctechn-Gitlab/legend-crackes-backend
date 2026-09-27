from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.admin_user import AdminUser
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductStockUpdate,
    ProductResponse,
    ProductPaginatedResponse
)
from app.services.inventory_service import inventory_service

router = APIRouter(prefix="/admin/inventory", tags=["Admin Inventory"])


@router.get(
    "",
    response_model=ProductPaginatedResponse,
    summary="List Inventory (Admin)",
    description="Retrieve catalog inventory with low-stock alerts, active/inactive filters and live counts."
)
def get_inventory(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=15, ge=1, le=100),
    search: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
    in_stock: Optional[bool] = Query(default=None),
    sort_by: Optional[str] = Query(default="new"),
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return inventory_service.list_inventory(
        db=db,
        page=page,
        limit=limit,
        search=search,
        category=category,
        in_stock=in_stock,
        sort_by=sort_by
    )


# Support both /admin/inventory/products and /admin/inventory
@router.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Inventory Product (Admin)"
)
@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False
)
def add_inventory_product(
    product_in: ProductCreate,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return inventory_service.add_product(
        db=db,
        data=product_in,
        admin_username=current_admin.username
    )


@router.put(
    "/products/{id}",
    response_model=ProductResponse,
    summary="Update Inventory Product (Admin)"
)
@router.put(
    "/{id}",
    response_model=ProductResponse,
    include_in_schema=False
)
def update_inventory_product(
    id: int,
    updates: ProductUpdate,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return inventory_service.update_product(
        db=db,
        product_id=id,
        updates=updates,
        admin_username=current_admin.username
    )


@router.patch(
    "/products/{id}/stock",
    response_model=ProductResponse,
    summary="Adjust Product Stock (Admin)"
)
@router.patch(
    "/{id}/stock",
    response_model=ProductResponse,
    include_in_schema=False
)
def adjust_inventory_stock(
    id: int,
    stock_payload: ProductStockUpdate,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return inventory_service.update_stock(
        db=db,
        product_id=id,
        stock_data=stock_payload,
        admin_username=current_admin.username
    )


@router.delete(
    "/products/{id}",
    summary="Delete Inventory Product (Admin)"
)
@router.delete(
    "/{id}",
    include_in_schema=False
)
def delete_inventory_product(
    id: int,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return inventory_service.delete_product(
        db=db,
        product_id=id,
        admin_username=current_admin.username
    )
