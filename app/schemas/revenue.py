from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict


class RevenuePeriodTrend(BaseModel):
    period: str
    revenue: float
    orders: int


class CategorySalesItem(BaseModel):
    category: str
    name: Optional[str] = None
    amount: float
    sales: Optional[float] = None
    percentage: float
    share: Optional[float] = None
    color: Optional[str] = None


class TopProductItem(BaseModel):
    id: int
    name: str
    code: str
    category: str
    units_sold: int
    selling_price: float
    total_revenue: float
    unitsSold: Optional[int] = None
    sellingPrice: Optional[float] = None
    totalRevenue: Optional[float] = None


class RevenueAnalyticsResponse(BaseModel):
    revenue: float
    order_count: int
    average_order_value: float
    time_range: str
    total_profit: Optional[float] = 0.0
    total_cost: Optional[float] = 0.0
    daily_revenue: Optional[float] = 0.0
    weekly_revenue: Optional[float] = 0.0
    monthly_revenue: Optional[float] = 0.0
    revenue_growth: Optional[str] = "Live Metrics"
    monthly_trend: List[Dict[str, Any]] = []
    sales_by_category: List[Dict[str, Any]] = []
    top_selling_products: List[Dict[str, Any]] = []

    # Frontend camelCase aliases
    totalRevenue: Optional[float] = None
    totalProfit: Optional[float] = None
    totalCost: Optional[float] = None
    orderCount: Optional[int] = None
    averageOrderValue: Optional[float] = None
    dailyRevenue: Optional[float] = None
    weeklyRevenue: Optional[float] = None
    monthlyRevenue: Optional[float] = None
    revenueGrowth: Optional[str] = None
    monthlyTrend: Optional[List[Dict[str, Any]]] = None
    salesByCategory: Optional[List[Dict[str, Any]]] = None
    topSellingProducts: Optional[List[Dict[str, Any]]] = None

    model_config = ConfigDict(from_attributes=True)
