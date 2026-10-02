import re

import markdown


def markdown_to_html(text):
    """
    Convert Markdown text to HTML.
    """
    return markdown.markdown(
        text,
        extensions=[
            "extra",
            "tables",
            "fenced_code",
            "toc",
        ],
    )


def format_markdown(text):
    """
    Apply basic formatting normalization to Markdown.
    """
    if not text:
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove trailing spaces from every line.
    lines = [
        line.rstrip()
        for line in text.split("\n")
    ]

    formatted_lines = []
    previous_blank = False

    for line in lines:
        stripped = line.strip()

        # Normalize unordered list markers.
        if re.match(r"^[-+*]\s+", stripped):
            line = re.sub(
                r"^(\s*)[-+*]\s+",
                r"\1- ",
                line,
            )

        # Normalize heading spacing.
        line = re.sub(
            r"^(#{1,6})([^ #])",
            r"\1 \2",
            line,
        )

        # Prevent excessive consecutive blank lines.
        if not stripped:
            if previous_blank:
                continue

            previous_blank = True
        else:
            previous_blank = False

        formatted_lines.append(line)

    return "\n".join(formatted_lines).strip()


def generate_markdown_table(headers, rows):
    """
    Generate a Markdown table from headers and rows.
    """
    headers = [
        str(header).strip()
        for header in headers
    ]

    cleaned_rows = []

    for row in rows:
        cleaned_rows.append([
            str(cell).strip().replace("|", "\\|")
            for cell in row
        ])

    header_line = (
        "| "
        + " | ".join(headers)
        + " |"
    )

    separator_line = (
        "| "
        + " | ".join("---" for _ in headers)
        + " |"
    )

    table_rows = [
        "| "
        + " | ".join(row)
        + " |"
        for row in cleaned_rows
    ]

    return "\n".join(
        [header_line, separator_line, *table_rows]
    )


def parse_table_input(header_text, row_text):
    """
    Parse newline-separated table input.
    """
    headers = [
        item.strip()
        for item in header_text.split(",")
        if item.strip()
    ]

    rows = []

    for line in row_text.splitlines():
        if not line.strip():
            continue

        cells = [
            item.strip()
            for item in line.split(",")
        ]

        rows.append(cells)

    return headers, rows


def create_markdown_document(title, body):
    """
    Create a simple Markdown document.
    """
    title = title.strip()
    body = body.strip()

    if not title:
        return body

    if not body:
        return f"# {title}"

    return f"# {title}\n\n{body}"