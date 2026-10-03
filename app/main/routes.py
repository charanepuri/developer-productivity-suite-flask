from flask import render_template

from app.main import main_bp


@main_bp.route("/")
def home():
    return render_template("home.html")

@main_bp.route("/about")
def about():
    return render_template("about.html")