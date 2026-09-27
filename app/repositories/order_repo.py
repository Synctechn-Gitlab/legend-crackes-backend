from typing import Optional, List, Tuple
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, desc
from app.models.order import Order, OrderItem
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    def __init__(self):
        super().__init__(Order)

    def get_by_id(self, db: Session, order_id: int) -> Optional[Order]:
        return db.query(Order).options(
            joinedload(Order.items)
        ).filter(Order.id == order_id).first()

    def get_by_order_number(self, db: Session, order_number: str) -> Optional[Order]:
        return db.query(Order).options(
            joinedload(Order.items)
        ).filter(Order.order_number == order_number.strip()).first()

    def query_orders(
        self,
        db: Session,
        offset: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        status: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None
    ) -> Tuple[List[Order], int]:
        query = db.query(Order).options(joinedload(Order.items))

        # Status filter
        if status and status.lower() != "all":
            query = query.filter(Order.order_status.ilike(status.strip()))

        # Search filter (order number, customer phone, customer name)
        if search and search.strip():
            term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Order.order_number.ilike(term),
                    Order.customer_phone.ilike(term),
                    Order.customer_name.ilike(term)
                )
            )

        # Date filtering
        if date_from:
            query = query.filter(Order.created_at >= date_from)
        if date_to:
            query = query.filter(Order.created_at <= date_to)

        total = query.count()
        orders = query.order_by(desc(Order.created_at)).offset(offset).limit(limit).all()
        return orders, total


order_repo = OrderRepository()
