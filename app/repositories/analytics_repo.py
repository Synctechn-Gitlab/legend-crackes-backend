from typing import Dict, Any, List
from datetime import datetime, time
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.category import Category


class AnalyticsRepository:
    def get_dashboard_metrics(self, db: Session) -> Dict[str, Any]:
        total_products = db.query(Product).count()
        active_products = db.query(Product).filter(Product.is_active.is_(True)).count()
        
        total_orders = db.query(Order).count()
        pending_orders = db.query(Order).filter(Order.order_status.ilike("pending")).count()
        completed_orders = db.query(Order).filter(Order.order_status.ilike("delivered")).count()
        
        # Revenue calculations
        revenue_sum = db.query(func.sum(Order.total_amount)).filter(
            Order.order_status.notin_(["Cancelled", "cancelled"])
        ).scalar() or 0.0

        # Profit calculation: sum((OrderItem.unit_price - func.coalesce(Product.my_price, Product.original_price)) * OrderItem.quantity)
        profit_query = db.query(
            func.sum((OrderItem.unit_price - func.coalesce(Product.my_price, Product.original_price)) * OrderItem.quantity)
        ).join(Product, Product.id == OrderItem.product_id)\
         .join(Order, Order.id == OrderItem.order_id)\
         .filter(Order.order_status.notin_(["Cancelled", "cancelled"])).scalar()
        
        total_revenue = float(revenue_sum)
        total_profit = float(profit_query) if profit_query is not None else 0.0
        total_cost = round(total_revenue - total_profit, 2)
        
        # Today's revenue
        today_start = datetime.combine(datetime.now().date(), time.min)
        today_revenue = db.query(func.sum(Order.total_amount)).filter(
            Order.created_at >= today_start,
            Order.order_status.notin_(["Cancelled", "cancelled"])
        ).scalar() or 0.0

        # Weekly revenue (last 7 days)
        from datetime import timedelta
        week_start = datetime.now() - timedelta(days=7)
        weekly_revenue = db.query(func.sum(Order.total_amount)).filter(
            Order.created_at >= week_start,
            Order.order_status.notin_(["Cancelled", "cancelled"])
        ).scalar() or 0.0

        # Stock quantity tracking
        low_stock_count = 0
        low_stock_products = []

        # Recent orders with preloaded items
        from sqlalchemy.orm import joinedload
        recent_orders = db.query(Order).options(
            joinedload(Order.items).joinedload(OrderItem.product)
        ).order_by(desc(Order.created_at)).limit(5).all()

        return {
            "total_products": total_products,
            "active_products": active_products,
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "completed_orders": completed_orders,
            "total_revenue": total_revenue,
            "today_revenue": float(today_revenue),
            "weekly_revenue": float(weekly_revenue),
            "total_profit": total_profit,
            "total_cost": total_cost,
            "low_stock_count": low_stock_count,
            "low_stock_products": low_stock_products,
            "recent_orders": recent_orders
        }

    def get_category_sales(self, db: Session) -> List[Dict[str, Any]]:
        results = db.query(
            Category.name,
            func.sum(OrderItem.total_price).label("sales_sum"),
            func.count(OrderItem.id).label("item_count")
        ).join(Product, Product.id == OrderItem.product_id)\
         .join(Category, Category.id == Product.category_id)\
         .group_by(Category.name)\
         .order_by(desc("sales_sum")).all()

        palette = ["#DC2626", "#F59E0B", "#10B981", "#6366F1", "#EC4899", "#8B5CF6", "#14B8A6"]
        total_sales = sum([float(r[1] or 0) for r in results]) or 1.0

        data = []
        for idx, r in enumerate(results):
            amount = float(r[1] or 0)
            share = round((amount / total_sales) * 100, 1)
            data.append({
                "category": r[0],
                "name": r[0],
                "amount": amount,
                "sales": amount,
                "percentage": share,
                "share": share,
                "color": palette[idx % len(palette)]
            })

        return data

    def get_top_products(self, db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        results = db.query(
            Product.id,
            Product.name,
            Product.product_code,
            Category.name.label("category_name"),
            func.sum(OrderItem.quantity).label("units_sold"),
            Product.selling_price,
            func.sum(OrderItem.total_price).label("product_revenue")
        ).join(OrderItem, OrderItem.product_id == Product.id)\
         .outerjoin(Category, Category.id == Product.category_id)\
         .group_by(Product.id, Product.name, Product.product_code, Category.name, Product.selling_price)\
         .order_by(desc("units_sold"))\
         .limit(limit).all()

        data = []
        for r in results:
            data.append({
                "id": r[0],
                "name": r[1],
                "code": r[2],
                "category": r[3] or "General",
                "units_sold": int(r[4] or 0),
                "unitsSold": int(r[4] or 0),
                "selling_price": float(r[5]),
                "sellingPrice": float(r[5]),
                "total_revenue": float(r[6] or 0),
                "totalRevenue": float(r[6] or 0)
            })

        return data

    def get_revenue_trend(self, db: Session, time_range: str = "monthly") -> List[Dict[str, Any]]:
        try:
            if time_range == "daily":
                trunc_col = func.date_trunc('day', Order.created_at)
            elif time_range == "weekly":
                trunc_col = func.date_trunc('week', Order.created_at)
            else:
                trunc_col = func.date_trunc('month', Order.created_at)

            results = db.query(
                trunc_col.label("period_dt"),
                func.sum(Order.total_amount).label("revenue"),
                func.count(Order.id).label("orders")
            ).filter(
                Order.order_status.notin_(["Cancelled", "cancelled"])
            ).group_by(trunc_col).order_by(trunc_col).all()

            trend = []
            for r in results:
                dt = r[0]
                if dt:
                    if time_range == "daily":
                        fmt_str = dt.strftime("%Y-%m-%d")
                    elif time_range == "weekly":
                        fmt_str = f"Week {dt.strftime('%V, %Y')}"
                    else:
                        fmt_str = dt.strftime("%b %Y")
                else:
                    fmt_str = "N/A"

                trend.append({
                    "period": fmt_str,
                    "month": fmt_str,
                    "date": fmt_str,
                    "revenue": float(r[1] or 0.0),
                    "sales": float(r[1] or 0.0),
                    "orders": int(r[2] or 0),
                    "orderCount": int(r[2] or 0)
                })

            return trend
        except Exception:
            return []


analytics_repo = AnalyticsRepository()
