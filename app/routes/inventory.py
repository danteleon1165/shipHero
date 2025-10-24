from flask import Blueprint, request, jsonify
from app.models import db, Product, InventoryAdjustment
from datetime import datetime

inventory_bp = Blueprint('inventory', __name__)


@inventory_bp.route('/inventory/adjust', methods=['POST'])
def adjust_inventory():
    """Adjust inventory for a product."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['product_id', 'adjustment_type', 'quantity_change']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get product
        product = Product.query.get(data['product_id'])
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Validate adjustment type
        valid_types = ['purchase', 'sale', 'return', 'damage', 'adjustment']
        if data['adjustment_type'] not in valid_types:
            return jsonify({'error': f'Invalid adjustment type. Must be one of: {valid_types}'}), 400
        
        quantity_change = int(data['quantity_change'])
        previous_quantity = product.quantity_on_hand
        new_quantity = previous_quantity + quantity_change
        
        # Prevent negative inventory
        if new_quantity < 0:
            return jsonify({'error': 'Cannot adjust inventory below zero'}), 400
        
        # Create adjustment record
        adjustment = InventoryAdjustment(
            product_id=product.id,
            adjustment_type=data['adjustment_type'],
            quantity_change=quantity_change,
            previous_quantity=previous_quantity,
            new_quantity=new_quantity,
            reason=data.get('reason'),
            reference_number=data.get('reference_number'),
            created_by=data.get('created_by', 'system')
        )
        
        # Update product inventory
        product.quantity_on_hand = new_quantity
        product.quantity_available = product.quantity_on_hand - product.quantity_reserved
        product.updated_at = datetime.utcnow()
        
        db.session.add(adjustment)
        db.session.commit()
        
        return jsonify({
            'message': 'Inventory adjusted successfully',
            'adjustment': adjustment.to_dict(),
            'product': product.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@inventory_bp.route('/inventory/product/<int:product_id>', methods=['GET'])
def get_product_inventory(product_id):
    """Get inventory details for a product."""
    try:
        product = Product.query.get_or_404(product_id)
        
        # Get recent adjustments
        recent_adjustments = InventoryAdjustment.query.filter_by(
            product_id=product_id
        ).order_by(InventoryAdjustment.created_at.desc()).limit(10).all()
        
        return jsonify({
            'product': product.to_dict(),
            'recent_adjustments': [adj.to_dict() for adj in recent_adjustments]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@inventory_bp.route('/inventory/adjustments', methods=['GET'])
def list_adjustments():
    """List inventory adjustments with optional filtering."""
    try:
        # Query parameters
        product_id = request.args.get('product_id', type=int)
        adjustment_type = request.args.get('adjustment_type')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Build query
        query = InventoryAdjustment.query
        
        if product_id:
            query = query.filter_by(product_id=product_id)
        if adjustment_type:
            query = query.filter_by(adjustment_type=adjustment_type)
        
        # Paginate
        query = query.order_by(InventoryAdjustment.created_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        adjustments = [adj.to_dict() for adj in pagination.items]
        
        return jsonify({
            'adjustments': adjustments,
            'total': pagination.total,
            'page': pagination.page,
            'per_page': pagination.per_page,
            'pages': pagination.pages
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
