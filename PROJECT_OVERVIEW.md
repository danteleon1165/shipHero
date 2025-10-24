# Mini EDI Order Management API - Project Overview

## 🎯 Project Purpose

This project demonstrates a **production-ready EDI Order Management System** similar to platforms like ShipHero and SPS Commerce. It showcases:

- Modern API design patterns (REST + GraphQL)
- Enterprise-level data modeling
- EDI integration concepts
- Background job processing
- Comprehensive testing
- Docker containerization

## 🏗️ Architecture

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Web Framework** | Flask 3.0 | Modern Python web framework |
| **ORM** | SQLAlchemy 2.0 | Database abstraction and modeling |
| **Database** | MySQL 8.0 | Production database (SQLite for testing) |
| **GraphQL** | Ariadne | Code-first GraphQL implementation |
| **Scheduler** | APScheduler | Background job processing |
| **Testing** | pytest | Comprehensive test coverage |
| **Container** | Docker | Application containerization |

### System Design

```
┌─────────────────────────────────────────────────────────┐
│                     API Gateway Layer                    │
│  ┌──────────────────┐        ┌──────────────────┐      │
│  │   REST Endpoints │        │  GraphQL Schema  │      │
│  │  /api/orders     │        │  Queries/        │      │
│  │  /api/products   │        │  Mutations       │      │
│  │  /api/shipments  │        │                  │      │
│  └──────────────────┘        └──────────────────┘      │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                    Service Layer                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  OrderService                                     │  │
│  │  - create_order_from_edi()                       │  │
│  │  - cancel_order()                                │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                    Data Layer                            │
│  ┌────────────┬───────────┬──────────┬─────────────┐   │
│  │ Retailer   │ Product   │  Order   │  Shipment   │   │
│  │            │           │          │             │   │
│  │ OrderLine  │ Inventory │          │             │   │
│  │            │ Adjustment│          │             │   │
│  └────────────┴───────────┴──────────┴─────────────┘   │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                 Background Jobs Layer                    │
│  ┌──────────────────────────────────────────────────┐  │
│  │  APScheduler                                      │  │
│  │  - Poll SPS Orders (every 5 minutes)            │  │
│  │  - Sync Inventory to Retailers                   │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 📊 Data Model

### Core Entities

**Retailer** (EDI Partners)
- Represents trading partners like Walmart, Target, Amazon
- Stores EDI identifiers and contact information
- Links to orders

**Product** (SKU Management)
- SKU, UPC, and product details
- Real-time inventory tracking (on_hand, reserved, available)
- Pricing information (cost, retail price)

**Order** (Customer Orders)
- Order header with shipping details
- Status tracking (pending, processing, shipped, completed, cancelled)
- Financial totals (subtotal, tax, shipping, total)

**OrderLine** (Line Items)
- Links products to orders
- Quantity ordered vs. shipped tracking
- Line-level pricing

**Shipment** (Fulfillment)
- Carrier and tracking information
- Multi-shipment support per order
- Status tracking (pending, in_transit, delivered)

**InventoryAdjustment** (Audit Trail)
- Complete history of inventory changes
- Adjustment types (purchase, sale, return, damage, adjustment)
- Reference numbers for traceability

### Entity Relationships

```
Retailer (1) ──< (N) Order
Product (1) ──< (N) OrderLine >── (1) Order
Product (1) ──< (N) InventoryAdjustment
Order (1) ──< (N) Shipment
```

## 🚀 Key Features

### 1. REST API

Complete CRUD operations for:
- **Orders**: Create, list, retrieve, update
- **Products**: Full product lifecycle management
- **Shipments**: Tracking and status updates
- **Inventory**: Real-time adjustments with audit trail

### 2. GraphQL API

- **Flexible Queries**: Get exactly the data you need
- **Nested Relations**: Fetch related data in single request
- **Mutations**: Create and update operations
- **GraphiQL Explorer**: Interactive API documentation

### 3. EDI Simulation

**SPS Commerce Integration Endpoint**
```
POST /api/sps/orders
```

Simulates receiving EDI 850 Purchase Orders from retailers:
- Validates retailer EDI identifiers
- Creates orders with line items
- Reserves inventory automatically
- Calculates totals

### 4. Background Jobs

**Scheduled Tasks:**
- Poll SPS Commerce for new orders (every 5 minutes)
- Sync inventory levels to retailers
- Process order status updates

### 5. Inventory Management

**Real-time Tracking:**
- `quantity_on_hand`: Physical inventory
- `quantity_reserved`: Allocated to orders
- `quantity_available`: Available for sale

**Adjustment Types:**
- Purchase receipts
- Sales/fulfillment
- Returns
- Damage/loss
- Manual adjustments

### 6. Comprehensive Testing

**28 Passing Tests:**
- REST endpoint tests
- GraphQL query/mutation tests
- Business logic validation
- Edge case handling
- Error scenarios

**Test Coverage:**
- Products: 5 tests
- Orders: 6 tests
- Shipments: 5 tests
- Inventory: 6 tests
- GraphQL: 6 tests

## 📈 Production Readiness

### What's Included

✅ **Application Factory Pattern**: Flexible initialization
✅ **Configuration Management**: Environment-based configs
✅ **Database Migrations**: Flask-Migrate support
✅ **Error Handling**: Consistent error responses
✅ **CORS Support**: Cross-origin requests enabled
✅ **Docker Support**: Containerized deployment
✅ **Background Jobs**: Scheduled task processing
✅ **Comprehensive Tests**: 100% passing test suite
✅ **API Documentation**: REST + GraphQL examples
✅ **Seed Data**: Sample data for testing

### What Would Be Added for Production

🔲 **Authentication**: JWT-based auth
🔲 **Authorization**: Role-based access control
🔲 **Rate Limiting**: API throttling
🔲 **Logging**: Structured logging (ELK stack)
🔲 **Monitoring**: Prometheus + Grafana
🔲 **Caching**: Redis for performance
🔲 **Message Queue**: Celery for async tasks
🔲 **API Versioning**: Version management
🔲 **Webhooks**: Event notifications
🔲 **Documentation**: OpenAPI/Swagger specs

## 🎓 Educational Value

### Demonstrates Knowledge Of:

1. **API Design**
   - RESTful principles
   - GraphQL patterns
   - API versioning concepts

2. **Database Design**
   - Normalized schema design
   - Foreign key relationships
   - Index strategy
   - Audit trail patterns

3. **Business Logic**
   - Order processing workflows
   - Inventory management
   - State machine patterns
   - Transaction handling

4. **Integration Patterns**
   - EDI concepts
   - Scheduled jobs
   - Webhook patterns
   - Third-party API simulation

5. **Testing**
   - Unit testing
   - Integration testing
   - Fixture management
   - Test isolation

6. **DevOps**
   - Docker containerization
   - Docker Compose orchestration
   - Environment configuration
   - Deployment patterns

## 🔄 Typical Workflows

### 1. Order Fulfillment Flow

```
1. Receive EDI Order (POST /api/sps/orders)
   ↓
2. Validate retailer and products
   ↓
3. Create order and line items
   ↓
4. Reserve inventory
   ↓
5. Update order status to "processing"
   ↓
6. Create shipment (POST /api/shipments)
   ↓
7. Deduct inventory on shipment
   ↓
8. Update order status to "shipped"
   ↓
9. Update shipment status to "delivered"
   ↓
10. Mark order as "completed"
```

### 2. Inventory Management Flow

```
1. Receive purchase order from supplier
   ↓
2. Adjust inventory (POST /api/inventory/adjust)
   - type: "purchase"
   - quantity_change: +100
   ↓
3. Create audit record (InventoryAdjustment)
   ↓
4. Update product quantities
   - quantity_on_hand += 100
   - quantity_available += 100
   ↓
5. Sync to retailers (background job)
```

## 📦 Project Statistics

- **Total Files**: 34
- **Lines of Code**: ~2,700
- **Models**: 6
- **REST Endpoints**: 12
- **GraphQL Queries**: 8
- **GraphQL Mutations**: 4
- **Tests**: 28
- **Test Coverage**: High

## 🎯 Interview Talking Points

1. **Scalability**: How would you scale this for high volume?
   - Read replicas for queries
   - Write queue for orders
   - Caching layer for products
   - Sharding strategy

2. **Reliability**: How would you ensure 99.9% uptime?
   - Health checks
   - Circuit breakers
   - Retry mechanisms
   - Database replication

3. **Performance**: How would you optimize for speed?
   - Database indexing
   - Query optimization
   - Caching strategies
   - Async processing

4. **Security**: How would you secure the API?
   - OAuth 2.0 / JWT
   - API key management
   - Input validation
   - SQL injection prevention
   - Rate limiting

5. **Observability**: How would you monitor in production?
   - Application metrics
   - Request tracing
   - Error tracking
   - Performance monitoring

## 🚀 Next Steps for Enhancement

1. **Real EDI Integration**: Connect to actual EDI providers
2. **Admin Dashboard**: React frontend with D3 visualizations
3. **Webhook System**: Real-time event notifications
4. **Advanced Reporting**: Analytics and insights
5. **Multi-warehouse**: Support for multiple fulfillment centers
6. **Returns Management**: Complete returns workflow
7. **Batch Processing**: Bulk operations support
8. **API Documentation**: Interactive OpenAPI docs

---

**This project demonstrates production-ready API development skills suitable for modern e-commerce and logistics platforms.**
