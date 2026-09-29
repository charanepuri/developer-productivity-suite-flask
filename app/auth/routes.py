from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for
)

from flask_login import (
    current_user,
    login_user,
    logout_user
)

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from app.auth import auth_bp
from app.auth.forms import (
    LoginForm,
    RegistrationForm
)

from app.extensions import db
from app.models import User


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(
            url_for("dashboard.index")
        )

    form = RegistrationForm()

    if form.validate_on_submit():

        existing_username = User.query.filter_by(
            username=form.username.data.strip()
        ).first()

        if existing_username:

            flash(
                "Username is already taken.",
                "danger"
            )

            return render_template(
                "auth/register.html",
                form=form
            )

        existing_email = User.query.filter_by(
            email=form.email.data.lower().strip()
        ).first()

        if existing_email:

            flash(
                "An account with this email already exists.",
                "danger"
            )

            return render_template(
                "auth/register.html",
                form=form
            )

        user = User(
            username=form.username.data.strip(),
            email=form.email.data.lower().strip(),
            password_hash=generate_password_hash(
                form.password.data
            )
        )

        db.session.add(user)
        db.session.commit()

        flash(
            "Your account has been created successfully. Please log in.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/register.html",
        form=form
    )
    

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(
            url_for("dashboard.index")
        )

    form = LoginForm()

    if form.validate_on_submit():

        email = form.email.data.lower().strip()

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password_hash,
            form.password.data
        ):

            if not user.is_active:

                flash(
                    "Your account is inactive.",
                    "danger"
                )

                return redirect(
                    url_for("auth.login")
                )

            login_user(user)

            flash(
                "Login successful. Welcome back!",
                "success"
            )

            next_page = request.args.get("next")

            if next_page:
                return redirect(next_page)

            return redirect(
                url_for("dashboard.index")
            )

        flash(
            "Invalid email or password.",
            "danger"
        )

    return render_template(
        "auth/login.html",
        form=form
    )
    

@auth_bp.route("/logout")
def logout():

    logout_user()

    flash(
        "You have been logged out successfully.",
        "info"
    )

    return redirect(
        url_for("main.home")
    )