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

from app.tools.services.json_tools import (
    escape_json,
    format_json,
    json_to_csv,
    minify_json,
    sort_json,
    unescape_json,
    validate_json,
)

from app.tools.services.security_tools import (
    check_password_strength,
    generate_hash,
    generate_password,
    generate_random_token,
    generate_uuid,
    identify_hash,
)

from app.tools.services.css_tools import (
    format_css,
    generate_box_shadow,
    generate_flexbox,
    generate_gradient,
    minify_css,
)

from app.tools.services.color_tools import (
    convert_color,
    generate_palette,
    generate_random_palette,
    contrast_ratio,
    contrast_level,
    generate_gradient,
    normalize_hex,
)

from . import tools_bp


@tools_bp.route("/")
def index():
    """Display all categories and tools."""

    categories = Category.query.order_by(
        Category.id
    ).all()

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

    tools = Tool.query.filter_by(
        category_id=category.id,
        is_active=True,
    ).order_by(
        Tool.name
    ).all()

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

        # Text Tools
        "word-counter":
            "tools/text/word_counter.html",

        "character-counter":
            "tools/text/character_counter.html",

        "case-converter":
            "tools/text/case_converter.html",

        "remove-duplicate-lines":
            "tools/text/remove_duplicate_lines.html",

        "text-sorter":
            "tools/text/text_sorter.html",

        "text-reverser":
            "tools/text/text_reverser.html",

        # JSON Tools
        "json-formatter":
            "tools/json/json_formatter.html",

        "json-validator":
            "tools/json/json_validator.html",

        "json-minifier":
            "tools/json/json_minifier.html",

        "json-to-csv":
            "tools/json/json_to_csv.html",

        "json-sorter":
            "tools/json/json_sorter.html",

        "json-escape-unescape":
            "tools/json/json_escape_unescape.html",
            
        # Security Tools

            "password-generator":
                "tools/security/password_generator.html",

            "password-strength-checker":
                "tools/security/password_strength_checker.html",

            "hash-generator":
                "tools/security/hash_generator.html",

            "hash-identifier":
                "tools/security/hash_identifier.html",

            "uuid-generator":
                "tools/security/uuid_generator.html",

            "random-token-generator":
                "tools/security/random_token_generator.html",
                
            # CSS Tools

            "css-minifier":
                "tools/css/css_minifier.html",

            "css-formatter":
                "tools/css/css_formatter.html",

            "css-box-shadow-generator":
                "tools/css/css_box_shadow_generator.html",

            "css-gradient-generator":
                "tools/css/css_gradient_generator.html",

            "css-flexbox-generator":
                "tools/css/css_flexbox_generator.html",
                
            
    }

    template = template_map.get(
        tool.slug,
        "tools/detail.html",
    )

    return render_template(
        template,
        tool=tool,
    )


@tools_bp.route(
    "/word-counter",
    methods=["GET", "POST"],
)
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


@tools_bp.route(
    "/character-counter",
    methods=["GET", "POST"],
)
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


@tools_bp.route(
    "/case-converter",
    methods=["GET", "POST"],
)
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


@tools_bp.route(
    "/json-formatter",
    methods=["GET", "POST"],
)
def json_formatter():
    """JSON Formatter tool."""

    text = ""
    result = None
    error = None

    if request.method == "POST":
        text = request.form.get("text", "")

        try:
            result = format_json(text)

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "tools/json/json_formatter.html",
        tool_name="JSON Formatter",
        text=text,
        result=result,
        error=error,
    )


@tools_bp.route(
    "/json-validator",
    methods=["GET", "POST"],
)
def json_validator():
    """JSON Validator tool."""

    text = ""
    result = None

    if request.method == "POST":
        text = request.form.get("text", "")

        result = validate_json(text)

    return render_template(
        "tools/json/json_validator.html",
        tool_name="JSON Validator",
        text=text,
        result=result,
    )


@tools_bp.route(
    "/json-minifier",
    methods=["GET", "POST"],
)
def json_minifier():
    """JSON Minifier tool."""

    text = ""
    result = None
    error = None

    if request.method == "POST":
        text = request.form.get("text", "")

        try:
            result = minify_json(text)

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "tools/json/json_minifier.html",
        tool_name="JSON Minifier",
        text=text,
        result=result,
        error=error,
    )


@tools_bp.route(
    "/json-to-csv",
    methods=["GET", "POST"],
)
def json_to_csv_tool():
    """JSON to CSV tool."""

    text = ""
    result = None
    error = None

    if request.method == "POST":
        text = request.form.get("text", "")

        try:
            result = json_to_csv(text)

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "tools/json/json_to_csv.html",
        tool_name="JSON to CSV",
        text=text,
        result=result,
        error=error,
    )


@tools_bp.route(
    "/json-sorter",
    methods=["GET", "POST"],
)
def json_sorter():
    """JSON Sorter tool."""

    text = ""
    result = None
    error = None

    if request.method == "POST":
        text = request.form.get("text", "")

        try:
            result = sort_json(text)

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "tools/json/json_sorter.html",
        tool_name="JSON Sorter",
        text=text,
        result=result,
        error=error,
    )


@tools_bp.route(
    "/json-escape-unescape",
    methods=["GET", "POST"],
)
def json_escape_unescape():
    """JSON Escape/Unescape tool."""

    text = ""
    result = None
    error = None
    operation = "escape"

    if request.method == "POST":
        text = request.form.get("text", "")

        operation = request.form.get(
            "operation",
            "escape",
        )

        try:
            if operation == "unescape":
                result = unescape_json(text)

            else:
                result = escape_json(text)

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "tools/json/json_escape_unescape.html",
        tool_name="JSON Escape/Unescape",
        text=text,
        result=result,
        error=error,
        operation=operation,
    )
    
@tools_bp.route(
    "/password-generator",
    methods=["GET", "POST"],
)
def password_generator():
    """Password Generator tool."""

    password = None
    error = None

    length = 16
    use_uppercase = True
    use_lowercase = True
    use_digits = True
    use_symbols = True

    if request.method == "POST":

        length = request.form.get(
            "length",
            "16",
        )

        use_uppercase = (
            request.form.get("use_uppercase")
            == "on"
        )

        use_lowercase = (
            request.form.get("use_lowercase")
            == "on"
        )

        use_digits = (
            request.form.get("use_digits")
            == "on"
        )

        use_symbols = (
            request.form.get("use_symbols")
            == "on"
        )

        try:

            password = generate_password(
                length=length,
                use_uppercase=use_uppercase,
                use_lowercase=use_lowercase,
                use_digits=use_digits,
                use_symbols=use_symbols,
            )

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "tools/security/password_generator.html",
        tool_name="Password Generator",
        password=password,
        error=error,
        length=length,
        use_uppercase=use_uppercase,
        use_lowercase=use_lowercase,
        use_digits=use_digits,
        use_symbols=use_symbols,
    )
    
@tools_bp.route(
    "/password-strength-checker",
    methods=["GET", "POST"],
)
def password_strength_checker():
    """Password Strength Checker tool."""

    password = ""
    result = None

    if request.method == "POST":

        password = request.form.get(
            "password",
            "",
        )

        result = check_password_strength(
            password
        )

    return render_template(
        "tools/security/password_strength_checker.html",
        tool_name="Password Strength Checker",
        password=password,
        result=result,
    )
    
@tools_bp.route(
    "/hash-generator",
    methods=["GET", "POST"],
)
def hash_generator():
    """Hash Generator tool."""

    text = ""
    algorithm = "sha256"
    result = None
    error = None

    if request.method == "POST":

        text = request.form.get(
            "text",
            "",
        )

        algorithm = request.form.get(
            "algorithm",
            "sha256",
        )

        try:

            result = generate_hash(
                text,
                algorithm,
            )

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "tools/security/hash_generator.html",
        tool_name="Hash Generator",
        text=text,
        algorithm=algorithm,
        result=result,
        error=error,
    )
    
@tools_bp.route(
    "/hash-identifier",
    methods=["GET", "POST"],
)
def hash_identifier():
    """Hash Identifier tool."""

    hash_value = ""
    result = None

    if request.method == "POST":

        hash_value = request.form.get(
            "hash_value",
            "",
        )

        result = identify_hash(
            hash_value
        )

    return render_template(
        "tools/security/hash_identifier.html",
        tool_name="Hash Identifier",
        hash_value=hash_value,
        result=result,
    )
    
@tools_bp.route(
    "/uuid-generator",
    methods=["GET", "POST"],
)
def uuid_generator():
    """UUID Generator tool."""

    version = "4"
    count = 1
    result = None
    error = None

    if request.method == "POST":

        version = request.form.get(
            "version",
            "4",
        )

        count = request.form.get(
            "count",
            "1",
        )

        try:

            result = generate_uuid(
                version=version,
                count=count,
            )

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "tools/security/uuid_generator.html",
        tool_name="UUID Generator",
        version=version,
        count=count,
        result=result,
        error=error,
    )
    
@tools_bp.route(
    "/random-token-generator",
    methods=["GET", "POST"],
)
def random_token_generator():
    """Random Token Generator tool."""

    length = 32
    result = None
    error = None

    if request.method == "POST":

        length = request.form.get(
            "length",
            "32",
        )

        try:

            result = generate_random_token(
                length
            )

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "tools/security/random_token_generator.html",
        tool_name="Random Token Generator",
        length=length,
        result=result,
        error=error,
    )
    
@tools_bp.route(
    "/css-minifier",
    methods=["GET", "POST"],
)
def css_minifier():
    """CSS Minifier tool."""

    text = ""
    result = None
    error = None

    if request.method == "POST":

        text = request.form.get(
            "text",
            "",
        )

        try:
            result = minify_css(text)

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "tools/css/css_minifier.html",
        tool_name="CSS Minifier",
        text=text,
        result=result,
        error=error,
    )
    
@tools_bp.route(
    "/css-formatter",
    methods=["GET", "POST"],
)
def css_formatter():
    """CSS Formatter tool."""

    text = ""
    result = None
    error = None

    if request.method == "POST":

        text = request.form.get(
            "text",
            "",
        )

        try:
            result = format_css(text)

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "tools/css/css_formatter.html",
        tool_name="CSS Formatter",
        text=text,
        result=result,
        error=error,
    )
    
@tools_bp.route(
    "/css-box-shadow-generator",
    methods=["GET", "POST"],
)
def css_box_shadow_generator():
    """CSS Box Shadow Generator."""

    horizontal = 0
    vertical = 10
    blur = 20
    spread = 0
    color = "rgba(0, 0, 0, 0.2)"
    inset = False

    result = None
    error = None

    if request.method == "POST":

        horizontal = request.form.get(
            "horizontal",
            "0",
        )

        vertical = request.form.get(
            "vertical",
            "10",
        )

        blur = request.form.get(
            "blur",
            "20",
        )

        spread = request.form.get(
            "spread",
            "0",
        )

        color = request.form.get(
            "color",
            "rgba(0, 0, 0, 0.2)",
        )

        inset = (
            request.form.get("inset")
            == "on"
        )

        try:

            result = generate_box_shadow(
                horizontal=horizontal,
                vertical=vertical,
                blur=blur,
                spread=spread,
                color=color,
                inset=inset,
            )

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "tools/css/css_box_shadow_generator.html",
        tool_name="CSS Box Shadow Generator",
        horizontal=horizontal,
        vertical=vertical,
        blur=blur,
        spread=spread,
        color=color,
        inset=inset,
        result=result,
        error=error,
    )
    
@tools_bp.route(
    "/css-gradient-generator",
    methods=["GET", "POST"],
)
def css_gradient_generator():
    """CSS Gradient Generator."""

    gradient_type = "linear"
    direction = "to right"
    color1 = "#6a11cb"
    color2 = "#2575fc"

    result = None
    error = None

    if request.method == "POST":

        gradient_type = request.form.get(
            "gradient_type",
            "linear",
        )

        direction = request.form.get(
            "direction",
            "to right",
        )

        color1 = request.form.get(
            "color1",
            "#6a11cb",
        )

        color2 = request.form.get(
            "color2",
            "#2575fc",
        )

        try:

            result = generate_gradient(
                gradient_type=gradient_type,
                direction=direction,
                color1=color1,
                color2=color2,
            )

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "tools/css/css_gradient_generator.html",
        tool_name="CSS Gradient Generator",
        gradient_type=gradient_type,
        direction=direction,
        color1=color1,
        color2=color2,
        result=result,
        error=error,
    )
    
@tools_bp.route(
    "/css-flexbox-generator",
    methods=["GET", "POST"],
)
def css_flexbox_generator():
    """CSS Flexbox Generator."""

    direction = "row"
    justify_content = "flex-start"
    align_items = "stretch"
    flex_wrap = "nowrap"
    gap = 0

    result = None
    error = None

    if request.method == "POST":

        direction = request.form.get(
            "direction",
            "row",
        )

        justify_content = request.form.get(
            "justify_content",
            "flex-start",
        )

        align_items = request.form.get(
            "align_items",
            "stretch",
        )

        flex_wrap = request.form.get(
            "flex_wrap",
            "nowrap",
        )

        gap = request.form.get(
            "gap",
            "0",
        )

        try:

            result = generate_flexbox(
                direction=direction,
                justify_content=justify_content,
                align_items=align_items,
                flex_wrap=flex_wrap,
                gap=gap,
            )

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "tools/css/css_flexbox_generator.html",
        tool_name="CSS Flexbox Generator",
        direction=direction,
        justify_content=justify_content,
        align_items=align_items,
        flex_wrap=flex_wrap,
        gap=gap,
        result=result,
        error=error,
    )
    
@tools_bp.route("/color-converter", methods=["GET", "POST"])
def color_converter():
    result = None
    error = None

    if request.method == "POST":
        color = request.form.get("color", "").strip()

        try:
            result = convert_color(color)
        except ValueError as exc:
            error = str(exc)

    return render_template(
        "tools/color/color_converter.html",
        result=result,
        error=error,
    )
    
@tools_bp.route("/color-picker", methods=["GET", "POST"])
def color_picker():
    selected_color = "#6A11CB"
    color_info = None

    if request.method == "POST":
        selected_color = request.form.get(
            "color",
            "#6A11CB",
        )

        try:
            color_info = convert_color(selected_color)
        except ValueError:
            color_info = None

    return render_template(
        "tools/color/color_picker.html",
        selected_color=selected_color,
        color_info=color_info,
    )
    
@tools_bp.route(
    "/color-palette-generator",
    methods=["GET", "POST"],
)
def color_palette_generator():
    palette = None
    base_color = "#6A11CB"
    count = 5
    mode = "base"

    if request.method == "POST":
        mode = request.form.get("mode", "base")

        try:
            count = int(request.form.get("count", 5))
            count = max(2, min(count, 10))
        except ValueError:
            count = 5

        if mode == "random":
            palette = generate_random_palette(count)
        else:
            base_color = request.form.get(
                "base_color",
                "#6A11CB",
            )

            try:
                palette = generate_palette(
                    base_color,
                    count,
                )
            except ValueError:
                palette = None

    return render_template(
        "tools/color/color_palette_generator.html",
        palette=palette,
        base_color=base_color,
        count=count,
        mode=mode,
    )
    
@tools_bp.route(
    "/contrast-checker",
    methods=["GET", "POST"],
)
def contrast_checker():
    result = None
    foreground = "#FFFFFF"
    background = "#000000"

    if request.method == "POST":
        foreground = request.form.get(
            "foreground",
            "#FFFFFF",
        )

        background = request.form.get(
            "background",
            "#000000",
        )

        try:
            ratio = contrast_ratio(
                foreground,
                background,
            )

            result = {
                "ratio": ratio,
                "level": contrast_level(ratio),
            }
        except ValueError:
            result = None

    return render_template(
        "tools/color/contrast_checker.html",
        result=result,
        foreground=foreground,
        background=background,
    )
    
@tools_bp.route(
    "/gradient-generator",
    methods=["GET", "POST"],
)
def gradient_generator():
    result = None

    color1 = "#6A11CB"
    color2 = "#2575FC"
    gradient_type = "linear"
    direction = "to right"

    if request.method == "POST":
        color1 = request.form.get(
            "color1",
            "#6A11CB",
        )

        color2 = request.form.get(
            "color2",
            "#2575FC",
        )

        gradient_type = request.form.get(
            "gradient_type",
            "linear",
        )

        direction = request.form.get(
            "direction",
            "to right",
        )

        try:
            result = generate_gradient(
                color1,
                color2,
                gradient_type,
                direction,
            )
        except ValueError:
            result = None

    return render_template(
        "tools/color/gradient_generator.html",
        result=result,
        color1=color1,
        color2=color2,
        gradient_type=gradient_type,
        direction=direction,
    )