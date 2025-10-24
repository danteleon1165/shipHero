from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Retailer(db.Model):
    """Retailer entity representing EDI partners."""
    __tablename__ = 'retailers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    edi_identifier = db.Column(db.String(100), unique=True, nullable=False)
    contact_email = db.Column(db.String(200))
    contact_phone = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', back_populates='retailer', lazy='dynamic')
    
    def __repr__(self):
        return f'<Retailer {self.name} - {self.edi_identifier}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'edi_identifier': self.edi_identifier,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Product(db.Model):
    """Product entity with SKU, UPC, and inventory tracking."""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(100), unique=True, nullable=False, index=True)
    upc = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), default=0.00)
    cost = db.Column(db.Numeric(10, 2), default=0.00)
    quantity_on_hand = db.Column(db.Integer, default=0)
    quantity_reserved = db.Column(db.Integer, default=0)
    quantity_available = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order_lines = db.relationship('OrderLine', back_populates='product', lazy='dynamic')
    inventory_adjustments = db.relationship('InventoryAdjustment', back_populates='product', lazy='dynamic')
    
    def __repr__(self):
        return f'<Product {self.sku} - {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'sku': self.sku,
            'upc': self.upc,
            'name': self.name,
            'description': self.description,
            'price': float(self.price) if self.price else 0.00,
            'cost': float(self.cost) if self.cost else 0.00,
            'quantity_on_hand': self.quantity_on_hand,
            'quantity_reserved': self.quantity_reserved,
            'quantity_available': self.quantity_available,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Order(db.Model):
    """Order entity with EDI information."""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(100), unique=True, nullable=False, index=True)
    retailer_id = db.Column(db.Integer, db.ForeignKey('retailers.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, processing, shipped, completed, cancelled
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    ship_by_date = db.Column(db.DateTime)
    
    # Shipping Information
    ship_to_name = db.Column(db.String(200))
    ship_to_address1 = db.Column(db.String(300))
    ship_to_address2 = db.Column(db.String(300))
    ship_to_city = db.Column(db.String(100))
    ship_to_state = db.Column(db.String(50))
    ship_to_zip = db.Column(db.String(20))
    ship_to_country = db.Column(db.String(50))
    ship_to_phone = db.Column(db.String(50))
    
    # Totals
    subtotal = db.Column(db.Numeric(10, 2), default=0.00)
    tax_amount = db.Column(db.Numeric(10, 2), default=0.00)
    shipping_amount = db.Column(db.Numeric(10, 2), default=0.00)
    total_amount = db.Column(db.Numeric(10, 2), default=0.00)
    
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    retailer = db.relationship('Retailer', back_populates='orders')
    order_lines = db.relationship('OrderLine', back_populates='order', cascade='all, delete-orphan', lazy='dynamic')
    shipments = db.relationship('Shipment', back_populates='order', cascade='all, delete-orphan', lazy='dynamic')
    
    def __repr__(self):
        return f'<Order {self.order_number} - {self.status}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'retailer_id': self.retailer_id,
            'status': self.status,
            'order_date': self.order_date.isoformat() if self.order_date else None,
            'ship_by_date': self.ship_by_date.isoformat() if self.ship_by_date else None,
            'ship_to_name': self.ship_to_name,
            'ship_to_address1': self.ship_to_address1,
            'ship_to_address2': self.ship_to_address2,
            'ship_to_city': self.ship_to_city,
            'ship_to_state': self.ship_to_state,
            'ship_to_zip': self.ship_to_zip,
            'ship_to_country': self.ship_to_country,
            'ship_to_phone': self.ship_to_phone,
            'subtotal': float(self.subtotal) if self.subtotal else 0.00,
            'tax_amount': float(self.tax_amount) if self.tax_amount else 0.00,
            'shipping_amount': float(self.shipping_amount) if self.shipping_amount else 0.00,
            'total_amount': float(self.total_amount) if self.total_amount else 0.00,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class OrderLine(db.Model):
    """Order line items linking orders to products."""
    __tablename__ = 'order_lines'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity_ordered = db.Column(db.Integer, nullable=False)
    quantity_shipped = db.Column(db.Integer, default=0)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    line_total = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order = db.relationship('Order', back_populates='order_lines')
    product = db.relationship('Product', back_populates='order_lines')
    
    def __repr__(self):
        return f'<OrderLine Order:{self.order_id} Product:{self.product_id} Qty:{self.quantity_ordered}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity_ordered': self.quantity_ordered,
            'quantity_shipped': self.quantity_shipped,
            'unit_price': float(self.unit_price) if self.unit_price else 0.00,
            'line_total': float(self.line_total) if self.line_total else 0.00,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Shipment(db.Model):
    """Shipment tracking for orders."""
    __tablename__ = 'shipments'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    shipment_number = db.Column(db.String(100), unique=True, nullable=False, index=True)
    carrier = db.Column(db.String(100))  # UPS, FedEx, USPS, etc.
    tracking_number = db.Column(db.String(200))
    service_level = db.Column(db.String(100))  # Ground, Express, etc.
    status = db.Column(db.String(50), default='pending')  # pending, in_transit, delivered, exception
    shipped_date = db.Column(db.DateTime)
    delivered_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order = db.relationship('Order', back_populates='shipments')
    
    def __repr__(self):
        return f'<Shipment {self.shipment_number} - {self.carrier} - {self.status}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'shipment_number': self.shipment_number,
            'carrier': self.carrier,
            'tracking_number': self.tracking_number,
            'service_level': self.service_level,
            'status': self.status,
            'shipped_date': self.shipped_date.isoformat() if self.shipped_date else None,
            'delivered_date': self.delivered_date.isoformat() if self.delivered_date else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class InventoryAdjustment(db.Model):
    """Track inventory adjustments and changes."""
    __tablename__ = 'inventory_adjustments'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    adjustment_type = db.Column(db.String(50), nullable=False)  # purchase, sale, return, damage, adjustment
    quantity_change = db.Column(db.Integer, nullable=False)  # positive or negative
    previous_quantity = db.Column(db.Integer, nullable=False)
    new_quantity = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(300))
    reference_number = db.Column(db.String(100))  # PO, Order, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(100))
    
    # Relationships
    product = db.relationship('Product', back_populates='inventory_adjustments')
    
    def __repr__(self):
        return f'<InventoryAdjustment Product:{self.product_id} Type:{self.adjustment_type} Change:{self.quantity_change}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'adjustment_type': self.adjustment_type,
            'quantity_change': self.quantity_change,
            'previous_quantity': self.previous_quantity,
            'new_quantity': self.new_quantity,
            'reason': self.reason,
            'reference_number': self.reference_number,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'created_by': self.created_by
        }
