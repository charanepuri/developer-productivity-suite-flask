import base64
import html
from urllib.parse import quote, unquote


def base64_encode(text):
    """
    Encode text using UTF-8 Base64.
    """
    if text is None:
        text = ""

    encoded = base64.b64encode(
        text.encode("utf-8")
    )

    return encoded.decode("utf-8")


def base64_decode(encoded_text):
    """
    Decode UTF-8 Base64 text.
    """
    if encoded_text is None:
        encoded_text = ""

    try:
        decoded = base64.b64decode(
            encoded_text,
            validate=True,
        )

        return decoded.decode("utf-8")

    except (
        ValueError,
        UnicodeDecodeError,
        base64.binascii.Error,
    ) as exc:

        raise ValueError(
            "Invalid Base64 input."
        ) from exc


def url_encode(text):
    """
    URL encode text.
    """
    if text is None:
        text = ""

    return quote(
        text,
        safe="",
    )


def url_decode(encoded_text):
    """
    URL decode text.
    """
    if encoded_text is None:
        encoded_text = ""

    return unquote(encoded_text)


def html_entity_encode(text):
    """
    Encode HTML special characters.
    """
    if text is None:
        text = ""

    return html.escape(
        text,
        quote=True,
    )


def html_entity_decode(encoded_text):
    """
    Decode HTML entities.
    """
    if encoded_text is None:
        encoded_text = ""

    return html.unescape(encoded_text)