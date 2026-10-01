from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.repositories.analytics_repo import analytics_repo
from app.schemas.dashboard import DashboardStatsResponse
from app.schemas.revenue import RevenueAnalyticsResponse
from app.utils.formatters import format_product_dict, format_order_dict
from app.schemas.product import ProductResponse
from app.schemas.order import OrderResponse


class AnalyticsService:
    def get_dashboard(self, db: Session) -> DashboardStatsResponse:
        metrics = analytics_repo.get_dashboard_metrics(db)
        
        # Format recent orders and low stock products
        low_stock_formatted = [ProductResponse(**format_product_dict(p)) for p in metrics["low_stock_products"]]
        recent_orders_formatted = [OrderResponse(**format_order_dict(o)) for o in metrics["recent_orders"]]
        category_sales = analytics_repo.get_category_sales(db)

        revenue_over_time = []

        total_rev = metrics["total_revenue"]
        today_rev = metrics["today_revenue"]
        total_profit = metrics.get("total_profit", 0.0)
        total_cost = metrics.get("total_cost", 0.0)

        return DashboardStatsResponse(
            total_products=metrics["total_products"],
            active_products=metrics["active_products"],
            total_orders=metrics["total_orders"],
            pending_orders=metrics["pending_orders"],
            completed_orders=metrics["completed_orders"],
            total_revenue=total_rev,
            today_revenue=today_rev,
            total_profit=total_profit,
            total_cost=total_cost,
            low_stock_count=metrics["low_stock_count"],
            low_stock_products=low_stock_formatted,
            recent_orders=recent_orders_formatted,
            revenue_over_time=revenue_over_time,
            category_wise_sales=category_sales,
            # React camelCase fields
            totalProducts=metrics["total_products"],
            totalOrders=metrics["total_orders"],
            pendingOrders=metrics["pending_orders"],
            completedOrders=metrics["completed_orders"],
            totalRevenue=total_rev,
            todayRevenue=today_rev,
            totalProfit=total_profit,
            totalCost=total_cost,
            lowStockCount=metrics["low_stock_count"],
            lowStockProducts=low_stock_formatted,
            recentOrders=recent_orders_formatted,
            revenueOverTime=revenue_over_time,
            categoryWiseSales=category_sales,
        )

    def get_revenue_analytics(self, db: Session, time_range: str = "monthly") -> RevenueAnalyticsResponse:
        metrics = analytics_repo.get_dashboard_metrics(db)
        total_rev = metrics["total_revenue"]
        order_cnt = metrics["total_orders"]
        aov = round(total_rev / order_cnt, 2) if order_cnt > 0 else 0.0
        total_profit = metrics.get("total_profit", 0.0)
        total_cost = metrics.get("total_cost", 0.0)

        monthly_trend = analytics_repo.get_revenue_trend(db, time_range=time_range)

        cat_sales = analytics_repo.get_category_sales(db)
        top_prods = analytics_repo.get_top_products(db)

        weekly_rev = metrics.get("weekly_revenue", 0.0)

        return RevenueAnalyticsResponse(
            revenue=total_rev,
            order_count=order_cnt,
            average_order_value=aov,
            time_range=time_range,
            total_profit=total_profit,
            total_cost=total_cost,
            daily_revenue=metrics["today_revenue"],
            weekly_revenue=weekly_rev,
            monthly_revenue=total_rev,
            revenue_growth="Live Real-time Metrics",
            monthly_trend=monthly_trend,
            sales_by_category=cat_sales,
            top_selling_products=top_prods,
            # Frontend compatibility
            totalRevenue=total_rev,
            totalProfit=total_profit,
            totalCost=total_cost,
            orderCount=order_cnt,
            averageOrderValue=aov,
            dailyRevenue=metrics["today_revenue"],
            weeklyRevenue=weekly_rev,
            monthlyRevenue=total_rev,
            revenueGrowth="Live Real-time Metrics",
            monthlyTrend=monthly_trend,
            salesByCategory=cat_sales,
            topSellingProducts=top_prods,
        )

    def get_category_sales(self, db: Session) -> List[Dict[str, Any]]:
        return analytics_repo.get_category_sales(db)

    def get_top_products(self, db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        return analytics_repo.get_top_products(db, limit=limit)


analytics_service = AnalyticsService()
