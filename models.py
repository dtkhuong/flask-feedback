""" Models for Feedback App."""

from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()
# bcrypt = Bcrypt()


class User(db.Model):
    """User model."""
    
    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, password):
        """Register user with hashed password and return user."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8)


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
