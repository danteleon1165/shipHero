"""
Seed script to populate the database with sample data for testing.
"""
import os
os.environ['FLASK_ENV'] = 'testing'

from app import create_app
from app.models import db, Retailer, Product, Order, OrderLine, Shipment
from datetime import datetime, timedelta

app = create_app('testing')

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()
    
    print("Creating sample retailers...")
    retailers = [
        Retailer(
            name='Walmart',
            edi_identifier='WALMART001',
            contact_email='edi@walmart.com',
            contact_phone='555-0001'
        ),
        Retailer(
            name='Target',
            edi_identifier='TARGET001',
            contact_email='edi@target.com',
            contact_phone='555-0002'
        ),
        Retailer(
            name='Amazon',
            edi_identifier='AMAZON001',
            contact_email='edi@amazon.com',
            contact_phone='555-0003'
        ),
    ]
    db.session.add_all(retailers)
    db.session.commit()
    print(f"✓ Created {len(retailers)} retailers")
    
    print("Creating sample products...")
    products = [
        Product(
            sku='WIDGET-001',
            upc='123456789001',
            name='Premium Widget',
            description='High-quality widget for all purposes',
            price=29.99,
            cost=15.00,
            quantity_on_hand=500,
            quantity_reserved=0,
            quantity_available=500
        ),
        Product(
            sku='GADGET-002',
            upc='123456789002',
            name='Smart Gadget',
            description='IoT-enabled smart gadget',
            price=49.99,
            cost=25.00,
            quantity_on_hand=300,
            quantity_reserved=0,
            quantity_available=300
        ),
        Product(
            sku='TOOL-003',
            upc='123456789003',
            name='Multi-Tool Set',
            description='Complete tool set for professionals',
            price=89.99,
            cost=45.00,
            quantity_on_hand=150,
            quantity_reserved=0,
            quantity_available=150
        ),
        Product(
            sku='GIZMO-004',
            upc='123456789004',
            name='Portable Gizmo',
            description='Compact and portable gizmo',
            price=19.99,
            cost=8.00,
            quantity_on_hand=1000,
            quantity_reserved=0,
            quantity_available=1000
        ),
    ]
    db.session.add_all(products)
    db.session.commit()
    print(f"✓ Created {len(products)} products")
    
    print("Creating sample orders...")
    # Order 1
    order1 = Order(
        order_number='WMT-20240115-001',
        retailer_id=retailers[0].id,
        status='pending',
        order_date=datetime.utcnow() - timedelta(days=2),
        ship_by_date=datetime.utcnow() + timedelta(days=3),
        ship_to_name='John Smith',
        ship_to_address1='123 Main Street',
        ship_to_city='Springfield',
        ship_to_state='IL',
        ship_to_zip='62701',
        ship_to_country='USA',
        subtotal=59.98,
        tax_amount=4.80,
        shipping_amount=9.99,
        total_amount=74.77
    )
    db.session.add(order1)
    db.session.flush()
    
    order1_lines = [
        OrderLine(
            order_id=order1.id,
            product_id=products[0].id,
            quantity_ordered=2,
            unit_price=29.99,
            line_total=59.98
        )
    ]
    db.session.add_all(order1_lines)
    
    # Order 2
    order2 = Order(
        order_number='TGT-20240116-001',
        retailer_id=retailers[1].id,
        status='processing',
        order_date=datetime.utcnow() - timedelta(days=1),
        ship_by_date=datetime.utcnow() + timedelta(days=2),
        ship_to_name='Jane Doe',
        ship_to_address1='456 Oak Avenue',
        ship_to_city='Portland',
        ship_to_state='OR',
        ship_to_zip='97201',
        ship_to_country='USA',
        subtotal=139.97,
        tax_amount=11.20,
        shipping_amount=12.99,
        total_amount=164.16
    )
    db.session.add(order2)
    db.session.flush()
    
    order2_lines = [
        OrderLine(
            order_id=order2.id,
            product_id=products[1].id,
            quantity_ordered=1,
            unit_price=49.99,
            line_total=49.99
        ),
        OrderLine(
            order_id=order2.id,
            product_id=products[2].id,
            quantity_ordered=1,
            unit_price=89.99,
            line_total=89.99
        )
    ]
    db.session.add_all(order2_lines)
    
    # Order 3
    order3 = Order(
        order_number='AMZ-20240117-001',
        retailer_id=retailers[2].id,
        status='shipped',
        order_date=datetime.utcnow() - timedelta(hours=12),
        ship_by_date=datetime.utcnow() + timedelta(days=1),
        ship_to_name='Bob Johnson',
        ship_to_address1='789 Pine Street',
        ship_to_address2='Apt 4B',
        ship_to_city='Austin',
        ship_to_state='TX',
        ship_to_zip='78701',
        ship_to_country='USA',
        subtotal=99.95,
        tax_amount=8.00,
        shipping_amount=0.00,
        total_amount=107.95
    )
    db.session.add(order3)
    db.session.flush()
    
    order3_lines = [
        OrderLine(
            order_id=order3.id,
            product_id=products[3].id,
            quantity_ordered=5,
            unit_price=19.99,
            line_total=99.95
        )
    ]
    db.session.add_all(order3_lines)
    
    db.session.commit()
    print(f"✓ Created 3 orders with line items")
    
    print("Creating sample shipments...")
    shipment1 = Shipment(
        order_id=order3.id,
        shipment_number='SHIP-20240117-001',
        carrier='UPS',
        tracking_number='1Z999AA10123456789',
        service_level='Ground',
        status='in_transit',
        shipped_date=datetime.utcnow() - timedelta(hours=6)
    )
    db.session.add(shipment1)
    db.session.commit()
    print(f"✓ Created 1 shipment")
    
    print("\n" + "="*50)
    print("✓ Database seeded successfully!")
    print("="*50)
    print(f"\nRetailers: {Retailer.query.count()}")
    print(f"Products: {Product.query.count()}")
    print(f"Orders: {Order.query.count()}")
    print(f"Order Lines: {OrderLine.query.count()}")
    print(f"Shipments: {Shipment.query.count()}")
    print("\n" + "="*50)
    print("You can now start the application with: python run_dev.py")
    print("="*50)
