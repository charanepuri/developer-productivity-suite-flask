import difflib
import io
import random
import re
import string
from datetime import datetime, timezone

import black
import qrcode


def test_regex(pattern, text, flags=0):
    """
    Test a regular expression against text.
    """
    try:
        compiled_pattern = re.compile(pattern, flags)

        matches = []

        for match in compiled_pattern.finditer(text):
            matches.append(
                {
                    "match": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                    "groups": match.groups(),
                }
            )

        return {
            "valid": True,
            "matches": matches,
            "count": len(matches),
        }

    except re.error as exc:
        return {
            "valid": False,
            "error": str(exc),
            "matches": [],
            "count": 0,
        }


def timestamp_to_datetime(timestamp):
    """
    Convert Unix timestamp to UTC datetime.
    """
    timestamp = float(timestamp)

    return datetime.fromtimestamp(
        timestamp,
        tz=timezone.utc,
    )


def datetime_to_timestamp(date_string):
    """
    Convert ISO datetime string to Unix timestamp.
    """
    normalized = date_string.strip()

    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"

    parsed = datetime.fromisoformat(normalized)

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    return int(parsed.timestamp())


def generate_lorem(
    paragraphs=1,
    sentences_per_paragraph=3,
):
    """
    Generate deterministic placeholder Lorem Ipsum text.
    """
    paragraphs = max(1, min(int(paragraphs), 20))
    sentences_per_paragraph = max(
        1,
        min(int(sentences_per_paragraph), 20),
    )

    sentence_bank = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Integer feugiat neque vitae sem tincidunt, sed consequat.",
        "Praesent malesuada turpis at sapien tincidunt posuere.",
        "Vestibulum ante ipsum primis in faucibus orci luctus.",
        "Curabitur consequat magna sed lorem facilisis elementum.",
        "Mauris tincidunt erat vitae libero aliquet vestibulum.",
        "Suspendisse potenti sed lectus gravida consectetur.",
        "Donec vulputate massa non lorem consequat, vitae posuere.",
    ]

    generated_paragraphs = []

    for _ in range(paragraphs):
        sentences = random.choices(
            sentence_bank,
            k=sentences_per_paragraph,
        )

        generated_paragraphs.append(
            " ".join(sentences)
        )

    return "\n\n".join(generated_paragraphs)


def generate_qr_code(data):
    """
    Generate a QR code PNG in memory.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    image = qr.make_image(
        fill_color="black",
        back_color="white",
    )

    image_buffer = io.BytesIO()
    image.save(image_buffer, format="PNG")
    image_buffer.seek(0)

    return image_buffer


def compare_texts(text1, text2):
    """
    Compare two text inputs and return an HTML diff.
    """
    diff = difflib.HtmlDiff(
        tabsize=4,
        wrapcolumn=80,
    )

    html = diff.make_table(
        text1.splitlines(),
        text2.splitlines(),
        fromdesc="Original",
        todesc="Modified",
        context=True,
        numlines=3,
    )

    return html


def format_python_code(code):
    """
    Format Python code using Black.
    """
    try:
        formatted = black.format_str(
            code,
            mode=black.Mode(),
        )

        return {
            "success": True,
            "code": formatted,
            "error": None,
        }

    except Exception as exc:
        return {
            "success": False,
            "code": code,
            "error": str(exc),
        }


def format_code(code, language):
    """
    Format supported source code.
    """
    language = language.lower().strip()

    if language == "python":
        return format_python_code(code)

    if language in {"json", "javascript", "css", "html"}:
        return {
            "success": True,
            "code": basic_code_format(code, language),
            "error": None,
        }

    return {
        "success": False,
        "code": code,
        "error": (
            f"Unsupported language: {language}"
        ),
    }


def basic_code_format(code, language):
    """
    Basic formatting for non-Python languages.

    This is intentionally lightweight and does not
    attempt to replace a full language parser.
    """
    code = code.strip()

    if not code:
        return ""

    if language == "json":
        import json

        try:
            parsed = json.loads(code)

            return json.dumps(
                parsed,
                indent=4,
                ensure_ascii=False,
            )

        except json.JSONDecodeError:
            return code

    if language in {"html", "css", "javascript"}:
        lines = []
        indentation = 0

        tokens = re.split(
            r"(\{|\})",
            code,
        )

        for token in tokens:
            token = token.strip()

            if not token:
                continue

            if token == "}":
                indentation = max(0, indentation - 1)

            lines.append(
                "    " * indentation + token
            )

            if token == "{":
                indentation += 1

        return "\n".join(lines)

    return code