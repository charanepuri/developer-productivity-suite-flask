import csv
import io
import json


def format_json(text, indent=4):
    """Format JSON with readable indentation."""

    if not text or not text.strip():
        raise ValueError("JSON input cannot be empty.")

    try:
        data = json.loads(text)

        return json.dumps(
            data,
            indent=indent,
            ensure_ascii=False,
        )

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON: {exc.msg} "
            f"(line {exc.lineno}, column {exc.colno})"
        ) from exc


def validate_json(text):
    """Validate JSON and return validation details."""

    if not text or not text.strip():
        return {
            "valid": False,
            "message": "JSON input cannot be empty.",
        }

    try:
        json.loads(text)

        return {
            "valid": True,
            "message": "Valid JSON.",
        }

    except json.JSONDecodeError as exc:
        return {
            "valid": False,
            "message": (
                f"Invalid JSON: {exc.msg} "
                f"(line {exc.lineno}, column {exc.colno})."
            ),
        }


def minify_json(text):
    """Minify JSON by removing unnecessary whitespace."""

    if not text or not text.strip():
        raise ValueError("JSON input cannot be empty.")

    try:
        data = json.loads(text)

        return json.dumps(
            data,
            ensure_ascii=False,
            separators=(",", ":"),
        )

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON: {exc.msg} "
            f"(line {exc.lineno}, column {exc.colno})"
        ) from exc


def json_to_csv(text):
    """Convert JSON records into CSV."""

    if not text or not text.strip():
        raise ValueError("JSON input cannot be empty.")

    try:
        data = json.loads(text)

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON: {exc.msg}"
        ) from exc

    if isinstance(data, dict):
        data = [data]

    if not isinstance(data, list):
        raise ValueError(
            "JSON must contain an object or an array of objects."
        )

    if not data:
        return ""

    if not all(isinstance(item, dict) for item in data):
        raise ValueError(
            "JSON array must contain only objects."
        )

    fieldnames = []

    for item in data:
        for key in item.keys():
            if key not in fieldnames:
                fieldnames.append(key)

    output = io.StringIO()

    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames,
        extrasaction="ignore",
    )

    writer.writeheader()

    for item in data:
        writer.writerow(item)

    return output.getvalue()


def sort_json(text):
    """Sort JSON object keys recursively."""

    if not text or not text.strip():
        raise ValueError("JSON input cannot be empty.")

    try:
        data = json.loads(text)

        return json.dumps(
            data,
            indent=4,
            ensure_ascii=False,
            sort_keys=True,
        )

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON: {exc.msg}"
        ) from exc


def escape_json(text):
    """Escape text for JSON string representation."""

    if text is None:
        return ""

    return json.dumps(
        text,
        ensure_ascii=False,
    )[1:-1]


def unescape_json(text):
    """Unescape JSON escaped text."""

    if text is None:
        return ""

    try:
        return json.loads(f'"{text}"')

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid escaped JSON text: {exc.msg}"
        ) from exc