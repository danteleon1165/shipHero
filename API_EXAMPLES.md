# API Examples

This directory contains example requests for the Mini EDI Order Management API.

## Prerequisites

Make sure the application is running:
```bash
python run_dev.py
```

## REST API Examples

### 1. List All Products
```bash
curl http://localhost:5000/api/products
```

### 2. Get a Specific Product
```bash
curl http://localhost:5000/api/products/1
```

### 3. Create a New Product
```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "sku": "NEW-PRODUCT-001",
    "name": "New Product",
    "description": "A brand new product",
    "price": 39.99,
    "cost": 20.00,
    "quantity_on_hand": 100
  }'
```

### 4. List All Orders
```bash
curl http://localhost:5000/api/orders
```

### 5. Receive an EDI Order from SPS Commerce
```bash
curl -X POST http://localhost:5000/api/sps/orders \
  -H "Content-Type: application/json" \
  -d '{
    "order_number": "SPS-12345",
    "retailer_edi_identifier": "WALMART001",
    "order_date": "2024-01-20T10:00:00",
    "ship_to_name": "Alice Williams",
    "ship_to_address1": "321 Elm Street",
    "ship_to_city": "Seattle",
    "ship_to_state": "WA",
    "ship_to_zip": "98101",
    "ship_to_country": "USA",
    "order_lines": [
      {
        "sku": "WIDGET-001",
        "quantity": 3,
        "unit_price": 29.99
      }
    ]
  }'
```

### 6. Create a Shipment
```bash
curl -X POST http://localhost:5000/api/shipments \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "shipment_number": "SHIP-NEW-001",
    "carrier": "FedEx",
    "tracking_number": "774567890123",
    "service_level": "Express",
    "status": "pending",
    "shipped_date": "2024-01-20T14:00:00"
  }'
```

### 7. Adjust Inventory
```bash
curl -X POST http://localhost:5000/api/inventory/adjust \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "adjustment_type": "purchase",
    "quantity_change": 100,
    "reason": "Received new stock from supplier",
    "reference_number": "PO-2024-001",
    "created_by": "warehouse_manager"
  }'
```

## GraphQL Examples

### Query: Get All Products
```bash
curl -X POST http://localhost:5000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ products(limit: 10) { id sku name price quantity_on_hand quantity_available } }"
  }'
```

### Query: Get Orders with Details
```bash
curl -X POST http://localhost:5000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ orders(limit: 5) { id order_number status total_amount retailer { name edi_identifier } order_lines { quantity_ordered product { sku name } } } }"
  }'
```

### Mutation: Update Inventory
```bash
curl -X POST http://localhost:5000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { updateInventory(product_id: 1, quantity_change: 50, adjustment_type: \"purchase\", reason: \"Restock\") { success message product { quantity_on_hand } } }"
  }'
```

### Mutation: Update Order Status
```bash
curl -X POST http://localhost:5000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { updateOrderStatus(order_id: 1, status: \"processing\") { success message order { id status } } }"
  }'
```

### Mutation: Create Product via GraphQL
```bash
curl -X POST http://localhost:5000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { createProduct(sku: \"GQL-PROD-001\", name: \"GraphQL Product\", price: 45.99, cost: 22.50, quantity_on_hand: 200) { id sku name price } }"
  }'
```

### Query: Get Specific Order with All Relations
```bash
curl -X POST http://localhost:5000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ order(id: 1) { order_number status ship_to_name ship_to_city retailer { name contact_email } order_lines { quantity_ordered unit_price product { sku name } } shipments { shipment_number carrier tracking_number status } } }"
  }'
```

## Testing the GraphQL Playground

Open your browser and go to:
```
http://localhost:5000/graphql
```

This will open the GraphiQL interactive explorer where you can:
- Browse the schema
- Write queries with autocomplete
- See documentation for all types
- Execute queries and mutations interactively

## Filter Examples

### Filter Orders by Status
```bash
curl "http://localhost:5000/api/orders?status=pending"
```

### Filter Products by SKU
```bash
curl "http://localhost:5000/api/products?sku=WIDGET"
```

### Filter Shipments by Order
```bash
curl "http://localhost:5000/api/shipments?order_id=3"
```

## Pagination Examples

```bash
# Get page 1 with 10 items
curl "http://localhost:5000/api/orders?page=1&per_page=10"

# Get page 2 with 5 items
curl "http://localhost:5000/api/products?page=2&per_page=5"
```
