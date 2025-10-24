# Quick Start Guide

Get the Mini EDI Order Management API up and running in 5 minutes!

## Option 1: Quick Local Start (SQLite - No MySQL Required)

### 1. Clone and Setup
```bash
git clone https://github.com/danteleon1165/shipHero.git
cd shipHero
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Seed the Database
```bash
python seed_data.py
```

Expected output:
```
✓ Created 3 retailers
✓ Created 4 products
✓ Created 3 orders with line items
✓ Created 1 shipment
Database seeded successfully!
```

### 3. Start the Server
```bash
python run_dev.py
```

Expected output:
```
✓ Database tables created successfully!
✓ Flask application factory working
✓ All routes registered
✓ GraphQL schema loaded

Starting server on http://localhost:5000
```

### 4. Test the API

**In another terminal:**

```bash
# Test REST endpoint
curl http://localhost:5000/api/products

# Test GraphQL endpoint
curl -X POST http://localhost:5000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ products { sku name price } }"}'
```

**Or open in browser:**
- REST API: http://localhost:5000/api/products
- GraphQL Explorer: http://localhost:5000/graphql

## Option 2: Docker (Production-like)

### 1. Clone the Repository
```bash
git clone https://github.com/danteleon1165/shipHero.git
cd shipHero
```

### 2. Start with Docker Compose
```bash
docker-compose up --build
```

This will:
- Start MySQL 8.0 container
- Start Flask application container
- Set up networking between services
- Initialize the database

### 3. Access the API
- REST API: http://localhost:5000/api
- GraphQL: http://localhost:5000/graphql

### 4. Populate Sample Data

**In another terminal:**
```bash
docker-compose exec app python seed_data.py
```

## Testing the API

### REST Examples

```bash
# List all products
curl http://localhost:5000/api/products

# Get specific order
curl http://localhost:5000/api/orders/1

# Create a new product
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "sku": "NEW-001",
    "name": "New Product",
    "price": 29.99,
    "quantity_on_hand": 100
  }'

# Receive EDI order
curl -X POST http://localhost:5000/api/sps/orders \
  -H "Content-Type: application/json" \
  -d '{
    "order_number": "SPS-001",
    "retailer_edi_identifier": "WALMART001",
    "order_lines": [{"sku": "WIDGET-001", "quantity": 2}]
  }'
```

### GraphQL Examples

**Open the GraphiQL Explorer:**
http://localhost:5000/graphql

**Try these queries:**

```graphql
# Get all products
{
  products(limit: 10) {
    sku
    name
    price
    quantity_available
  }
}

# Get orders with details
{
  orders(limit: 5) {
    order_number
    status
    total_amount
    retailer {
      name
    }
    order_lines {
      quantity_ordered
      product {
        sku
        name
      }
    }
  }
}

# Update inventory
mutation {
  updateInventory(
    product_id: 1
    quantity_change: 50
    adjustment_type: "purchase"
    reason: "New stock"
  ) {
    success
    message
    product {
      quantity_on_hand
    }
  }
}
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_products.py

# Run with verbose output
pytest -v
```

Expected output:
```
============================== 28 passed in 1.24s ==============================
```

## Exploring the Code

### Key Files to Review

1. **Models** (`app/models.py`): Database schema and relationships
2. **REST Routes** (`app/routes/`): API endpoints
3. **GraphQL Schema** (`app/schemas/schema.graphql`): GraphQL types
4. **GraphQL Resolvers** (`app/schemas/resolvers.py`): Query/mutation logic
5. **Tests** (`tests/`): Comprehensive test suite

### Project Structure

```
shipHero/
├── app/
│   ├── models.py           # SQLAlchemy models
│   ├── routes/             # REST endpoints
│   │   ├── orders.py
│   │   ├── products.py
│   │   ├── shipments.py
│   │   └── inventory.py
│   ├── schemas/            # GraphQL
│   │   ├── schema.graphql
│   │   ├── schema.py
│   │   └── resolvers.py
│   ├── services/           # Business logic
│   │   └── order_service.py
│   └── jobs/               # Background tasks
│       ├── scheduler.py
│       └── edi_sync.py
├── tests/                  # Test suite
├── run_dev.py             # Development server
├── seed_data.py           # Sample data
└── docker-compose.yml     # Docker setup
```

## Common Issues & Solutions

### Issue: Port 5000 already in use
**Solution:**
```bash
# Change port in run_dev.py or use environment variable
export PORT=8000
python run_dev.py
```

### Issue: MySQL connection refused (Docker)
**Solution:**
```bash
# Wait for MySQL to fully start
docker-compose logs mysql

# Or restart services
docker-compose restart
```

### Issue: Permission denied on Docker
**Solution:**
```bash
# Run with sudo or add user to docker group
sudo docker-compose up
```

## Next Steps

1. **Explore the API**: Try the examples in `API_EXAMPLES.md`
2. **Review the Tests**: Check `tests/` directory
3. **Read the Docs**: See `README.md` and `PROJECT_OVERVIEW.md`
4. **Customize**: Modify models, add endpoints, extend functionality

## Getting Help

- Check `README.md` for detailed documentation
- Review `API_EXAMPLES.md` for more API examples
- Read `PROJECT_OVERVIEW.md` for architecture details
- Look at test files for usage examples

## Success Indicators

You know it's working when you see:
- ✅ Server starts without errors
- ✅ All 28 tests pass
- ✅ API responds to HTTP requests
- ✅ GraphQL explorer loads
- ✅ Sample data loads successfully

**Happy coding! 🚀**
