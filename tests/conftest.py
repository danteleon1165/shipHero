import pytest
from app import create_app
from app.models import db, Retailer, Product, Order, OrderLine, Shipment


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def sample_retailer(app):
    """Create a sample retailer for testing."""
    with app.app_context():
        retailer = Retailer(
            name='Test Retailer',
            edi_identifier='TEST001',
            contact_email='test@retailer.com',
            contact_phone='555-1234'
        )
        db.session.add(retailer)
        db.session.commit()
        return retailer


@pytest.fixture
def sample_product(app):
    """Create a sample product for testing."""
    with app.app_context():
        product = Product(
            sku='TEST-SKU-001',
            upc='123456789012',
            name='Test Product',
            description='A test product',
            price=19.99,
            cost=10.00,
            quantity_on_hand=100,
            quantity_reserved=0,
            quantity_available=100
        )
        db.session.add(product)
        db.session.commit()
        return product


@pytest.fixture
def sample_order(app, sample_retailer, sample_product):
    """Create a sample order for testing."""
    with app.app_context():
        order = Order(
            order_number='ORD-001',
            retailer_id=sample_retailer.id,
            status='pending',
            ship_to_name='John Doe',
            ship_to_address1='123 Main St',
            ship_to_city='Anytown',
            ship_to_state='CA',
            ship_to_zip='12345',
            subtotal=19.99,
            total_amount=19.99
        )
        db.session.add(order)
        db.session.flush()
        
        order_line = OrderLine(
            order_id=order.id,
            product_id=sample_product.id,
            quantity_ordered=1,
            unit_price=19.99,
            line_total=19.99
        )
        db.session.add(order_line)
        db.session.commit()
        return order
