from flask import render_template

from app.user import user_bp


@user_bp.route("/profile")
def profile():
    return render_template("user/profile.html")


@user_bp.route("/favorites")
def favorites():
    return render_template("user/favorites.html")


@user_bp.route("/history")
def history():
    return render_template("user/history.html")


@user_bp.route("/saved-results")
def saved_results():
    return render_template("user/saved_results.html")