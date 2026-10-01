from flask import render_template

from app.models import Category, Tool
from . import tools_bp


@tools_bp.route("/")
def index():
    """Display all categories and tools."""
    categories = (
        Category.query
        .filter_by()
        .order_by(Category.id)
        .all()
    )

    return render_template(
        "tools/index.html",
        categories=categories,
    )


@tools_bp.route("/category/<slug>")
def category_detail(slug):
    """Display tools belonging to a category."""
    category = Category.query.filter_by(
        slug=slug
    ).first_or_404()

    tools = (
        Tool.query
        .filter_by(
            category_id=category.id,
            is_active=True,
        )
        .order_by(Tool.name)
        .all()
    )

    return render_template(
        "tools/category.html",
        category=category,
        tools=tools,
    )


@tools_bp.route("/<slug>")
def tool_detail(slug):
    """Display an individual tool."""
    tool = Tool.query.filter_by(
        slug=slug,
        is_active=True,
    ).first_or_404()

    return render_template(
        "tools/detail.html",
        tool=tool,
    )