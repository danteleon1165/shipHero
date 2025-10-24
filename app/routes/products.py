from flask import Blueprint, request, jsonify
from app.models import db, Product
from datetime import datetime

products_bp = Blueprint('products', __name__)


@products_bp.route('/products', methods=['GET'])
def list_products():
    """List all products with optional filtering."""
    try:
        # Query parameters
        sku = request.args.get('sku')
        is_active = request.args.get('is_active', type=bool)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Build query
        query = Product.query
        
        if sku:
            query = query.filter(Product.sku.like(f'%{sku}%'))
        if is_active is not None:
            query = query.filter_by(is_active=is_active)
        
        # Paginate
        query = query.order_by(Product.sku)
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        products = [product.to_dict() for product in pagination.items]
        
        return jsonify({
            'products': products,
            'total': pagination.total,
            'page': pagination.page,
            'per_page': pagination.per_page,
            'pages': pagination.pages
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get detailed information about a specific product."""
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify(product.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products_bp.route('/products', methods=['POST'])
def create_product():
    """Create a new product."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['sku', 'name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if product with SKU already exists
        existing_product = Product.query.filter_by(sku=data['sku']).first()
        if existing_product:
            return jsonify({'error': 'Product with this SKU already exists'}), 409
        
        # Create new product
        product = Product(
            sku=data['sku'],
            upc=data.get('upc'),
            name=data['name'],
            description=data.get('description'),
            price=data.get('price', 0.00),
            cost=data.get('cost', 0.00),
            quantity_on_hand=data.get('quantity_on_hand', 0),
            quantity_reserved=data.get('quantity_reserved', 0),
            quantity_available=data.get('quantity_available', 0),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'message': 'Product created successfully',
            'product': product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@products_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update product information."""
    try:
        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        
        # Update allowed fields
        updateable_fields = [
            'name', 'description', 'price', 'cost', 
            'upc', 'is_active'
        ]
        
        for field in updateable_fields:
            if field in data:
                setattr(product, field, data[field])
        
        product.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Product updated successfully',
            'product': product.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
