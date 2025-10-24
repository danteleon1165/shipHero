import pytest
from app.models import db, Shipment


def test_create_shipment(client, sample_order):
    """Test creating a new shipment."""
    response = client.post('/api/shipments', json={
        'order_id': sample_order.id,
        'shipment_number': 'SHIP-001',
        'carrier': 'UPS',
        'tracking_number': '1Z999AA10123456784',
        'service_level': 'Ground',
        'status': 'pending'
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Shipment created successfully'
    assert data['shipment']['shipment_number'] == 'SHIP-001'
    assert data['shipment']['carrier'] == 'UPS'


def test_list_shipments(client, app, sample_order):
    """Test listing shipments."""
    # Create a shipment first
    with app.app_context():
        shipment = Shipment(
            order_id=sample_order.id,
            shipment_number='SHIP-002',
            carrier='FedEx',
            status='in_transit'
        )
        db.session.add(shipment)
        db.session.commit()
    
    response = client.get('/api/shipments')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'shipments' in data
    assert len(data['shipments']) > 0


def test_get_shipment(client, app, sample_order):
    """Test getting a specific shipment."""
    # Create a shipment first
    with app.app_context():
        shipment = Shipment(
            order_id=sample_order.id,
            shipment_number='SHIP-003',
            carrier='USPS',
            status='pending'
        )
        db.session.add(shipment)
        db.session.commit()
        shipment_id = shipment.id
    
    response = client.get(f'/api/shipments/{shipment_id}')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['shipment_number'] == 'SHIP-003'
    assert 'order' in data


def test_update_shipment_status(client, app, sample_order):
    """Test updating shipment status."""
    # Create a shipment first
    with app.app_context():
        shipment = Shipment(
            order_id=sample_order.id,
            shipment_number='SHIP-004',
            carrier='UPS',
            status='pending'
        )
        db.session.add(shipment)
        db.session.commit()
        shipment_id = shipment.id
    
    response = client.put(f'/api/shipments/{shipment_id}', json={
        'status': 'in_transit',
        'tracking_number': '1Z999AA10123456785'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Shipment updated successfully'
    assert data['shipment']['status'] == 'in_transit'


def test_filter_shipments_by_order(client, app, sample_order):
    """Test filtering shipments by order ID."""
    # Create shipments for the order
    with app.app_context():
        shipment = Shipment(
            order_id=sample_order.id,
            shipment_number='SHIP-005',
            carrier='FedEx',
            status='pending'
        )
        db.session.add(shipment)
        db.session.commit()
    
    response = client.get(f'/api/shipments?order_id={sample_order.id}')
    
    assert response.status_code == 200
    data = response.get_json()
    assert all(s['order_id'] == sample_order.id for s in data['shipments'])
