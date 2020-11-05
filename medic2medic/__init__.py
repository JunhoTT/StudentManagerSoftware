from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)
    ma.init_app(app)
    import google_auth
    app.register_blueprint(google_auth.app)
    with app.app_context():
        from .models import equipment_pack_content
        from .models import equipment_pack
        from .models import laptop
        from .models import payment
        from .models import student_pack_content
        from .models import student

        from .models import tuition

        from .models import university
        from .models import course

        from .models import user
        from .models import quotes

        from .models import book
        from .models import assignedBooks

        db.create_all()  # Create sql tables for our data models
        from .routes import awsS3
        from .routes import equipment_pack
        from .routes import laptop
        from .routes import main
        from .routes import payment
        from .routes import reports
        from .routes import student
        from .routes import users

        from .routes import tuition

        from .routes import university
        from .routes import course
        from .routes import book
        from .routes import assignedBooks

        from .routes import quote
        user.setup_admin()
        user.log_admins()
        return app
