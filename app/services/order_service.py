from app.models import db, Order, OrderLine, Product
from datetime import datetime


class OrderService:
    """Service for handling order operations."""
    
    @staticmethod
    def create_order_from_edi(data, retailer):
        """Create an order from EDI data."""
        # Create order
        order = Order(
            order_number=data['order_number'],
            retailer_id=retailer.id,
            status='pending',
            order_date=datetime.fromisoformat(data['order_date']) if data.get('order_date') else datetime.utcnow(),
            ship_by_date=datetime.fromisoformat(data['ship_by_date']) if data.get('ship_by_date') else None,
            ship_to_name=data.get('ship_to_name'),
            ship_to_address1=data.get('ship_to_address1'),
            ship_to_address2=data.get('ship_to_address2'),
            ship_to_city=data.get('ship_to_city'),
            ship_to_state=data.get('ship_to_state'),
            ship_to_zip=data.get('ship_to_zip'),
            ship_to_country=data.get('ship_to_country', 'USA'),
            ship_to_phone=data.get('ship_to_phone'),
            notes=data.get('notes')
        )
        
        db.session.add(order)
        db.session.flush()  # Get order.id
        
        # Create order lines
        subtotal = 0
        for line_data in data['order_lines']:
            # Find product by SKU
            product = Product.query.filter_by(sku=line_data['sku']).first()
            if not product:
                raise ValueError(f"Product with SKU {line_data['sku']} not found")
            
            quantity = int(line_data['quantity'])
            unit_price = float(line_data.get('unit_price', product.price))
            line_total = quantity * unit_price
            
            order_line = OrderLine(
                order_id=order.id,
                product_id=product.id,
                quantity_ordered=quantity,
                quantity_shipped=0,
                unit_price=unit_price,
                line_total=line_total
            )
            
            db.session.add(order_line)
            subtotal += line_total
            
            # Reserve inventory
            product.quantity_reserved += quantity
            product.quantity_available = product.quantity_on_hand - product.quantity_reserved
        
        # Calculate totals
        order.subtotal = subtotal
        order.tax_amount = float(data.get('tax_amount', 0))
        order.shipping_amount = float(data.get('shipping_amount', 0))
        order.total_amount = order.subtotal + order.tax_amount + order.shipping_amount
        
        db.session.commit()
        return order
    
    @staticmethod
    def cancel_order(order_id):
        """Cancel an order and release reserved inventory."""
        order = Order.query.get(order_id)
        if not order:
            raise ValueError("Order not found")
        
        if order.status in ['shipped', 'completed']:
            raise ValueError("Cannot cancel shipped or completed orders")
        
        # Release reserved inventory
        for line in order.order_lines:
            product = line.product
            product.quantity_reserved -= line.quantity_ordered
            product.quantity_available = product.quantity_on_hand - product.quantity_reserved
        
        order.status = 'cancelled'
        order.updated_at = datetime.utcnow()
        db.session.commit()
        
        return order
