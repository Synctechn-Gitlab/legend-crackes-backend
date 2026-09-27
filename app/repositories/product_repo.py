from typing import Optional, List, Tuple
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, desc, asc
from app.models.product import Product
from app.models.category import Category
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self):
        super().__init__(Product)

    def get_by_id(self, db: Session, product_id: int) -> Optional[Product]:
        return db.query(Product).options(
            joinedload(Product.category),
            joinedload(Product.images)
        ).filter(Product.id == product_id).first()

    def get_by_id_for_update(self, db: Session, product_id: int) -> Optional[Product]:
        """Locks the product row for transaction consistency during checkout."""
        # SQLite doesn't support SELECT ... FOR UPDATE, SQLAlchemy handles it gracefully
        return db.query(Product).with_for_update().filter(Product.id == product_id).first()

    def get_by_code(self, db: Session, product_code: str) -> Optional[Product]:
        return db.query(Product).options(
            joinedload(Product.category)
        ).filter(Product.product_code == product_code.strip()).first()

    def get_by_slug(self, db: Session, slug: str) -> Optional[Product]:
        return db.query(Product).options(
            joinedload(Product.category),
            joinedload(Product.images)
        ).filter(Product.slug == slug.strip().lower()).first()

    def query_products(
        self,
        db: Session,
        offset: int = 0,
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
    ) -> Tuple[List[Product], int]:
        """High performance indexed query across 3000+ items."""
        query = db.query(Product).options(joinedload(Product.category))

        # Filter by active status
        if is_active is not None:
            query = query.filter(Product.is_active == is_active)

        # Category filter (by ID or Slug)
        if category_id is not None:
            query = query.filter(Product.category_id == category_id)
        elif category_slug and category_slug != "all":
            query = query.join(Product.category).filter(Category.slug == category_slug.lower())

        # Search filter (name or product code)
        if search and search.strip():
            term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Product.name.ilike(term),
                    Product.product_code.ilike(term),
                    Product.description.ilike(term)
                )
            )

        # Price range filters
        if price_min is not None and price_min > 0:
            query = query.filter(Product.selling_price >= price_min)
        if price_max is not None and price_max > 0:
            query = query.filter(Product.selling_price <= price_max)

        # Featured filter
        if is_featured is not None:
            query = query.filter(Product.is_featured == is_featured)

        # In-stock filter
        if in_stock is True:
            query = query.filter(Product.stock_quantity > 0)
        elif in_stock is False:
            query = query.filter(Product.stock_quantity == 0)

        # Total count before pagination
        total = query.count()

        # Sorting
        sort_lower = (sort_by or "featured").lower()
        if sort_lower in ["price-asc", "price_low_high", "price_asc"]:
            query = query.order_by(asc(Product.selling_price), asc(Product.id))
        elif sort_lower in ["price-desc", "price_high_low", "price_desc"]:
            query = query.order_by(desc(Product.selling_price), desc(Product.id))
        elif sort_lower in ["discount", "discount_high"]:
            query = query.order_by(desc(Product.discount_percentage), asc(Product.id))
        elif sort_lower in ["name", "name_asc"]:
            query = query.order_by(asc(Product.name))
        elif sort_lower in ["new", "latest"]:
            query = query.order_by(desc(Product.created_at))
        elif sort_lower in ["stock_low", "low_stock"]:
            query = query.order_by(asc(Product.stock_quantity))
        else:  # featured default
            query = query.order_by(desc(Product.is_featured), desc(Product.id))

        products = query.offset(offset).limit(limit).all()
        return products, total


product_repo = ProductRepository()
