from functools import wraps
from flask import jsonify
import logging


def setup_logging(app):
    """Configure application logging."""
    if not app.debug:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)


def validate_required_fields(data, required_fields):
    """Validate that all required fields are present in the data."""
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    return True, None


def handle_errors(f):
    """Decorator to handle common errors in route handlers."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception:
            return jsonify({'error': 'Internal server error'}), 500
    return decorated_function
