import hashlib
import re
import secrets
import string
import uuid


SUPPORTED_HASH_ALGORITHMS = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha224": hashlib.sha224,
    "sha256": hashlib.sha256,
    "sha384": hashlib.sha384,
    "sha512": hashlib.sha512,
}


def generate_password(
    length=16,
    use_uppercase=True,
    use_lowercase=True,
    use_digits=True,
    use_symbols=True,
):
    """Generate a cryptographically secure random password."""

    try:
        length = int(length)
    except (TypeError, ValueError) as exc:
        raise ValueError("Password length must be a number.") from exc

    if length < 4:
        raise ValueError(
            "Password length must be at least 4 characters."
        )

    if length > 256:
        raise ValueError(
            "Password length cannot exceed 256 characters."
        )

    character_sets = []

    if use_uppercase:
        character_sets.append(string.ascii_uppercase)

    if use_lowercase:
        character_sets.append(string.ascii_lowercase)

    if use_digits:
        character_sets.append(string.digits)

    if use_symbols:
        character_sets.append(
            "!@#$%^&*()-_=+[]{}:,.?"
        )

    if not character_sets:
        raise ValueError(
            "Select at least one character type."
        )

    # Guarantee at least one character from every
    # selected character set.
    password_characters = [
        secrets.choice(characters)
        for characters in character_sets
    ]

    all_characters = "".join(character_sets)

    remaining = length - len(password_characters)

    password_characters.extend(
        secrets.choice(all_characters)
        for _ in range(remaining)
    )

    # Securely shuffle the generated characters.
    shuffled = []

    while password_characters:
        index = secrets.randbelow(
            len(password_characters)
        )
        shuffled.append(
            password_characters.pop(index)
        )

    return "".join(shuffled)


def check_password_strength(password):
    """Analyze password characteristics."""

    if password is None:
        password = ""

    checks = {
        "length": len(password) >= 12,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "digit": bool(re.search(r"\d", password)),
        "symbol": bool(
            re.search(r"[^A-Za-z0-9]", password)
        ),
    }

    score = sum(checks.values())

    if not password:
        level = "Very Weak"
    elif score <= 1:
        level = "Very Weak"
    elif score == 2:
        level = "Weak"
    elif score == 3:
        level = "Moderate"
    elif score == 4:
        level = "Strong"
    else:
        level = "Very Strong"

    suggestions = []

    if len(password) < 12:
        suggestions.append(
            "Use at least 12 characters."
        )

    if not checks["uppercase"]:
        suggestions.append(
            "Add uppercase letters."
        )

    if not checks["lowercase"]:
        suggestions.append(
            "Add lowercase letters."
        )

    if not checks["digit"]:
        suggestions.append(
            "Add numbers."
        )

    if not checks["symbol"]:
        suggestions.append(
            "Add special characters."
        )

    return {
        "score": score,
        "max_score": 5,
        "level": level,
        "checks": checks,
        "suggestions": suggestions,
    }


def generate_hash(text, algorithm="sha256"):
    """Generate a hexadecimal hash digest."""

    if text is None:
        text = ""

    algorithm = algorithm.lower().strip()

    hash_function = SUPPORTED_HASH_ALGORITHMS.get(
        algorithm
    )

    if hash_function is None:
        raise ValueError(
            "Unsupported hash algorithm."
        )

    digest = hash_function(
        text.encode("utf-8")
    ).hexdigest()

    return digest


def identify_hash(hash_value):
    """Identify likely hash algorithms by length and format."""

    if not hash_value:
        return {
            "valid_format": False,
            "length": 0,
            "possible_algorithms": [],
        }

    value = hash_value.strip()

    if not re.fullmatch(
        r"[0-9a-fA-F]+",
        value,
    ):
        return {
            "valid_format": False,
            "length": len(value),
            "possible_algorithms": [],
        }

    length_map = {
        32: ["MD5"],
        40: ["SHA-1"],
        56: ["SHA-224"],
        64: ["SHA-256"],
        96: ["SHA-384"],
        128: ["SHA-512"],
    }

    return {
        "valid_format": True,
        "length": len(value),
        "possible_algorithms": length_map.get(
            len(value),
            [],
        ),
    }


def generate_uuid(version="4", count=1):
    """Generate UUID values."""

    try:
        count = int(count)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "UUID count must be a number."
        ) from exc

    if count < 1:
        raise ValueError(
            "UUID count must be at least 1."
        )

    if count > 100:
        raise ValueError(
            "UUID count cannot exceed 100."
        )

    version = str(version)

    if version == "4":
        values = [
            str(uuid.uuid4())
            for _ in range(count)
        ]

    elif version == "1":
        values = [
            str(uuid.uuid1())
            for _ in range(count)
        ]

    else:
        raise ValueError(
            "Supported UUID versions are 1 and 4."
        )

    return values


def generate_random_token(length=32):
    """Generate a cryptographically secure random token."""

    try:
        length = int(length)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "Token length must be a number."
        ) from exc

    if length < 8:
        raise ValueError(
            "Token length must be at least 8 characters."
        )

    if length > 256:
        raise ValueError(
            "Token length cannot exceed 256 characters."
        )

    alphabet = (
        string.ascii_letters
        + string.digits
        + "-_"
    )

    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )