from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from app.config import config_by_name
from app.models import db


migrate = Migrate()


def create_app(config_name='default'):
    """Flask application factory."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_by_name[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Register blueprints
    from app.routes.orders import orders_bp
    from app.routes.products import products_bp
    from app.routes.shipments import shipments_bp
    from app.routes.inventory import inventory_bp
    
    app.register_blueprint(orders_bp, url_prefix='/api')
    app.register_blueprint(products_bp, url_prefix='/api')
    app.register_blueprint(shipments_bp, url_prefix='/api')
    app.register_blueprint(inventory_bp, url_prefix='/api')
    
    # Setup GraphQL
    from app.schemas.schema import setup_graphql
    setup_graphql(app)
    
    # Setup background jobs
    from app.jobs.scheduler import setup_scheduler
    if not app.config.get('TESTING'):
        setup_scheduler(app)
    
    @app.route('/')
    def index():
        return {
            'message': 'Mini EDI Order Management API',
            'version': '1.0.0',
            'endpoints': {
                'rest': {
                    'orders': '/api/orders',
                    'sps_orders': '/api/sps/orders',
                    'products': '/api/products',
                    'shipments': '/api/shipments',
                    'inventory': '/api/inventory/adjust'
                },
                'graphql': '/graphql'
            }
        }
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    return app
