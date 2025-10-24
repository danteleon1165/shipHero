# shipHero


digraph ShipHeroAPI {
  rankdir=LR;
  node [shape=record, fontname="Helvetica"];

  API [label="{ShipHero Public GraphQL API|endpoint: https://public-api.shiphero.com/graphql}"];
  AUTH [label="{Authentication|/auth/token -> Bearer JWT}"];
  WEBHOOKS [label="{Webhooks|Inventory Update, Shipment Update, Order Update, Inventory Snapshot}"];
  COMPLEXITY [label="{Complexity & Quotas|query complexity, credits, analyze:true}"];
  DOCS [label="{Docs & Examples|schema, examples, mutations, queries}"];

  Account [label="{Account}"];
  Products [label="{Products|queries: products, product_create, product_update}"];
  Orders [label="{Orders|queries: order(s), create_order, order_fulfillment}"];
  Shipments [label="{Shipments|queries: shipments, create_shipment}"];
  Returns [label="{Returns|return_create}"];
  Inventory [label="{Inventory|inventory_sync, inventory_snapshot, warehouse_products}"];
  PurchaseOrders [label="{PurchaseOrders|purchase_orders, create_purchase_order}"];
  Vendors [label="{Vendors}"];
  Warehouses [label="{Warehouses}"];
  WebhookManagement [label="{Webhook Management|register, unregister, list, verify}"];
  Pagination [label="{Pagination Patterns|connections: edges -> node, args: first,last,filters}"];

  API -> AUTH;
  API -> DOCS;
  API -> COMPLEXITY;
  API -> WEBHOOKS [label="complements"];
  API -> Account;
  API -> Products;
  API -> Orders;
  API -> Shipments;
  API -> Returns;
  API -> Inventory;
  API -> PurchaseOrders;
  API -> Vendors;
  API -> Warehouses;
  API -> WebhookManagement;
  API -> Pagination;

  Orders -> Shipments [label="has/creates"];
  Orders -> Returns [label="may link to"];
  Products -> Inventory [label="stock levels / warehouse_products"];
  Warehouses -> Inventory [label="holds products"];
  PurchaseOrders -> Vendors [label="ordered from"];
  Inventory -> "Inventory Snapshot" [label="export (async)"];
  "Inventory Snapshot" [shape=note];
  WebhookManagement -> WEBHOOKS;

  COMPLEXITY -> Pagination [label="encourage limits"];
  COMPLEXITY -> "Analyze Mode" [label="analyze:true"];
  "Analyze Mode" [shape=note];

  subgraph cluster_client {
    label="Client / Integration";
    color=blue;
    ClientApp [label="Client (Python/JS)"];
    ClientApp -> API [label="POST {query, variables} + Authorization header"];
    ClientApp -> WEBHOOKS [style=dashed, label="register callback"];
  }
}
