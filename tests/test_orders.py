import pytest
from app.models import db, Order


def test_list_orders(client, sample_order):
    """Test listing orders."""
    response = client.get('/api/orders')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'orders' in data
    assert len(data['orders']) > 0


def test_get_order(client, sample_order):
    """Test getting a specific order with details."""
    response = client.get(f'/api/orders/{sample_order.id}')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['order_number'] == sample_order.order_number
    assert 'order_lines' in data
    assert len(data['order_lines']) > 0


def test_update_order_status(client, sample_order):
    """Test updating order status."""
    response = client.put(f'/api/orders/{sample_order.id}', json={
        'status': 'processing'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Order updated successfully'
    assert data['order']['status'] == 'processing'


def test_receive_sps_order(client, sample_retailer, sample_product):
    """Test receiving an EDI order from SPS Commerce."""
    response = client.post('/api/sps/orders', json={
        'order_number': 'SPS-ORD-001',
        'retailer_edi_identifier': sample_retailer.edi_identifier,
        'order_date': '2024-01-15T10:00:00',
        'ship_to_name': 'Jane Smith',
        'ship_to_address1': '456 Oak Ave',
        'ship_to_city': 'Springfield',
        'ship_to_state': 'IL',
        'ship_to_zip': '62701',
        'order_lines': [
            {
                'sku': sample_product.sku,
                'quantity': 2,
                'unit_price': 19.99
            }
        ]
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Order received successfully'
    assert data['order']['order_number'] == 'SPS-ORD-001'


def test_receive_duplicate_order(client, sample_order, sample_retailer, sample_product):
    """Test that receiving a duplicate order fails."""
    response = client.post('/api/sps/orders', json={
        'order_number': sample_order.order_number,
        'retailer_edi_identifier': sample_retailer.edi_identifier,
        'order_lines': [
            {
                'sku': sample_product.sku,
                'quantity': 1
            }
        ]
    })
    
    assert response.status_code == 409
    data = response.get_json()
    assert 'already exists' in data['error']


def test_filter_orders_by_status(client, sample_order):
    """Test filtering orders by status."""
    response = client.get('/api/orders?status=pending')
    
    assert response.status_code == 200
    data = response.get_json()
    assert all(order['status'] == 'pending' for order in data['orders'])
