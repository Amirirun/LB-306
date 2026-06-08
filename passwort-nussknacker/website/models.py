from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Registrierte Konten."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)  


class LoginLog(db.Model):
    """Protokoll jedes Loginversuchs (Anforderung 7).

    Kein Fremdschluessel zu users, weil auch Versuche mit nicht
    existierenden E-Mail-Adressen geloggt werden muessen.
    """

    __tablename__ = "login_logs"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    success = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
