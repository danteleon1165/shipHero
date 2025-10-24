import pytest
from app.models import db, Retailer, Product


def test_graphql_query_products(client, sample_product):
    """Test GraphQL query for products."""
    query = """
        query {
            products(limit: 10) {
                id
                sku
                name
                price
                quantity_on_hand
            }
        }
    """
    
    response = client.post('/graphql', json={'query': query})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'products' in data['data']
    assert len(data['data']['products']) > 0


def test_graphql_query_orders(client, sample_order):
    """Test GraphQL query for orders."""
    query = """
        query {
            orders(limit: 10) {
                id
                order_number
                status
                total_amount
            }
        }
    """
    
    response = client.post('/graphql', json={'query': query})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'orders' in data['data']
    assert len(data['data']['orders']) > 0


def test_graphql_mutation_create_product(client):
    """Test GraphQL mutation to create a product."""
    mutation = """
        mutation {
            createProduct(
                sku: "GQL-SKU-001",
                name: "GraphQL Product",
                price: 39.99,
                cost: 20.00,
                quantity_on_hand: 75
            ) {
                id
                sku
                name
                price
            }
        }
    """
    
    response = client.post('/graphql', json={'query': mutation})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'createProduct' in data['data']
    assert data['data']['createProduct']['sku'] == 'GQL-SKU-001'


def test_graphql_mutation_update_inventory(client, sample_product):
    """Test GraphQL mutation to update inventory."""
    mutation = f"""
        mutation {{
            updateInventory(
                product_id: {sample_product.id},
                quantity_change: 25,
                adjustment_type: "purchase",
                reason: "New stock arrival",
                created_by: "graphql_user"
            ) {{
                success
                message
                product {{
                    id
                    quantity_on_hand
                }}
            }}
        }}
    """
    
    response = client.post('/graphql', json={'query': mutation})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert data['data']['updateInventory']['success'] == True
    assert data['data']['updateInventory']['product']['quantity_on_hand'] == 125


def test_graphql_mutation_update_order_status(client, sample_order):
    """Test GraphQL mutation to update order status."""
    mutation = f"""
        mutation {{
            updateOrderStatus(
                order_id: {sample_order.id},
                status: "processing"
            ) {{
                success
                message
                order {{
                    id
                    status
                }}
            }}
        }}
    """
    
    response = client.post('/graphql', json={'query': mutation})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert data['data']['updateOrderStatus']['success'] == True
    assert data['data']['updateOrderStatus']['order']['status'] == 'processing'


def test_graphql_query_with_relations(client, sample_order):
    """Test GraphQL query with nested relations."""
    query = f"""
        query {{
            order(id: {sample_order.id}) {{
                id
                order_number
                retailer {{
                    name
                    edi_identifier
                }}
                order_lines {{
                    quantity_ordered
                    unit_price
                    product {{
                        sku
                        name
                    }}
                }}
            }}
        }}
    """
    
    response = client.post('/graphql', json={'query': query})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'order' in data['data']
    assert data['data']['order']['order_number'] == sample_order.order_number
    assert 'retailer' in data['data']['order']
    assert 'order_lines' in data['data']['order']
