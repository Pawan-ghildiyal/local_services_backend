from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    # Create Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)

    # Import and register blueprints
    from routes.auth_routes import auth_bp
    from routes.provider_routes import provider_bp
    from routes.booking_routes import booking_bp
    from routes.feedback_routes import feedback_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(provider_bp, url_prefix="/api/providers")
    app.register_blueprint(booking_bp, url_prefix="/api/bookings")
    app.register_blueprint(feedback_bp, url_prefix="/api/feedback")

    return app

# Create app instance
app = create_app()

# Initialize Migrate AFTER app and db are set up
migrate = Migrate(app, db)

# Run app
if __name__ == "__main__":
    app.run(debug=True)
