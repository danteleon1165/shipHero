from flask import Blueprint, request, jsonify
from app.models import db, Shipment, Order
from datetime import datetime

shipments_bp = Blueprint('shipments', __name__)


@shipments_bp.route('/shipments', methods=['POST'])
def create_shipment():
    """Create a new shipment for an order."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['order_id', 'shipment_number', 'carrier']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Verify order exists
        order = Order.query.get(data['order_id'])
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        # Check if shipment number already exists
        existing_shipment = Shipment.query.filter_by(
            shipment_number=data['shipment_number']
        ).first()
        
        if existing_shipment:
            return jsonify({'error': 'Shipment with this number already exists'}), 409
        
        # Create shipment
        shipment = Shipment(
            order_id=data['order_id'],
            shipment_number=data['shipment_number'],
            carrier=data['carrier'],
            tracking_number=data.get('tracking_number'),
            service_level=data.get('service_level'),
            status=data.get('status', 'pending'),
            shipped_date=datetime.fromisoformat(data['shipped_date']) if data.get('shipped_date') else None,
            notes=data.get('notes')
        )
        
        db.session.add(shipment)
        
        # Update order status if appropriate
        if shipment.status == 'in_transit' and order.status == 'pending':
            order.status = 'shipped'
            order.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Shipment created successfully',
            'shipment': shipment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@shipments_bp.route('/shipments', methods=['GET'])
def list_shipments():
    """List all shipments with optional filtering."""
    try:
        # Query parameters
        order_id = request.args.get('order_id', type=int)
        status = request.args.get('status')
        carrier = request.args.get('carrier')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Build query
        query = Shipment.query
        
        if order_id:
            query = query.filter_by(order_id=order_id)
        if status:
            query = query.filter_by(status=status)
        if carrier:
            query = query.filter_by(carrier=carrier)
        
        # Paginate
        query = query.order_by(Shipment.created_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        shipments = [shipment.to_dict() for shipment in pagination.items]
        
        return jsonify({
            'shipments': shipments,
            'total': pagination.total,
            'page': pagination.page,
            'per_page': pagination.per_page,
            'pages': pagination.pages
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@shipments_bp.route('/shipments/<int:shipment_id>', methods=['GET'])
def get_shipment(shipment_id):
    """Get detailed information about a specific shipment."""
    try:
        shipment = Shipment.query.get_or_404(shipment_id)
        
        shipment_data = shipment.to_dict()
        shipment_data['order'] = shipment.order.to_dict() if shipment.order else None
        
        return jsonify(shipment_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@shipments_bp.route('/shipments/<int:shipment_id>', methods=['PUT'])
def update_shipment(shipment_id):
    """Update shipment status or tracking information."""
    try:
        shipment = Shipment.query.get_or_404(shipment_id)
        data = request.get_json()
        
        # Update allowed fields
        if 'status' in data:
            shipment.status = data['status']
            
            # Update order status if shipment is delivered
            if data['status'] == 'delivered':
                order = shipment.order
                # Check if all shipments for this order are delivered
                all_delivered = all(
                    s.status == 'delivered' for s in order.shipments
                )
                if all_delivered:
                    order.status = 'completed'
                    order.updated_at = datetime.utcnow()
        
        if 'tracking_number' in data:
            shipment.tracking_number = data['tracking_number']
        if 'delivered_date' in data:
            shipment.delivered_date = datetime.fromisoformat(data['delivered_date'])
        if 'notes' in data:
            shipment.notes = data['notes']
        
        shipment.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Shipment updated successfully',
            'shipment': shipment.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
