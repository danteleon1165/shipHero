import pytest
from app.models import db, Product, InventoryAdjustment


def test_adjust_inventory(client, sample_product):
    """Test adjusting product inventory."""
    response = client.post('/api/inventory/adjust', json={
        'product_id': sample_product.id,
        'adjustment_type': 'purchase',
        'quantity_change': 50,
        'reason': 'Received new stock',
        'reference_number': 'PO-001',
        'created_by': 'admin'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Inventory adjusted successfully'
    assert data['product']['quantity_on_hand'] == 150  # 100 + 50


def test_adjust_inventory_negative(client, sample_product):
    """Test decreasing inventory."""
    response = client.post('/api/inventory/adjust', json={
        'product_id': sample_product.id,
        'adjustment_type': 'sale',
        'quantity_change': -10,
        'reason': 'Sale',
        'created_by': 'system'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['product']['quantity_on_hand'] == 90  # 100 - 10


def test_adjust_inventory_below_zero(client, sample_product):
    """Test that inventory cannot go below zero."""
    response = client.post('/api/inventory/adjust', json={
        'product_id': sample_product.id,
        'adjustment_type': 'damage',
        'quantity_change': -150,
        'reason': 'Damaged goods'
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'below zero' in data['error']


def test_get_product_inventory(client, app, sample_product):
    """Test getting product inventory details."""
    # Create an adjustment first
    with app.app_context():
        adjustment = InventoryAdjustment(
            product_id=sample_product.id,
            adjustment_type='adjustment',
            quantity_change=10,
            previous_quantity=100,
            new_quantity=110,
            reason='Stock count adjustment'
        )
        db.session.add(adjustment)
        db.session.commit()
    
    response = client.get(f'/api/inventory/product/{sample_product.id}')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'product' in data
    assert 'recent_adjustments' in data
    assert len(data['recent_adjustments']) > 0


def test_list_adjustments(client, app, sample_product):
    """Test listing inventory adjustments."""
    # Create adjustments first
    with app.app_context():
        adjustment1 = InventoryAdjustment(
            product_id=sample_product.id,
            adjustment_type='purchase',
            quantity_change=20,
            previous_quantity=100,
            new_quantity=120
        )
        adjustment2 = InventoryAdjustment(
            product_id=sample_product.id,
            adjustment_type='sale',
            quantity_change=-5,
            previous_quantity=120,
            new_quantity=115
        )
        db.session.add_all([adjustment1, adjustment2])
        db.session.commit()
    
    response = client.get(f'/api/inventory/adjustments?product_id={sample_product.id}')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'adjustments' in data
    assert len(data['adjustments']) > 0


def test_invalid_adjustment_type(client, sample_product):
    """Test that invalid adjustment type fails."""
    response = client.post('/api/inventory/adjust', json={
        'product_id': sample_product.id,
        'adjustment_type': 'invalid_type',
        'quantity_change': 10
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'Invalid adjustment type' in data['error']
