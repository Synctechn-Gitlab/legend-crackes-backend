from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import order_service

router = APIRouter(prefix="/orders", tags=["Orders (Public)"])


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Order (Guest Checkout)",
    description=(
        "Public endpoint for customer order placement without mandatory registration. "
        "Strictly recalculates all line-item prices, subtotal, and discounts on the server. "
        "Deducts product inventory in an atomic database transaction with rollback protection."
    )
)
def place_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    return order_service.create_order(db=db, order_in=order_in)
