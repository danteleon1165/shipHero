from ariadne import make_executable_schema, graphql_sync, load_schema_from_path
from ariadne.explorer import ExplorerGraphiQL
from flask import request, jsonify
from app.schemas.resolvers import (
    query, mutation, 
    retailer_type, product_type, order_type, 
    order_line_type, shipment_type, inventory_adjustment_type
)
import os


def setup_graphql(app):
    """Setup GraphQL endpoint with Ariadne."""
    
    # Load schema
    schema_path = os.path.join(
        os.path.dirname(__file__), 
        'schema.graphql'
    )
    type_defs = load_schema_from_path(schema_path)
    
    # Create executable schema
    schema = make_executable_schema(
        type_defs,
        query,
        mutation,
        retailer_type,
        product_type,
        order_type,
        order_line_type,
        shipment_type,
        inventory_adjustment_type
    )
    
    # GraphQL endpoint with GraphiQL explorer
    @app.route('/graphql', methods=['GET'])
    def graphql_explorer():
        return ExplorerGraphiQL().html(None), 200
    
    @app.route('/graphql', methods=['POST'])
    def graphql_server():
        data = request.get_json()
        
        success, result = graphql_sync(
            schema,
            data,
            context_value={"request": request},
            debug=app.debug
        )
        
        status_code = 200 if success else 400
        return jsonify(result), status_code
