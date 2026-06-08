from flask import Blueprint, render_template, request, jsonify

from models import db, User, LoginLog
from auth import hash_password, check_password

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        return jsonify({"error": "E-Mail und Passwort erforderlich"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "E-Mail bereits registriert"}), 409

    user = User(email=email, password_hash=hash_password(password))
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registrierung erfolgreich"}), 201


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    user = User.query.filter_by(email=email).first()
    success = user is not None and check_password(password, user.password_hash)

    # Jeden Versuch protokollieren (Anforderung 7)
    db.session.add(LoginLog(email=email, success=success))
    db.session.commit()

    if success:
        return jsonify({"message": "Login erfolgreich"}), 200
    return jsonify({"error": "Ungueltige Anmeldedaten"}), 401
