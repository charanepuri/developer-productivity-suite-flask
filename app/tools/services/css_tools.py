import re


def minify_css(css):
    """Minify CSS by removing unnecessary whitespace and comments."""

    if css is None:
        return ""

    if not css.strip():
        raise ValueError("CSS input cannot be empty.")

    # Remove CSS comments.
    css = re.sub(
        r"/\*.*?\*/",
        "",
        css,
        flags=re.DOTALL,
    )

    # Remove unnecessary whitespace.
    css = re.sub(r"\s+", " ", css)

    # Remove spaces around CSS syntax characters.
    css = re.sub(r"\s*([{}:;,>+~])\s*", r"\1", css)

    # Remove the final semicolon before a closing brace.
    css = re.sub(r";}", "}", css)

    return css.strip()


def format_css(css):
    """Format CSS into a readable structure."""

    if css is None:
        return ""

    if not css.strip():
        raise ValueError("CSS input cannot be empty.")

    # Remove existing comments.
    css = re.sub(
        r"/\*.*?\*/",
        "",
        css,
        flags=re.DOTALL,
    )

    # Normalize whitespace.
    css = re.sub(r"\s+", " ", css)

    # Format braces.
    css = re.sub(
        r"\s*\{\s*",
        " {\n    ",
        css,
    )

    css = re.sub(
        r"\s*;\s*",
        ";\n    ",
        css,
    )

    css = re.sub(
        r"\s*\}\s*",
        "\n}\n\n",
        css,
    )

    # Clean up indentation before closing braces.
    css = re.sub(
        r"\n\s*\}",
        "\n}",
        css,
    )

    # Clean extra whitespace.
    lines = []

    for line in css.splitlines():

        line = line.rstrip()

        if line.strip():
            lines.append(line)

    return "\n".join(lines).strip()


def generate_box_shadow(
    horizontal=0,
    vertical=10,
    blur=20,
    spread=0,
    color="rgba(0, 0, 0, 0.2)",
    inset=False,
):
    """Generate a CSS box-shadow declaration."""

    try:
        horizontal = int(horizontal)
        vertical = int(vertical)
        blur = int(blur)
        spread = int(spread)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "Shadow values must be valid numbers."
        ) from exc

    if not color.strip():
        raise ValueError(
            "Shadow color cannot be empty."
        )

    prefix = "inset " if inset else ""

    shadow = (
        f"{prefix}"
        f"{horizontal}px "
        f"{vertical}px "
        f"{blur}px "
        f"{spread}px "
        f"{color}"
    )

    return f"box-shadow: {shadow};"


def generate_gradient(
    gradient_type="linear",
    direction="to right",
    color1="#6a11cb",
    color2="#2575fc",
):
    """Generate a CSS gradient declaration."""

    if not color1.strip() or not color2.strip():
        raise ValueError(
            "Both gradient colors are required."
        )

    gradient_type = gradient_type.lower()

    if gradient_type == "radial":

        value = (
            f"radial-gradient("
            f"circle, "
            f"{color1}, "
            f"{color2}"
            f")"
        )

    elif gradient_type == "linear":

        value = (
            f"linear-gradient("
            f"{direction}, "
            f"{color1}, "
            f"{color2}"
            f")"
        )

    else:
        raise ValueError(
            "Gradient type must be linear or radial."
        )

    return f"background: {value};"


def generate_flexbox(
    direction="row",
    justify_content="flex-start",
    align_items="stretch",
    flex_wrap="nowrap",
    gap=0,
):
    """Generate CSS Flexbox properties."""

    allowed_directions = {
        "row",
        "row-reverse",
        "column",
        "column-reverse",
    }

    allowed_justify = {
        "flex-start",
        "center",
        "flex-end",
        "space-between",
        "space-around",
        "space-evenly",
    }

    allowed_align = {
        "stretch",
        "flex-start",
        "center",
        "flex-end",
        "baseline",
    }

    allowed_wrap = {
        "nowrap",
        "wrap",
        "wrap-reverse",
    }

    if direction not in allowed_directions:
        raise ValueError(
            "Invalid flex direction."
        )

    if justify_content not in allowed_justify:
        raise ValueError(
            "Invalid justify-content value."
        )

    if align_items not in allowed_align:
        raise ValueError(
            "Invalid align-items value."
        )

    if flex_wrap not in allowed_wrap:
        raise ValueError(
            "Invalid flex-wrap value."
        )

    try:
        gap = int(gap)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "Gap must be a valid number."
        ) from exc

    if gap < 0:
        raise ValueError(
            "Gap cannot be negative."
        )

    return (
        ".container {\n"
        "    display: flex;\n"
        f"    flex-direction: {direction};\n"
        f"    justify-content: {justify_content};\n"
        f"    align-items: {align_items};\n"
        f"    flex-wrap: {flex_wrap};\n"
        f"    gap: {gap}px;\n"
        "}"
    )