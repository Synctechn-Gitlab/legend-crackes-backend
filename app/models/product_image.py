from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    image_url = Column(String(500), nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)

    # Relationship
    product = relationship("Product", back_populates="images")

    def __repr__(self):
        return f"<ProductImage id={self.id} product_id={self.product_id} sort_order={self.sort_order}>"
