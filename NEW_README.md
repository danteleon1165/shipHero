# Mini EDI Order Management API

A production-style API simulating EDI Order Management with Flask, SQLAlchemy, MySQL, and GraphQL (Ariadne). This project demonstrates realistic integration patterns similar to ShipHero and SPS Commerce.

## 🚀 Features

- **REST API** for order management, inventory, and shipments
- **GraphQL API** with queries and mutations using Ariadne
- **EDI Simulation** for receiving orders from SPS Commerce
- **Background Jobs** using APScheduler for order polling
- **Comprehensive Testing** with pytest
- **Docker Support** for easy deployment
- **Production-Ready** patterns and structure

## 📋 Table of Contents

- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)
- [Background Jobs](#background-jobs)
- [Architecture](#architecture)

## 🛠 Tech Stack

- **Backend:** Flask 3.0
- **ORM:** SQLAlchemy 2.0
- **Database:** MySQL 8.0
- **GraphQL:** Ariadne
- **Background Jobs:** APScheduler
- **Testing:** pytest
- **Deployment:** Docker & Docker Compose

## 📁 Project Structure

```
mini_edi_api/
├── app/
│   ├── __init__.py           # Application factory
│   ├── config.py             # Configuration classes
│   ├── models.py             # SQLAlchemy models
│   ├── routes/               # REST API endpoints
│   │   ├── orders.py
│   │   ├── products.py
│   │   ├── shipments.py
│   │   └── inventory.py
│   ├── schemas/              # GraphQL schemas
│   │   ├── schema.graphql
│   │   ├── schema.py
│   │   └── resolvers.py
│   ├── services/             # Business logic
│   │   └── order_service.py
│   ├── utils/                # Utility functions
│   │   └── helpers.py
│   └── jobs/                 # Background jobs
│       ├── scheduler.py
│       └── edi_sync.py
├── tests/                    # Test suite
│   ├── conftest.py
│   ├── test_products.py
│   ├── test_orders.py
│   ├── test_shipments.py
│   ├── test_inventory.py
│   └── test_graphql.py
├── migrations/               # Database migrations
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🔧 Installation

### Prerequisites

- Python 3.11+
- MySQL 8.0+
- pip

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/danteleon1165/shipHero.git
   cd shipHero
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL database:**
   ```bash
   mysql -u root -p
   CREATE DATABASE mini_edi_db;
   CREATE USER 'edi_user'@'localhost' IDENTIFIED BY 'edi_password';
   GRANT ALL PRIVILEGES ON mini_edi_db.* TO 'edi_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

5. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

## ⚙️ Configuration

Edit `.env` file with your settings:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=edi_user
MYSQL_PASSWORD=edi_password
MYSQL_DATABASE=mini_edi_db
```

## 🚀 Running the Application

### Development Mode

```bash
python run.py
```

The API will be available at:
- REST API: `http://localhost:5000/api`
- GraphQL: `http://localhost:5000/graphql`
- Health Check: `http://localhost:5000/health`

### Production Mode

```bash
export FLASK_ENV=production
python run.py
```

## 📚 API Documentation

### REST Endpoints

#### Orders
- `POST /api/sps/orders` - Receive EDI order from SPS Commerce
- `GET /api/orders` - List orders (with filtering)
- `GET /api/orders/<id>` - Get order details
- `PUT /api/orders/<id>` - Update order

#### Products
- `GET /api/products` - List products
- `GET /api/products/<id>` - Get product details
- `POST /api/products` - Create product
- `PUT /api/products/<id>` - Update product

#### Shipments
- `POST /api/shipments` - Create shipment
- `GET /api/shipments` - List shipments
- `GET /api/shipments/<id>` - Get shipment details
- `PUT /api/shipments/<id>` - Update shipment

#### Inventory
- `POST /api/inventory/adjust` - Adjust inventory
- `GET /api/inventory/product/<id>` - Get product inventory
- `GET /api/inventory/adjustments` - List adjustments

### GraphQL Endpoints

#### Queries
```graphql
query {
  orders(status: "pending", limit: 10) {
    id
    order_number
    status
    retailer { name }
    order_lines {
      quantity_ordered
      product { sku, name }
    }
  }
  
  products(is_active: true) {
    sku
    name
    quantity_available
  }
}
```

#### Mutations
```graphql
mutation {
  updateInventory(
    product_id: 1,
    quantity_change: 50,
    adjustment_type: "purchase",
    reason: "New stock"
  ) {
    success
    message
    product { quantity_on_hand }
  }
  
  updateOrderStatus(order_id: 1, status: "processing") {
    success
    order { status }
  }
}
```

### Example: Receive SPS Order

```bash
curl -X POST http://localhost:5000/api/sps/orders \
  -H "Content-Type: application/json" \
  -d '{
    "order_number": "ORD-12345",
    "retailer_edi_identifier": "WALMART001",
    "order_date": "2024-01-15T10:00:00",
    "ship_to_name": "John Doe",
    "ship_to_address1": "123 Main St",
    "ship_to_city": "Anytown",
    "ship_to_state": "CA",
    "ship_to_zip": "12345",
    "order_lines": [
      {
        "sku": "PROD-001",
        "quantity": 2,
        "unit_price": 19.99
      }
    ]
  }'
```

## 🧪 Testing

### Run all tests:
```bash
pytest
```

### Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

### Run specific test file:
```bash
pytest tests/test_orders.py
```

### Test Structure:
- `test_products.py` - Product CRUD operations
- `test_orders.py` - Order management and EDI
- `test_shipments.py` - Shipment tracking
- `test_inventory.py` - Inventory adjustments
- `test_graphql.py` - GraphQL queries and mutations

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Using Docker only

```bash
# Build image
docker build -t mini-edi-api .

# Run container
docker run -p 5000:5000 \
  -e MYSQL_HOST=host.docker.internal \
  -e MYSQL_USER=edi_user \
  -e MYSQL_PASSWORD=edi_password \
  mini-edi-api
```

## ⏰ Background Jobs

The application includes APScheduler for background tasks:

### EDI Order Polling
- **Frequency:** Every 5 minutes
- **Purpose:** Poll SPS Commerce for new orders
- **Location:** `app/jobs/edi_sync.py`

To customize job schedules, edit `app/jobs/scheduler.py`:

```python
scheduler.add_job(
    func=lambda: poll_sps_orders(app),
    trigger=IntervalTrigger(minutes=5),
    id='poll_sps_orders',
    name='Poll SPS Commerce for new orders'
)
```

## 🏗 Architecture

### Core Entities

1. **Retailer** - EDI partners (Walmart, Target, etc.)
2. **Product** - SKU, UPC, inventory tracking
3. **Order** - Customer orders with EDI info
4. **OrderLine** - Individual line items
5. **Shipment** - Carrier tracking and status
6. **InventoryAdjustment** - Audit trail for inventory changes

### Database Schema

```
retailers (1) ──< (N) orders
products (1) ──< (N) order_lines >── (1) orders
products (1) ──< (N) inventory_adjustments
orders (1) ──< (N) shipments
```

### Key Design Patterns

- **Application Factory** - Flexible app initialization
- **Service Layer** - Business logic separation
- **Repository Pattern** - Data access abstraction
- **Background Jobs** - Async processing with APScheduler

## 🔒 Security Considerations

- Environment variables for sensitive data
- Input validation on all endpoints
- SQLAlchemy ORM prevents SQL injection
- CORS configured for cross-origin requests

## 📈 Future Enhancements

- [ ] Add JWT authentication
- [ ] Implement rate limiting
- [ ] Add Celery for distributed tasks
- [ ] Create admin dashboard with React
- [ ] Add webhook support for order updates
- [ ] Implement real EDI (X12/EDIFACT) parsing
- [ ] Add comprehensive logging and monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## 📝 License

This project is for educational purposes.

## 👤 Author

Built as a demonstration project for interview purposes, showcasing production-ready API development patterns.

## 📞 Support

For questions or issues, please open an issue on GitHub.

---

**Note:** This is a simulation project for educational purposes. In a production environment, you would integrate with actual EDI providers (SPS Commerce, CommerceHub, etc.) and implement additional security, monitoring, and scaling features.
