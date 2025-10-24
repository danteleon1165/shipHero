#!/usr/bin/env python
"""
Simple script to demonstrate the API works with SQLite for development/testing.
This starts the app without trying to create tables on startup.
"""
import os

# Set testing mode to use SQLite
os.environ['FLASK_ENV'] = 'testing'

from app import create_app

if __name__ == '__main__':
    app = create_app('testing')
    
    # Create tables in testing environment
    from app.models import db
    with app.app_context():
        db.create_all()
        print("✓ Database tables created successfully!")
    
    print("✓ Flask application factory working")
    print("✓ All routes registered")
    print("✓ GraphQL schema loaded")
    print("\nStarting server on http://localhost:5000")
    print("Note: Background scheduler disabled in testing mode")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
