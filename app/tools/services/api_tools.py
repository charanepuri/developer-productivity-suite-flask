import json
from urllib.parse import urlparse

import requests


HTTP_STATUS_CODES = {
    100: {
        "name": "Continue",
        "category": "Informational",
        "description": "The request headers have been received and the client may continue.",
    },
    101: {
        "name": "Switching Protocols",
        "category": "Informational",
        "description": "The server is switching protocols as requested by the client.",
    },
    200: {
        "name": "OK",
        "category": "Success",
        "description": "The request was successfully processed.",
    },
    201: {
        "name": "Created",
        "category": "Success",
        "description": "The request successfully created a new resource.",
    },
    202: {
        "name": "Accepted",
        "category": "Success",
        "description": "The request has been accepted for processing.",
    },
    204: {
        "name": "No Content",
        "category": "Success",
        "description": "The request succeeded but there is no response body.",
    },
    301: {
        "name": "Moved Permanently",
        "category": "Redirection",
        "description": "The requested resource has permanently moved to another URL.",
    },
    302: {
        "name": "Found",
        "category": "Redirection",
        "description": "The requested resource is temporarily available at another URL.",
    },
    304: {
        "name": "Not Modified",
        "category": "Redirection",
        "description": "The resource has not changed since the previous request.",
    },
    307: {
        "name": "Temporary Redirect",
        "category": "Redirection",
        "description": "The resource is temporarily available at another URL.",
    },
    308: {
        "name": "Permanent Redirect",
        "category": "Redirection",
        "description": "The resource has permanently moved to another URL.",
    },
    400: {
        "name": "Bad Request",
        "category": "Client Error",
        "description": "The server could not understand the request.",
    },
    401: {
        "name": "Unauthorized",
        "category": "Client Error",
        "description": "Authentication is required or the supplied credentials are invalid.",
    },
    403: {
        "name": "Forbidden",
        "category": "Client Error",
        "description": "The server understood the request but refuses to authorize it.",
    },
    404: {
        "name": "Not Found",
        "category": "Client Error",
        "description": "The requested resource could not be found.",
    },
    405: {
        "name": "Method Not Allowed",
        "category": "Client Error",
        "description": "The HTTP method is not supported for the requested resource.",
    },
    408: {
        "name": "Request Timeout",
        "category": "Client Error",
        "description": "The server timed out waiting for the request.",
    },
    409: {
        "name": "Conflict",
        "category": "Client Error",
        "description": "The request conflicts with the current state of the resource.",
    },
    415: {
        "name": "Unsupported Media Type",
        "category": "Client Error",
        "description": "The server does not support the request's media format.",
    },
    422: {
        "name": "Unprocessable Content",
        "category": "Client Error",
        "description": "The request format is understood but contains invalid data.",
    },
    429: {
        "name": "Too Many Requests",
        "category": "Client Error",
        "description": "The client has sent too many requests in a given period.",
    },
    500: {
        "name": "Internal Server Error",
        "category": "Server Error",
        "description": "The server encountered an unexpected condition.",
    },
    501: {
        "name": "Not Implemented",
        "category": "Server Error",
        "description": "The server does not support the functionality required by the request.",
    },
    502: {
        "name": "Bad Gateway",
        "category": "Server Error",
        "description": "The server received an invalid response from an upstream server.",
    },
    503: {
        "name": "Service Unavailable",
        "category": "Server Error",
        "description": "The server is temporarily unable to handle the request.",
    },
    504: {
        "name": "Gateway Timeout",
        "category": "Server Error",
        "description": "An upstream server failed to respond in time.",
    },
}


def validate_url(url):
    """
    Validate that a URL has a supported HTTP/HTTPS scheme.
    """
    parsed = urlparse(url.strip())

    if parsed.scheme not in {"http", "https"}:
        raise ValueError(
            "URL must start with http:// or https://."
        )

    if not parsed.netloc:
        raise ValueError(
            "Please enter a valid URL."
        )

    return url.strip()


def parse_headers(headers_text):
    """
    Parse newline-separated HTTP headers.

    Example:
        Authorization: Bearer token
        Accept: application/json
    """
    headers = {}

    for line in headers_text.splitlines():
        line = line.strip()

        if not line:
            continue

        if ":" not in line:
            raise ValueError(
                f"Invalid header: {line}"
            )

        key, value = line.split(":", 1)

        key = key.strip()
        value = value.strip()

        if key:
            headers[key] = value

    return headers


def parse_request_body(body_text):
    """
    Try to parse a request body as JSON.

    If it is not valid JSON, return the original text.
    """
    if not body_text.strip():
        return None

    try:
        return json.loads(body_text)
    except json.JSONDecodeError:
        return body_text


def make_api_request(
    url,
    method="GET",
    headers=None,
    body=None,
    timeout=10,
):
    """
    Execute an HTTP request and return useful response data.
    """
    url = validate_url(url)

    method = method.upper()

    response = requests.request(
        method=method,
        url=url,
        headers=headers or {},
        json=body if isinstance(body, (dict, list)) else None,
        data=body if isinstance(body, str) else None,
        timeout=timeout,
    )

    response_body = response.text

    try:
        parsed_json = response.json()
    except ValueError:
        parsed_json = None

    return {
        "status_code": response.status_code,
        "reason": response.reason,
        "headers": dict(response.headers),
        "body": response_body,
        "json": parsed_json,
        "elapsed": round(
            response.elapsed.total_seconds(),
            3,
        ),
    }


def get_status_code_info(status_code):
    """
    Return information about an HTTP status code.
    """
    try:
        status_code = int(status_code)
    except (TypeError, ValueError):
        return None

    return HTTP_STATUS_CODES.get(status_code)


def generate_curl_command(
    url,
    method="GET",
    headers=None,
    body=None,
):
    """
    Generate a cURL command.
    """
    url = validate_url(url)

    method = method.upper()

    parts = [
        "curl",
        f"-X {method}",
        f"'{url}'",
    ]

    for key, value in (headers or {}).items():
        parts.append(
            f"-H '{key}: {value}'"
        )

    if body:
        if isinstance(body, (dict, list)):
            body = json.dumps(body)

        escaped_body = body.replace(
            "'",
            "'\\''",
        )

        parts.append(
            f"-d '{escaped_body}'"
        )

    return " ".join(parts)


def format_api_response(response_text):
    """
    Format a JSON API response when possible.
    """
    if not response_text.strip():
        return {
            "success": True,
            "format": "empty",
            "output": "",
        }

    try:
        parsed = json.loads(response_text)

        return {
            "success": True,
            "format": "json",
            "output": json.dumps(
                parsed,
                indent=4,
                ensure_ascii=False,
            ),
        }

    except json.JSONDecodeError:
        return {
            "success": False,
            "format": "text",
            "output": response_text,
            "error": "Input is not valid JSON.",
        }