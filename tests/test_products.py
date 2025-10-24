import pytest
from app.models import db, Product


def test_create_product(client, app):
    """Test creating a new product via REST API."""
    response = client.post('/api/products', json={
        'sku': 'NEW-SKU-001',
        'name': 'New Product',
        'price': 29.99,
        'cost': 15.00,
        'quantity_on_hand': 50
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Product created successfully'
    assert data['product']['sku'] == 'NEW-SKU-001'
    assert data['product']['name'] == 'New Product'


def test_list_products(client, sample_product):
    """Test listing products."""
    response = client.get('/api/products')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'products' in data
    assert len(data['products']) > 0


def test_get_product(client, sample_product):
    """Test getting a specific product."""
    response = client.get(f'/api/products/{sample_product.id}')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['sku'] == sample_product.sku
    assert data['name'] == 'Test Product'


def test_update_product(client, sample_product):
    """Test updating a product."""
    response = client.put(f'/api/products/{sample_product.id}', json={
        'name': 'Updated Product Name',
        'price': 24.99
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Product updated successfully'
    assert data['product']['name'] == 'Updated Product Name'


def test_create_duplicate_sku(client, sample_product):
    """Test that creating a product with duplicate SKU fails."""
    response = client.post('/api/products', json={
        'sku': sample_product.sku,
        'name': 'Duplicate Product'
    })
    
    assert response.status_code == 409
    data = response.get_json()
    assert 'already exists' in data['error']
