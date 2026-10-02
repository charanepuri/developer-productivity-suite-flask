from flask import render_template, request , send_file

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

from app.tools.services.markdown_tools import (
    markdown_to_html,
    format_markdown,
    generate_markdown_table,
    parse_table_input,
    create_markdown_document,
)

from app.tools.services.developer_tools import (
    test_regex,
    timestamp_to_datetime,
    datetime_to_timestamp,
    generate_lorem,
    generate_qr_code,
    compare_texts,
    format_code,
)

from app.tools.services.date_time_tools import (
    timestamp_to_datetime,
    datetime_to_timestamp,
    calculate_date_difference,
    get_timezone_names,
    convert_timezone,
    calculate_age,
)

from app.tools.services.api_tools import (
    parse_headers,
    parse_request_body,
    make_api_request,
    get_status_code_info,
    generate_curl_command,
    format_api_response,
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
    
@tools_bp.route(
    "/markdown-editor",
    methods=["GET", "POST"],
)
def markdown_editor():
    markdown_content = ""
    preview_html = None

    if request.method == "POST":
        markdown_content = request.form.get(
            "markdown_content",
            "",
        )

        preview_html = markdown_to_html(
            markdown_content
        )

    return render_template(
        "tools/markdown/markdown_editor.html",
        markdown_content=markdown_content,
        preview_html=preview_html,
    )
    
@tools_bp.route(
    "/markdown-previewer",
    methods=["GET", "POST"],
)
def markdown_previewer():
    markdown_content = ""
    preview_html = None

    if request.method == "POST":
        markdown_content = request.form.get(
            "markdown_content",
            "",
        )

        preview_html = markdown_to_html(
            markdown_content
        )

    return render_template(
        "tools/markdown/markdown_previewer.html",
        markdown_content=markdown_content,
        preview_html=preview_html,
    )
    
@tools_bp.route(
    "/markdown-to-html",
    methods=["GET", "POST"],
)
def markdown_to_html_tool():
    markdown_content = ""
    html_output = None

    if request.method == "POST":
        markdown_content = request.form.get(
            "markdown_content",
            "",
        )

        html_output = markdown_to_html(
            markdown_content
        )

    return render_template(
        "tools/markdown/markdown_to_html.html",
        markdown_content=markdown_content,
        html_output=html_output,
    )
    
@tools_bp.route(
    "/markdown-formatter",
    methods=["GET", "POST"],
)
def markdown_formatter():
    markdown_content = ""
    formatted_content = None

    if request.method == "POST":
        markdown_content = request.form.get(
            "markdown_content",
            "",
        )

        formatted_content = format_markdown(
            markdown_content
        )

    return render_template(
        "tools/markdown/markdown_formatter.html",
        markdown_content=markdown_content,
        formatted_content=formatted_content,
    )
    
@tools_bp.route(
    "/markdown-table-generator",
    methods=["GET", "POST"],
)
def markdown_table_generator():
    headers_text = ""
    rows_text = ""
    table_output = None

    if request.method == "POST":
        headers_text = request.form.get(
            "headers",
            "",
        )

        rows_text = request.form.get(
            "rows",
            "",
        )

        headers, rows = parse_table_input(
            headers_text,
            rows_text,
        )

        if headers:
            table_output = generate_markdown_table(
                headers,
                rows,
            )

    return render_template(
        "tools/markdown/markdown_table_generator.html",
        headers_text=headers_text,
        rows_text=rows_text,
        table_output=table_output,
    )
    
@tools_bp.route(
    "/regex-tester",
    methods=["GET", "POST"],
)
def regex_tester():
    pattern = ""
    text = ""
    result = None

    if request.method == "POST":
        pattern = request.form.get(
            "pattern",
            "",
        )

        text = request.form.get(
            "text",
            "",
        )

        result = test_regex(
            pattern,
            text,
        )

    return render_template(
        "tools/developer/regex_tester.html",
        pattern=pattern,
        text=text,
        result=result,
    )
    
@tools_bp.route(
    "/timestamp-converter",
    methods=["GET", "POST"],
)
def timestamp_converter():
    timestamp_result = None
    datetime_result = None
    error = None

    if request.method == "POST":

        conversion_type = request.form.get(
            "conversion_type",
            "timestamp_to_datetime",
        )

        try:
            if conversion_type == "timestamp_to_datetime":

                timestamp = request.form.get(
                    "timestamp",
                    "",
                )

                timestamp_result = timestamp_to_datetime(
                    timestamp
                )

            else:

                date_string = request.form.get(
                    "datetime",
                    "",
                )

                datetime_result = datetime_to_timestamp(
                    date_string
                )

        except (ValueError, TypeError, OverflowError) as exc:
            error = str(exc)

    return render_template(
        "tools/developer/timestamp_converter.html",
        timestamp_result=timestamp_result,
        datetime_result=datetime_result,
        error=error,
    )
    
@tools_bp.route(
    "/lorem-ipsum-generator",
    methods=["GET", "POST"],
)
def lorem_ipsum_generator():
    generated_text = None
    paragraphs = 2
    sentences = 3

    if request.method == "POST":

        try:
            paragraphs = int(
                request.form.get(
                    "paragraphs",
                    2,
                )
            )

            sentences = int(
                request.form.get(
                    "sentences",
                    3,
                )
            )

        except ValueError:
            paragraphs = 2
            sentences = 3

        generated_text = generate_lorem(
            paragraphs,
            sentences,
        )

    return render_template(
        "tools/developer/lorem_ipsum_generator.html",
        generated_text=generated_text,
        paragraphs=paragraphs,
        sentences=sentences,
    )
    
@tools_bp.route(
    "/qr-code-generator",
    methods=["GET", "POST"],
)
def qr_code_generator():
    qr_data = ""
    qr_generated = False

    if request.method == "POST":

        qr_data = request.form.get(
            "data",
            "",
        ).strip()

        if qr_data:
            qr_generated = True

    return render_template(
        "tools/developer/qr_code_generator.html",
        qr_data=qr_data,
        qr_generated=qr_generated,
    )
    
@tools_bp.route(
    "/diff-checker",
    methods=["GET", "POST"],
)
def diff_checker():
    original_text = ""
    modified_text = ""
    diff_html = None

    if request.method == "POST":

        original_text = request.form.get(
            "original_text",
            "",
        )

        modified_text = request.form.get(
            "modified_text",
            "",
        )

        diff_html = compare_texts(
            original_text,
            modified_text,
        )

    return render_template(
        "tools/developer/diff_checker.html",
        original_text=original_text,
        modified_text=modified_text,
        diff_html=diff_html,
    )
    
@tools_bp.route(
    "/code-formatter",
    methods=["GET", "POST"],
)
def code_formatter():
    code = ""
    formatted_code = None
    language = "python"
    error = None

    if request.method == "POST":

        code = request.form.get(
            "code",
            "",
        )

        language = request.form.get(
            "language",
            "python",
        )

        result = format_code(
            code,
            language,
        )

        formatted_code = result["code"]
        error = result["error"]

    return render_template(
        "tools/developer/code_formatter.html",
        code=code,
        formatted_code=formatted_code,
        language=language,
        error=error,
    )
    
@tools_bp.route(
    "/unix-timestamp-converter",
    methods=["GET", "POST"],
)
def unix_timestamp_converter():
    timestamp_result = None
    datetime_result = None
    error = None

    if request.method == "POST":

        conversion_type = request.form.get(
            "conversion_type",
            "timestamp_to_datetime",
        )

        try:

            if conversion_type == "timestamp_to_datetime":

                timestamp = request.form.get(
                    "timestamp",
                    "",
                )

                timestamp_result = (
                    timestamp_to_datetime(timestamp)
                )

            else:

                date_string = request.form.get(
                    "datetime",
                    "",
                )

                datetime_result = (
                    datetime_to_timestamp(
                        date_string
                    )
                )

        except (
            ValueError,
            TypeError,
            OverflowError,
        ) as exc:

            error = str(exc)

    return render_template(
        "tools/date_time/unix_timestamp_converter.html",
        timestamp_result=timestamp_result,
        datetime_result=datetime_result,
        error=error,
    )
    
@tools_bp.route(
    "/date-difference-calculator",
    methods=["GET", "POST"],
)
def date_difference_calculator():
    result = None
    error = None

    start_date = ""
    end_date = ""

    if request.method == "POST":

        start_date = request.form.get(
            "start_date",
            "",
        )

        end_date = request.form.get(
            "end_date",
            "",
        )

        try:

            result = calculate_date_difference(
                start_date,
                end_date,
            )

        except ValueError as exc:

            error = str(exc)

    return render_template(
        "tools/date_time/date_difference_calculator.html",
        result=result,
        error=error,
        start_date=start_date,
        end_date=end_date,
    )
    
@tools_bp.route(
    "/time-zone-converter",
    methods=["GET", "POST"],
)
def time_zone_converter():
    result = None
    error = None

    timezones = get_timezone_names()

    date_string = ""
    source_timezone = "Asia/Kolkata"
    target_timezone = "UTC"

    if request.method == "POST":

        date_string = request.form.get(
            "datetime",
            "",
        )

        source_timezone = request.form.get(
            "source_timezone",
            "Asia/Kolkata",
        )

        target_timezone = request.form.get(
            "target_timezone",
            "UTC",
        )

        try:

            result = convert_timezone(
                date_string,
                source_timezone,
                target_timezone,
            )

        except (
            ValueError,
            KeyError,
        ) as exc:

            error = str(exc)

    return render_template(
        "tools/date_time/time_zone_converter.html",
        result=result,
        error=error,
        timezones=timezones,
        date_string=date_string,
        source_timezone=source_timezone,
        target_timezone=target_timezone,
    )
    
@tools_bp.route(
    "/age-calculator",
    methods=["GET", "POST"],
)
def age_calculator():
    result = None
    error = None

    birth_date = ""
    reference_date = ""

    if request.method == "POST":

        birth_date = request.form.get(
            "birth_date",
            "",
        )

        reference_date = request.form.get(
            "reference_date",
            "",
        )

        try:

            result = calculate_age(
                birth_date,
                reference_date or None,
            )

        except ValueError as exc:

            error = str(exc)

    return render_template(
        "tools/date_time/age_calculator.html",
        result=result,
        error=error,
        birth_date=birth_date,
        reference_date=reference_date,
    )
    
@tools_bp.route(
    "/api-request-builder",
    methods=["GET", "POST"],
)
def api_request_builder():
    url = ""
    method = "GET"
    headers_text = ""
    body_text = ""

    result = None
    error = None

    if request.method == "POST":

        url = request.form.get(
            "url",
            "",
        ).strip()

        method = request.form.get(
            "method",
            "GET",
        ).upper()

        headers_text = request.form.get(
            "headers",
            "",
        )

        body_text = request.form.get(
            "body",
            "",
        )

        try:
            headers = parse_headers(
                headers_text
            )

            body = parse_request_body(
                body_text
            )

            result = make_api_request(
                url=url,
                method=method,
                headers=headers,
                body=body,
            )

        except Exception as exc:
            error = str(exc)

    return render_template(
        "tools/api/api_request_builder.html",
        url=url,
        method=method,
        headers_text=headers_text,
        body_text=body_text,
        result=result,
        error=error,
    )
    
@tools_bp.route(
    "/http-status-code-lookup",
    methods=["GET", "POST"],
)
def http_status_code_lookup():
    status_code = ""
    result = None

    if request.method == "POST":

        status_code = request.form.get(
            "status_code",
            "",
        )

        result = get_status_code_info(
            status_code
        )

    return render_template(
        "tools/api/http_status_code_lookup.html",
        status_code=status_code,
        result=result,
    )
    
@tools_bp.route(
    "/curl-generator",
    methods=["GET", "POST"],
)
def curl_generator():
    url = ""
    method = "GET"
    headers_text = ""
    body_text = ""
    curl_command = None
    error = None

    if request.method == "POST":

        url = request.form.get(
            "url",
            "",
        ).strip()

        method = request.form.get(
            "method",
            "GET",
        ).upper()

        headers_text = request.form.get(
            "headers",
            "",
        )

        body_text = request.form.get(
            "body",
            "",
        )

        try:
            headers = parse_headers(
                headers_text
            )

            body = parse_request_body(
                body_text
            )

            curl_command = generate_curl_command(
                url=url,
                method=method,
                headers=headers,
                body=body,
            )

        except Exception as exc:
            error = str(exc)

    return render_template(
        "tools/api/curl_generator.html",
        url=url,
        method=method,
        headers_text=headers_text,
        body_text=body_text,
        curl_command=curl_command,
        error=error,
    )
    
@tools_bp.route(
    "/api-response-formatter",
    methods=["GET", "POST"],
)
def api_response_formatter():
    response_text = ""
    result = None

    if request.method == "POST":

        response_text = request.form.get(
            "response",
            "",
        )

        result = format_api_response(
            response_text
        )

    return render_template(
        "tools/api/api_response_formatter.html",
        response_text=response_text,
        result=result,
    )
    
