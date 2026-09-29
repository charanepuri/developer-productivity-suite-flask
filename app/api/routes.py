from flask import jsonify

from app.api import api_bp


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