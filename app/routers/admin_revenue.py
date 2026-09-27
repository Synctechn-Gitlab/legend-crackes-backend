from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.admin_user import AdminUser
from app.schemas.revenue import RevenueAnalyticsResponse
from app.services.analytics_service import analytics_service

router = APIRouter(prefix="/admin/revenue", tags=["Admin Revenue"])


@router.get(
    "",
    response_model=RevenueAnalyticsResponse,
    summary="Revenue Analytics",
    description="Retrieve financial metrics with period breakdown (daily, weekly, monthly, custom)."
)
def get_revenue_metrics(
    range: Optional[str] = Query(default="monthly", description="Time range: daily, weekly, monthly"),
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return analytics_service.get_revenue_analytics(db=db, time_range=range)


@router.get(
    "/category",
    response_model=List[Dict[str, Any]],
    summary="Category-wise Sales Distribution",
    description="Sales volume and percentage contribution broken down by crackers category."
)
def get_category_sales(
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return analytics_service.get_category_sales(db=db)


@router.get(
    "/top-products",
    response_model=List[Dict[str, Any]],
    summary="Top-Selling Products",
    description="Best-selling crackers ranked by units sold and gross revenue."
)
def get_top_products(
    limit: int = Query(default=10, ge=1, le=50),
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return analytics_service.get_top_products(db=db, limit=limit)
