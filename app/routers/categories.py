from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.admin_user import AdminUser
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services.category_service import category_service

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get(
    "",
    response_model=List[CategoryResponse],
    summary="List Categories",
    description="Fetch all active fireworks categories along with their live product counts."
)
def get_categories(db: Session = Depends(get_db)):
    return category_service.list_categories(db=db, active_only=True)


@router.get(
    "/{id}",
    response_model=CategoryResponse,
    summary="Get Category by ID",
    description="Retrieve specific category information by ID."
)
def get_category_by_id(id: int, db: Session = Depends(get_db)):
    return category_service.get_by_id(db=db, category_id=id)


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Category (Admin Only)",
    description="Add a new cracker product category. Requires admin JWT."
)
def create_category(
    cat_in: CategoryCreate,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return category_service.create_category(db=db, data=cat_in, admin_username=current_admin.username)


@router.put(
    "/{id}",
    response_model=CategoryResponse,
    summary="Update Category (Admin Only)",
    description="Update category name, description, or image. Requires admin JWT."
)
def update_category(
    id: int,
    updates: CategoryUpdate,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return category_service.update_category(
        db=db,
        category_id=id,
        updates=updates,
        admin_username=current_admin.username
    )


@router.delete(
    "/{id}",
    summary="Delete Category (Admin Only)",
    description="Delete a category. Requires admin JWT."
)
def delete_category(
    id: int,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return category_service.delete_category(
        db=db,
        category_id=id,
        admin_username=current_admin.username
    )
