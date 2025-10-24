import os
from app import create_app
from app.models import db

# Get environment
env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)


if __name__ == '__main__':
    # Create tables if they don't exist (for development)
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config.get('DEBUG', False)
    )
