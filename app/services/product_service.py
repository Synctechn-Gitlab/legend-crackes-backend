import math
import uuid
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.product_image import ProductImage
from app.repositories.product_repo import product_repo
from app.repositories.category_repo import category_repo
from app.schemas.product import ProductCreate, ProductUpdate, ProductPaginatedResponse, ProductResponse
from app.utils.formatters import format_product_dict, slugify
from app.core.logging import audit_logger


class ProductService:
    def list_products(
        self,
        db: Session,
        page: int = 1,
        limit: int = 24,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        category_slug: Optional[str] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        is_featured: Optional[bool] = None,
        in_stock: Optional[bool] = None,
        is_active: Optional[bool] = True,
        sort_by: Optional[str] = "featured"
    ) -> ProductPaginatedResponse:
        safe_limit = min(max(1, limit), 100)
        safe_page = max(1, page)
        offset = (safe_page - 1) * safe_limit

        if not category_id and category_slug and category_slug.isdigit():
            category_id = int(category_slug)
            category_slug = None

        products, total = product_repo.query_products(
            db=db,
            offset=offset,
            limit=safe_limit,
            search=search,
            category_id=category_id,
            category_slug=category_slug,
            price_min=price_min,
            price_max=price_max,
            is_featured=is_featured,
            in_stock=in_stock,
            is_active=is_active,
            sort_by=sort_by
        )

        total_pages = math.ceil(total / safe_limit) if total > 0 else 1
        formatted = [ProductResponse(**format_product_dict(p)) for p in products]

        return ProductPaginatedResponse(
            products=formatted,
            total=total,
            page=safe_page,
            limit=safe_limit,
            total_pages=total_pages
        )

    def get_by_id(self, db: Session, product_id: int) -> ProductResponse:
        prod = product_repo.get_by_id(db, product_id)
        if not prod:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found."
            )
        return ProductResponse(**format_product_dict(prod))

    def get_by_slug(self, db: Session, slug: str) -> ProductResponse:
        prod = product_repo.get_by_slug(db, slug)
        if not prod:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with slug '{slug}' not found."
            )
        return ProductResponse(**format_product_dict(prod))

    def create_product(self, db: Session, data: ProductCreate, admin_username: str) -> ProductResponse:
        # Product code generation or duplicate check
        product_code = (data.product_code or "").strip().upper()
        if not product_code:
            product_code = f"SPK-{uuid.uuid4().hex[:6].upper()}"
            while product_repo.get_by_code(db, product_code):
                product_code = f"SPK-{uuid.uuid4().hex[:6].upper()}"
        elif product_repo.get_by_code(db, product_code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product code '{product_code}' already exists."
            )

        # Slug generation if needed
        base_slug = slugify(data.slug or data.name)
        slug = base_slug
        idx = 1
        while product_repo.get_by_slug(db, slug):
            slug = f"{base_slug}-{idx}"
            idx += 1

        # Category resolution
        cat_id = data.category_id
        if not cat_id and getattr(data, "category", None):
            val = str(data.category).strip().lower()
            if val and val != "all":
                cat = category_repo.get_by_slug(db, val)
                if cat:
                    cat_id = cat.id

        # Calculate discount percentage if not provided
        discount = data.discount_percentage
        if discount == 0 and data.original_price > data.selling_price and data.original_price > 0:
            discount = round(((data.original_price - data.selling_price) / data.original_price) * 100)

        prod = Product(
            product_code=product_code,
            name=data.name.strip(),
            slug=slug,
            category_id=cat_id,
            description=data.description,
            image_url=data.image_url,
            original_price=data.original_price,
            selling_price=data.selling_price,
            my_price=data.my_price if data.my_price is not None else data.original_price,
            discount_percentage=discount,
            stock_quantity=data.stock_quantity,
            unit=data.unit or "Box",
            is_featured=data.is_featured,
            is_active=data.is_active
        )
        db.add(prod)
        db.flush()

        # Handle secondary images if any
        if data.images:
            for s_idx, img_url in enumerate(data.images):
                img = ProductImage(product_id=prod.id, image_url=img_url, sort_order=s_idx)
                db.add(img)

        db.commit()
        db.refresh(prod)
        audit_logger.info(f"Product created: {prod.product_code} by admin {admin_username}")
        return ProductResponse(**format_product_dict(prod))

    def update_product(self, db: Session, product_id: int, updates: ProductUpdate, admin_username: str) -> ProductResponse:
        prod = product_repo.get_by_id(db, product_id)
        if not prod:
            raise HTTPException(status_code=404, detail="Product not found.")

        update_dict = updates.model_dump(exclude_unset=True)
        if "stock_quantity" in update_dict and update_dict["stock_quantity"] < 0:
            raise HTTPException(status_code=400, detail="Stock quantity cannot be negative.")

        # Resolve category slug if category_id not provided
        if "category_id" not in update_dict and getattr(updates, "category", None):
            val = str(updates.category).strip().lower()
            if val and val != "all":
                cat = category_repo.get_by_slug(db, val)
                if cat:
                    update_dict["category_id"] = cat.id

        valid_columns = {c.name for c in Product.__table__.columns} - {"id", "created_at", "updated_at"}

        for key, val in update_dict.items():
            if key in valid_columns:
                setattr(prod, key, val)

        # Recalculate discount if prices updated
        if "selling_price" in update_dict or "original_price" in update_dict:
            orig = float(prod.original_price or 0.0)
            sell = float(prod.selling_price or 0.0)
            if orig > sell and orig > 0:
                prod.discount_percentage = round(((orig - sell) / orig) * 100)

        db.commit()
        db.refresh(prod)
        audit_logger.info(f"Product updated: {prod.product_code} (ID: {prod.id}) by admin {admin_username}")
        return ProductResponse(**format_product_dict(prod))

    def update_stock(self, db: Session, product_id: int, new_stock: int, admin_username: str) -> ProductResponse:
        if new_stock < 0:
            raise HTTPException(status_code=400, detail="Stock quantity cannot be negative.")

        prod = product_repo.get_by_id(db, product_id)
        if not prod:
            raise HTTPException(status_code=404, detail="Product not found.")

        old_stock = prod.stock_quantity
        prod.stock_quantity = new_stock
        db.commit()
        db.refresh(prod)
        audit_logger.info(f"Stock adjusted for {prod.product_code}: {old_stock} -> {new_stock} by {admin_username}")
        return ProductResponse(**format_product_dict(prod))

    def delete_product(self, db: Session, product_id: int, admin_username: str) -> dict:
        prod = product_repo.get_by_id(db, product_id)
        if not prod:
            raise HTTPException(status_code=404, detail="Product not found.")

        code = prod.product_code
        db.delete(prod)
        db.commit()
        audit_logger.info(f"Product deleted: {code} (ID: {product_id}) by admin {admin_username}")
        return {"success": True, "message": f"Product {code} deleted successfully."}


product_service = ProductService()
