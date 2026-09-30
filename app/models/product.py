from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_code = Column(String(60), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    tamil_name = Column(String(255), nullable=True, index=True)
    slug = Column(String(280), unique=True, nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    original_price = Column(Numeric(10, 2), nullable=False)
    selling_price = Column(Numeric(10, 2), nullable=False)
    my_price = Column(Numeric(10, 2), nullable=True, default=0.0)
    discount_percentage = Column(Integer, default=0, nullable=False)
    stock_quantity = Column(Integer, default=0, nullable=False)
    unit = Column(String(50), default="Box", nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    category = relationship("Category", back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan", order_by="ProductImage.sort_order")
    order_items = relationship("OrderItem", back_populates="product")

    # Composite & Single Indexes for query performance across 3000+ products
    __table_args__ = (
        Index("ix_products_cat_active", "category_id", "is_active"),
        Index("ix_products_selling_price", "selling_price"),
        Index("ix_products_active_featured", "is_active", "is_featured"),
    )

    def __repr__(self):
        return f"<Product id={self.id} code='{self.product_code}' name='{self.name}' stock={self.stock_quantity}>"
