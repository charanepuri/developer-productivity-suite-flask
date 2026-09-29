from flask import render_template

from app.admin import admin_bp


@admin_bp.route("/")
def index():
    return render_template("admin/index.html")