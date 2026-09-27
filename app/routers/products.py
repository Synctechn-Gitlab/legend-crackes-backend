from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.admin_user import AdminUser
from app.schemas.product import (
    ProductResponse,
    ProductPaginatedResponse,
    ProductCreate,
    ProductUpdate,
    ProductStockUpdate
)
from app.services.product_service import product_service

router = APIRouter(prefix="/products", tags=["Products"])


@router.get(
    "",
    response_model=ProductPaginatedResponse,
    summary="List Products with Filtering & Pagination",
    description="Fetch paginated crackers with search, category filtering, price range, and sorting. Server-side pagination ensures fast loading across 3000+ products."
)
def get_products(
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=24, ge=1, le=100, description="Items per page (max 100)"),
    search: Optional[str] = Query(default=None, description="Search term for name or product code"),
    category_id: Optional[int] = Query(default=None, description="Filter by Category ID"),
    category: Optional[str] = Query(default=None, description="Filter by Category Slug (e.g. sparklers, aerial-shots)"),
    sort_by: Optional[str] = Query(default="featured", description="Sorting option: featured, price-asc, price-desc, discount, name, new"),
    price_min: Optional[float] = Query(default=None, ge=0, description="Minimum price filter"),
    price_max: Optional[float] = Query(default=None, ge=0, description="Maximum price filter"),
    is_featured: Optional[bool] = Query(default=None, description="Filter featured products"),
    in_stock: Optional[bool] = Query(default=None, description="Filter items currently in stock"),
    db: Session = Depends(get_db)
):
    return product_service.list_products(
        db=db,
        page=page,
        limit=limit,
        search=search,
        category_id=category_id,
        category_slug=category,
        price_min=price_min,
        price_max=price_max,
        is_featured=is_featured,
        in_stock=in_stock,
        is_active=True,
        sort_by=sort_by
    )


@router.get(
    "/featured",
    summary="Get Featured Products",
    description="Fetch featured products for home page showcase."
)
def get_featured_products(
    limit: int = Query(default=8, ge=1, le=50),
    db: Session = Depends(get_db)
):
    res = product_service.list_products(db=db, page=1, limit=limit, is_featured=True, sort_by="featured")
    return res.products


@router.get(
    "/special-offers",
    summary="Get Festive Deals & Offers",
    description="Fetch top discounted products for festival promotions."
)
def get_special_offers(
    limit: int = Query(default=8, ge=1, le=50),
    db: Session = Depends(get_db)
):
    res = product_service.list_products(db=db, page=1, limit=limit, sort_by="discount")
    return res.products


@router.get(
    "/search",
    summary="Quick Search Autocomplete",
    description="Search products by prefix or keyword for live search dropdowns."
)
def search_products(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(default=6, ge=1, le=20),
    db: Session = Depends(get_db)
):
    res = product_service.list_products(db=db, page=1, limit=limit, search=q)
    return res.products


@router.get(
    "/slug/{slug}",
    response_model=ProductResponse,
    summary="Get Product by Slug",
    description="Retrieve full product details by its unique URL slug."
)
def get_product_by_slug(slug: str, db: Session = Depends(get_db)):
    return product_service.get_by_slug(db=db, slug=slug)


@router.get(
    "/{id}",
    response_model=ProductResponse,
    summary="Get Product by ID",
    description="Retrieve full product details by primary key ID."
)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    return product_service.get_by_id(db=db, product_id=id)


# Admin-Only Product Routes
@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create New Product (Admin Only)",
    description="Add a new cracker product to the catalog. Requires admin JWT."
)
def create_product(
    product_in: ProductCreate,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return product_service.create_product(db=db, data=product_in, admin_username=current_admin.username)


@router.put(
    "/{id}",
    response_model=ProductResponse,
    summary="Update Product (Admin Only)",
    description="Modify product attributes, pricing, or visibility. Requires admin JWT."
)
def update_product(
    id: int,
    updates: ProductUpdate,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return product_service.update_product(
        db=db,
        product_id=id,
        updates=updates,
        admin_username=current_admin.username
    )


@router.patch(
    "/{id}/stock",
    response_model=ProductResponse,
    summary="Update Product Stock (Admin Only)",
    description="Quick inline update for inventory stock quantity. Stock cannot be negative."
)
def update_product_stock(
    id: int,
    stock_payload: ProductStockUpdate,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return product_service.update_stock(
        db=db,
        product_id=id,
        new_stock=stock_payload.stock_quantity,
        admin_username=current_admin.username
    )


@router.delete(
    "/{id}",
    summary="Delete Product (Admin Only)",
    description="Permanently remove a cracker product from catalog. Requires admin JWT."
)
def delete_product(
    id: int,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return product_service.delete_product(
        db=db,
        product_id=id,
        admin_username=current_admin.username
    )
