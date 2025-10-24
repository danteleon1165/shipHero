from ariadne import QueryType, MutationType, ObjectType
from app.models import (
    db, Order, Product, Retailer, Shipment, 
    InventoryAdjustment, OrderLine
)
from datetime import datetime

query = QueryType()
mutation = MutationType()

# Object type resolvers
retailer_type = ObjectType("Retailer")
product_type = ObjectType("Product")
order_type = ObjectType("Order")
order_line_type = ObjectType("OrderLine")
shipment_type = ObjectType("Shipment")
inventory_adjustment_type = ObjectType("InventoryAdjustment")


# Query Resolvers
@query.field("orders")
def resolve_orders(obj, info, status=None, retailer_id=None, limit=20, offset=0):
    query_obj = Order.query
    
    if status:
        query_obj = query_obj.filter_by(status=status)
    if retailer_id:
        query_obj = query_obj.filter_by(retailer_id=retailer_id)
    
    query_obj = query_obj.order_by(Order.created_at.desc())
    query_obj = query_obj.limit(limit).offset(offset)
    
    return query_obj.all()


@query.field("order")
def resolve_order(obj, info, id):
    return Order.query.get(id)


@query.field("products")
def resolve_products(obj, info, sku=None, is_active=None, limit=20, offset=0):
    query_obj = Product.query
    
    if sku:
        query_obj = query_obj.filter(Product.sku.like(f'%{sku}%'))
    if is_active is not None:
        query_obj = query_obj.filter_by(is_active=is_active)
    
    query_obj = query_obj.order_by(Product.sku)
    query_obj = query_obj.limit(limit).offset(offset)
    
    return query_obj.all()


@query.field("product")
def resolve_product(obj, info, id):
    return Product.query.get(id)


@query.field("retailer")
def resolve_retailer(obj, info, id):
    return Retailer.query.get(id)


@query.field("retailers")
def resolve_retailers(obj, info, is_active=None):
    query_obj = Retailer.query
    
    if is_active is not None:
        query_obj = query_obj.filter_by(is_active=is_active)
    
    return query_obj.all()


@query.field("shipments")
def resolve_shipments(obj, info, order_id=None, status=None):
    query_obj = Shipment.query
    
    if order_id:
        query_obj = query_obj.filter_by(order_id=order_id)
    if status:
        query_obj = query_obj.filter_by(status=status)
    
    return query_obj.order_by(Shipment.created_at.desc()).all()


@query.field("inventoryAdjustments")
def resolve_inventory_adjustments(obj, info, product_id=None, adjustment_type=None):
    query_obj = InventoryAdjustment.query
    
    if product_id:
        query_obj = query_obj.filter_by(product_id=product_id)
    if adjustment_type:
        query_obj = query_obj.filter_by(adjustment_type=adjustment_type)
    
    return query_obj.order_by(InventoryAdjustment.created_at.desc()).limit(50).all()


# Mutation Resolvers
@mutation.field("updateInventory")
def resolve_update_inventory(obj, info, product_id, quantity_change, adjustment_type, 
                             reason=None, created_by="system"):
    try:
        product = Product.query.get(product_id)
        if not product:
            return {
                "success": False,
                "message": "Product not found",
                "product": None,
                "adjustment": None
            }
        
        previous_quantity = product.quantity_on_hand
        new_quantity = previous_quantity + quantity_change
        
        if new_quantity < 0:
            return {
                "success": False,
                "message": "Cannot adjust inventory below zero",
                "product": None,
                "adjustment": None
            }
        
        adjustment = InventoryAdjustment(
            product_id=product_id,
            adjustment_type=adjustment_type,
            quantity_change=quantity_change,
            previous_quantity=previous_quantity,
            new_quantity=new_quantity,
            reason=reason,
            created_by=created_by
        )
        
        product.quantity_on_hand = new_quantity
        product.quantity_available = product.quantity_on_hand - product.quantity_reserved
        product.updated_at = datetime.utcnow()
        
        db.session.add(adjustment)
        db.session.commit()
        
        return {
            "success": True,
            "message": "Inventory updated successfully",
            "product": product,
            "adjustment": adjustment
        }
    except Exception as e:
        db.session.rollback()
        return {
            "success": False,
            "message": str(e),
            "product": None,
            "adjustment": None
        }


@mutation.field("updateOrderStatus")
def resolve_update_order_status(obj, info, order_id, status):
    try:
        order = Order.query.get(order_id)
        if not order:
            return {
                "success": False,
                "message": "Order not found",
                "order": None
            }
        
        valid_statuses = ['pending', 'processing', 'shipped', 'completed', 'cancelled']
        if status not in valid_statuses:
            return {
                "success": False,
                "message": f"Invalid status. Must be one of: {valid_statuses}",
                "order": None
            }
        
        order.status = status
        order.updated_at = datetime.utcnow()
        db.session.commit()
        
        return {
            "success": True,
            "message": "Order status updated successfully",
            "order": order
        }
    except Exception as e:
        db.session.rollback()
        return {
            "success": False,
            "message": str(e),
            "order": None
        }


@mutation.field("createProduct")
def resolve_create_product(obj, info, sku, name, price=0.0, cost=0.0, quantity_on_hand=0):
    try:
        existing = Product.query.filter_by(sku=sku).first()
        if existing:
            raise ValueError("Product with this SKU already exists")
        
        product = Product(
            sku=sku,
            name=name,
            price=price,
            cost=cost,
            quantity_on_hand=quantity_on_hand,
            quantity_available=quantity_on_hand
        )
        
        db.session.add(product)
        db.session.commit()
        
        return product
    except Exception as e:
        db.session.rollback()
        raise e


@mutation.field("createRetailer")
def resolve_create_retailer(obj, info, name, edi_identifier, contact_email=None, contact_phone=None):
    try:
        existing = Retailer.query.filter_by(edi_identifier=edi_identifier).first()
        if existing:
            raise ValueError("Retailer with this EDI identifier already exists")
        
        retailer = Retailer(
            name=name,
            edi_identifier=edi_identifier,
            contact_email=contact_email,
            contact_phone=contact_phone
        )
        
        db.session.add(retailer)
        db.session.commit()
        
        return retailer
    except Exception as e:
        db.session.rollback()
        raise e


# Object field resolvers
@order_type.field("retailer")
def resolve_order_retailer(obj, info):
    return obj.retailer


@order_type.field("order_lines")
def resolve_order_lines(obj, info):
    return list(obj.order_lines)


@order_type.field("shipments")
def resolve_order_shipments(obj, info):
    return list(obj.shipments)


@order_line_type.field("product")
def resolve_order_line_product(obj, info):
    return obj.product


@inventory_adjustment_type.field("product")
def resolve_inventory_adjustment_product(obj, info):
    return obj.product
