from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.admin_user import AdminUser
from app.schemas.dashboard import DashboardStatsResponse
from app.services.analytics_service import analytics_service

router = APIRouter(prefix="/admin/dashboard", tags=["Admin Dashboard"])


@router.get(
    "",
    response_model=DashboardStatsResponse,
    summary="Admin Dashboard Metrics",
    description="Retrieve live KPI statistics: total/active products, order statuses, today/lifetime revenue, and low stock warnings."
)
@router.get(
    "/stats",
    response_model=DashboardStatsResponse,
    include_in_schema=False
)
def get_dashboard_stats(
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return analytics_service.get_dashboard(db=db)
