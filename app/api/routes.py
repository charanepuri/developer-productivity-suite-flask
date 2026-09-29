from flask import jsonify

from app.api import api_bp
from app.models import Category, Tool, User


@api_bp.route("/")
def index():
    return jsonify({
        "name": "Developer Productivity Suite API",
        "version": "1.0",
        "status": "active"
    })


@api_bp.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@api_bp.route("/database-status")
def database_status():
    return jsonify({
        "database": "connected",
        "users": User.query.count(),
        "categories": Category.query.count(),
        "tools": Tool.query.count()
    })