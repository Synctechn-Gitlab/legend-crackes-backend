import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.database import Base, get_db
from app.core.security import hash_password, create_access_token
from app.models.admin_user import AdminUser
from app.models.category import Category
from app.models.product import Product
from app.main import app

# Use StaticPool so all connection checkouts share the single in-memory database
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    
    # Create test admin
    test_admin = AdminUser(
        id=1,
        username="testadmin",
        email="testadmin@sivakasi.com",
        password_hash=hash_password("testpass123"),
        is_active=True
    )
    db.add(test_admin)

    # Create test categories
    cat1 = Category(id=1, name="Sparklers", slug="sparklers", description="Test sparklers")
    cat2 = Category(id=2, name="Sky Shots", slug="sky-shots", description="Test sky shots")
    db.add_all([cat1, cat2])
    db.flush()

    # Create test products
    p1 = Product(
        id=1,
        product_code="TST-101",
        name="10cm Gold Sparkler",
        slug="10cm-gold-sparkler",
        category_id=1,
        description="Golden handheld sparks",
        original_price=100.0,
        selling_price=60.0,
        discount_percentage=40,
        stock_quantity=50,
        unit="Box",
        is_featured=True,
        is_active=True
    )
    p2 = Product(
        id=2,
        product_code="TST-102",
        name="12 Shots Sky Bloom",
        slug="12-shots-sky-bloom",
        category_id=2,
        description="12 aerial multi-colour shells",
        original_price=1200.0,
        selling_price=650.0,
        discount_percentage=46,
        stock_quantity=10,
        unit="Box",
        is_featured=False,
        is_active=True
    )
    db.add_all([p1, p2])
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def admin_headers():
    token = create_access_token(subject=1)
    return {"Authorization": f"Bearer {token}"}
