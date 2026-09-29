from flask import render_template

from app.tools import tools_bp


@tools_bp.route("/")
def index():
    return render_template("tools/index.html")