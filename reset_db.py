import sys
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, Base, engine
from app.core.security import hash_password
from app.core.logging import logger
from app.models.admin_user import AdminUser
from app.models.order import OrderItem, Order
from app.models.product import Product
from app.models.product_image import ProductImage
from app.models.category import Category


def clear_mock_data():
    logger.info("Connecting to database to clear mock data...")
    db: Session = SessionLocal()
    try:
        # Delete dependent child tables first
        num_items = db.query(OrderItem).delete()
        num_images = db.query(ProductImage).delete()
        num_orders = db.query(Order).delete()
        num_products = db.query(Product).delete()
        num_categories = db.query(Category).delete()

        db.commit()
        logger.info(f"Deleted {num_items} OrderItems, {num_images} ProductImages, {num_orders} Orders, {num_products} Products, {num_categories} Categories.")

        # Ensure Super Admin exists
        admin = db.query(AdminUser).filter(AdminUser.username == "admin").first()
        if not admin:
            admin = AdminUser(
                username="admin",
                email="admin@sivakasicrackers.com",
                password_hash=hash_password("admin123"),
                is_active=True
            )
            db.add(admin)
            db.commit()
            logger.info("Created default Admin User (admin / admin123).")
        else:
            logger.info("Preserved default Admin User (admin).")

        logger.info("Database successfully reset! All mock products, orders, categories, inventory, and revenue data cleared.")

    except Exception as e:
        db.rollback()
        logger.error(f"Error clearing database: {str(e)}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    clear_mock_data()
