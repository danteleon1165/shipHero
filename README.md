graph LR
  API[ShipHero Public GraphQL API<br/>https://public-api.shiphero.com/graphql]
  AUTH[/auth/token → Bearer JWT/]
  WEBHOOKS[Webhooks: Inventory Update, Shipment Update, Order Update, Inventory Snapshot]
  COMPLEXITY[Complexity & Quotas: query complexity, credits, analyze:true]
  DOCS[Docs & Examples: schema, examples, mutations, queries]
  Account[Account]
  Products[Products (products, product_create, product_update)]
  Orders[Orders (order(s), create_order, fulfillment)]
  Shipments[Shipments (shipments, create_shipment)]
  Returns[Returns (return_create)]
  Inventory[Inventory (inventory_sync, snapshot, warehouse_products)]
  PurchaseOrders[Purchase Orders]
  Vendors[Vendors]
  Warehouses[Warehouses]
  WebhookMgmt[Webhook Management (register, unregister, list, verify)]
  Pagination[Pagination: connections (edges → node), args: first,last,filters]

  API --> AUTH
  API --> DOCS
  API --> COMPLEXITY
  API --> WEBHOOKS
  API --> Account
  API --> Products
  API --> Orders
  API --> Shipments
  API --> Returns
  API --> Inventory
  API --> PurchaseOrders
  API --> Vendors
  API --> Warehouses
  API --> WebhookMgmt
  API --> Pagination

  Orders --> Shipments
  Orders --> Returns
  Products --> Inventory
  Warehouses --> Inventory
  PurchaseOrders --> Vendors
  Inventory --> Snapshot[Inventory Snapshot (async export)]
  WebhookMgmt --> WEBHOOKS

  COMPLEXITY --> Pagination
  COMPLEXITY --> Analyze[Analyze Mode (analyze:true)]
  Client[Client (Python/JS)] -->|POST {query,variables} + Authorization| API
  Client -->|register callback| WEBHOOKS
