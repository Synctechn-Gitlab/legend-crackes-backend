from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.product import Product
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(Category)

    def get_by_slug(self, db: Session, slug: str) -> Optional[Category]:
        return db.query(Category).filter(Category.slug == slug.strip().lower()).first()

    def get_active(self, db: Session) -> List[Category]:
        return db.query(Category).filter(Category.is_active.is_(True)).order_by(Category.id.asc()).all()

    def get_with_counts(self, db: Session) -> List[dict]:
        categories = db.query(Category).order_by(Category.id.asc()).all()
        result = []
        for cat in categories:
            cnt = db.query(Product).filter(Product.category_id == cat.id, Product.is_active.is_(True)).count()
            result.append({
                "id": cat.id,
                "name": cat.name,
                "slug": cat.slug,
                "description": cat.description,
                "image_url": cat.image_url,
                "is_active": cat.is_active,
                "created_at": cat.created_at,
                "updated_at": cat.updated_at,
                "product_count": cnt
            })
        return result


category_repo = CategoryRepository()
