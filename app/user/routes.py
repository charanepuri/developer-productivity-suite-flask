from flask import render_template

from app.user import user_bp

from flask_login import login_required , current_user

from app.models import Favorite

@user_bp.route("/profile")
@login_required
def profile():
    return render_template("user/profile.html")


@user_bp.route("/favorites")
@login_required
def favorites():
    favorites = (
        Favorite.query
        .filter_by(user_id=current_user.id)
        .order_by(Favorite.created_at.desc())
        .all()
    )

    return render_template(
        "user/favorites.html",
        favorites=favorites,
    )


@user_bp.route("/history")
def history():
    return render_template("user/history.html")


@user_bp.route("/saved-results")
def saved_results():
    return render_template("user/saved_results.html")