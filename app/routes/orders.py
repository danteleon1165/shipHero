from flask import Blueprint, request, jsonify
from app.models import db, Order, OrderLine, Product, Retailer
from app.services.order_service import OrderService
from datetime import datetime

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/sps/orders', methods=['POST'])
def receive_sps_order():
    """Simulate receiving an EDI order from SPS Commerce."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['order_number', 'retailer_edi_identifier', 'order_lines']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Find or create retailer
        retailer = Retailer.query.filter_by(
            edi_identifier=data['retailer_edi_identifier']
        ).first()
        
        if not retailer:
            return jsonify({'error': 'Retailer not found'}), 404
        
        # Check if order already exists
        existing_order = Order.query.filter_by(
            order_number=data['order_number']
        ).first()
        
        if existing_order:
            return jsonify({'error': 'Order already exists'}), 409
        
        # Create order using service
        order = OrderService.create_order_from_edi(data, retailer)
        
        return jsonify({
            'message': 'Order received successfully',
            'order': order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@orders_bp.route('/orders', methods=['GET'])
def list_orders():
    """List all orders with optional filtering."""
    try:
        # Query parameters
        status = request.args.get('status')
        retailer_id = request.args.get('retailer_id', type=int)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Build query
        query = Order.query
        
        if status:
            query = query.filter_by(status=status)
        if retailer_id:
            query = query.filter_by(retailer_id=retailer_id)
        
        # Paginate
        query = query.order_by(Order.created_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        orders = [order.to_dict() for order in pagination.items]
        
        return jsonify({
            'orders': orders,
            'total': pagination.total,
            'page': pagination.page,
            'per_page': pagination.per_page,
            'pages': pagination.pages
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get detailed information about a specific order."""
    try:
        order = Order.query.get_or_404(order_id)
        
        # Get order details with lines and shipments
        order_data = order.to_dict()
        order_data['order_lines'] = [line.to_dict() for line in order.order_lines]
        order_data['shipments'] = [shipment.to_dict() for shipment in order.shipments]
        order_data['retailer'] = order.retailer.to_dict() if order.retailer else None
        
        return jsonify(order_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orders_bp.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """Update order status or information."""
    try:
        order = Order.query.get_or_404(order_id)
        data = request.get_json()
        
        # Update allowed fields
        if 'status' in data:
            order.status = data['status']
        if 'notes' in data:
            order.notes = data['notes']
        
        order.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Order updated successfully',
            'order': order.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
