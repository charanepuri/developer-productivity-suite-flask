def count_words(text):
    """Return the number of words in text."""
    if not text:
        return 0

    return len(text.split())


def count_characters(text, include_spaces=True):
    """Return character count."""
    if not text:
        return 0

    if include_spaces:
        return len(text)

    return len("".join(text.split()))


def convert_case(text, case_type):
    """Convert text into the requested case."""
    if not text:
        return ""

    converters = {
        "uppercase": str.upper,
        "lowercase": str.lower,
        "title": str.title,
        "capitalize": str.capitalize,
        "swapcase": str.swapcase,
    }

    converter = converters.get(case_type)

    if not converter:
        return text

    return converter(text)


def remove_duplicate_lines(text):
    """Remove duplicate lines while preserving original order."""
    if not text:
        return ""

    seen = set()
    unique_lines = []

    for line in text.splitlines():
        if line not in seen:
            seen.add(line)
            unique_lines.append(line)

    return "\n".join(unique_lines)


def sort_lines(text, reverse=False, ignore_case=False):
    """Sort text lines."""
    if not text:
        return ""

    lines = text.splitlines()

    if ignore_case:
        return "\n".join(
            sorted(
                lines,
                key=str.lower,
                reverse=reverse,
            )
        )

    return "\n".join(
        sorted(
            lines,
            reverse=reverse,
        )
    )


def reverse_text(text, mode="characters"):
    """Reverse text by characters, words, or lines."""

    if not text:
        return ""

    if mode == "words":
        return " ".join(text.split()[::-1])

    if mode == "lines":
        return "\n".join(text.splitlines()[::-1])

    return text[::-1]