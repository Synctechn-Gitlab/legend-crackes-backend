from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.category import Category
from app.repositories.category_repo import category_repo
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.utils.formatters import slugify
from app.core.logging import audit_logger


class CategoryService:
    def list_categories(self, db: Session, active_only: bool = True) -> List[CategoryResponse]:
        raw = category_repo.get_with_counts(db)
        if active_only:
            raw = [c for c in raw if c["is_active"]]
        return [CategoryResponse(**c) for c in raw]

    def get_by_id(self, db: Session, category_id: int) -> CategoryResponse:
        cat = category_repo.get(db, category_id)
        if not cat:
            raise HTTPException(status_code=404, detail="Category not found.")
        raw = category_repo.get_with_counts(db)
        match = next((c for c in raw if c["id"] == category_id), None)
        return CategoryResponse(**(match or cat.__dict__))

    def create_category(self, db: Session, data: CategoryCreate, admin_username: str) -> CategoryResponse:
        base_slug = slugify(data.slug or data.name)
        slug = base_slug
        idx = 1
        while category_repo.get_by_slug(db, slug):
            slug = f"{base_slug}-{idx}"
            idx += 1

        cat = Category(
            name=data.name.strip(),
            slug=slug,
            description=data.description,
            image_url=data.image_url,
            is_active=data.is_active
        )
        db.add(cat)
        db.commit()
        db.refresh(cat)
        audit_logger.info(f"Category created: {cat.name} by admin {admin_username}")
        return self.get_by_id(db, cat.id)

    def update_category(self, db: Session, category_id: int, updates: CategoryUpdate, admin_username: str) -> CategoryResponse:
        cat = category_repo.get(db, category_id)
        if not cat:
            raise HTTPException(status_code=404, detail="Category not found.")

        data = updates.model_dump(exclude_unset=True)
        if "slug" in data and data["slug"]:
            slug = slugify(data["slug"])
            existing = category_repo.get_by_slug(db, slug)
            if existing and existing.id != category_id:
                raise HTTPException(status_code=400, detail="Category slug already in use.")
            data["slug"] = slug

        for k, v in data.items():
            setattr(cat, k, v)

        db.commit()
        db.refresh(cat)
        audit_logger.info(f"Category updated: {cat.name} by admin {admin_username}")
        return self.get_by_id(db, cat.id)

    def delete_category(self, db: Session, category_id: int, admin_username: str) -> dict:
        cat = category_repo.get(db, category_id)
        if not cat:
            raise HTTPException(status_code=404, detail="Category not found.")
        name = cat.name
        
        # Dissociate products so foreign key constraints are clean
        from app.models.product import Product
        db.query(Product).filter(Product.category_id == category_id).update({Product.category_id: None})
        
        db.delete(cat)
        db.commit()
        audit_logger.info(f"Category deleted: {name} by admin {admin_username}")
        return {"success": True, "message": f"Category '{name}' deleted successfully."}


category_service = CategoryService()
