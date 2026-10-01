from flask import render_template, request

from app.models import Category, Tool
from app.tools.services.text_tools import (
    count_characters,
    count_words,
    convert_case,
    remove_duplicate_lines,
    reverse_text,
    sort_lines,
)

from . import tools_bp


@tools_bp.route("/")
def index():
    """Display all categories and tools."""

    categories = (
        Category.query
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


@tools_bp.route("/tool/<slug>")
def tool_detail(slug):
    """Display an individual tool."""

    tool = Tool.query.filter_by(
        slug=slug,
        is_active=True,
    ).first_or_404()

    template_map = {
        "word-counter": "tools/text/word_counter.html",
        "character-counter": "tools/text/character_counter.html",
        "case-converter": "tools/text/case_converter.html",
        "remove-duplicate-lines": "tools/text/remove_duplicate_lines.html",
        "text-sorter": "tools/text/text_sorter.html",
        "text-reverser": "tools/text/text_reverser.html",
    }

    template = template_map.get(
        tool.slug,
        "tools/detail.html",
    )

    return render_template(
        template,
        tool=tool,
    )


@tools_bp.route("/word-counter", methods=["GET", "POST"])
def word_counter():
    """Word Counter tool."""

    text = ""
    result = None

    if request.method == "POST":
        text = request.form.get("text", "")
        result = count_words(text)

    return render_template(
        "tools/text/word_counter.html",
        tool_name="Word Counter",
        text=text,
        result=result,
    )


@tools_bp.route("/character-counter", methods=["GET", "POST"])
def character_counter():
    """Character Counter tool."""

    text = ""
    result = None
    include_spaces = True

    if request.method == "POST":
        text = request.form.get("text", "")
        include_spaces = request.form.get(
            "include_spaces"
        ) == "on"

        result = count_characters(
            text,
            include_spaces,
        )

    return render_template(
        "tools/text/character_counter.html",
        tool_name="Character Counter",
        text=text,
        result=result,
        include_spaces=include_spaces,
    )


@tools_bp.route("/case-converter", methods=["GET", "POST"])
def case_converter():
    """Case Converter tool."""

    text = ""
    result = None
    case_type = "uppercase"

    if request.method == "POST":
        text = request.form.get("text", "")
        case_type = request.form.get(
            "case_type",
            "uppercase",
        )

        result = convert_case(
            text,
            case_type,
        )

    return render_template(
        "tools/text/case_converter.html",
        tool_name="Case Converter",
        text=text,
        result=result,
        case_type=case_type,
    )


@tools_bp.route(
    "/remove-duplicate-lines",
    methods=["GET", "POST"],
)
def duplicate_lines():
    """Remove Duplicate Lines tool."""

    text = ""
    result = None

    if request.method == "POST":
        text = request.form.get("text", "")
        result = remove_duplicate_lines(text)

    return render_template(
        "tools/text/remove_duplicate_lines.html",
        tool_name="Remove Duplicate Lines",
        text=text,
        result=result,
    )


@tools_bp.route(
    "/text-sorter",
    methods=["GET", "POST"],
)
def text_sorter():
    """Text Sorter tool."""

    text = ""
    result = None

    reverse = False
    ignore_case = False

    if request.method == "POST":
        text = request.form.get("text", "")

        reverse = request.form.get("reverse") == "on"
        ignore_case = request.form.get("ignore_case") == "on"

        result = sort_lines(
            text,
            reverse=reverse,
            ignore_case=ignore_case,
        )

    return render_template(
        "tools/text/text_sorter.html",
        tool_name="Text Sorter",
        text=text,
        result=result,
        reverse=reverse,
        ignore_case=ignore_case,
    )


@tools_bp.route(
    "/text-reverser",
    methods=["GET", "POST"],
)
def text_reverser():
    """Text Reverser tool."""

    text = ""
    result = None
    mode = "characters"

    if request.method == "POST":
        text = request.form.get("text", "")
        mode = request.form.get(
            "mode",
            "characters",
        )

        result = reverse_text(
            text,
            mode,
        )

    return render_template(
        "tools/text/text_reverser.html",
        tool_name="Text Reverser",
        text=text,
        result=result,
        mode=mode,
    )