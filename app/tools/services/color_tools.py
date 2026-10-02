import colorsys
import random
import re


HEX_PATTERN = re.compile(r"^#?[0-9a-fA-F]{6}$")


def normalize_hex(color):
    """Normalize a 6-digit hexadecimal color."""
    color = color.strip()

    if not HEX_PATTERN.match(color):
        raise ValueError("Enter a valid 6-digit HEX color.")

    if not color.startswith("#"):
        color = f"#{color}"

    return color.upper()


def hex_to_rgb(hex_color):
    """Convert HEX color to RGB."""
    hex_color = normalize_hex(hex_color)

    return tuple(
        int(hex_color[i:i + 2], 16)
        for i in (1, 3, 5)
    )


def rgb_to_hex(red, green, blue):
    """Convert RGB values to HEX."""
    values = [red, green, blue]

    if any(value < 0 or value > 255 for value in values):
        raise ValueError("RGB values must be between 0 and 255.")

    return "#{:02X}{:02X}{:02X}".format(
        int(red),
        int(green),
        int(blue),
    )


def rgb_to_hsl(red, green, blue):
    """Convert RGB to HSL."""
    red /= 255
    green /= 255
    blue /= 255

    hue, lightness, saturation = colorsys.rgb_to_hls(
        red,
        green,
        blue,
    )

    return {
        "h": round(hue * 360, 2),
        "s": round(saturation * 100, 2),
        "l": round(lightness * 100, 2),
    }


def hsl_to_rgb(hue, saturation, lightness):
    """Convert HSL to RGB."""
    hue /= 360
    saturation /= 100
    lightness /= 100

    red, green, blue = colorsys.hls_to_rgb(
        hue,
        lightness,
        saturation,
    )

    return (
        round(red * 255),
        round(green * 255),
        round(blue * 255),
    )


def convert_color(hex_color):
    """Return HEX, RGB and HSL representations."""
    hex_color = normalize_hex(hex_color)

    red, green, blue = hex_to_rgb(hex_color)
    hsl = rgb_to_hsl(red, green, blue)

    return {
        "hex": hex_color,
        "rgb": f"rgb({red}, {green}, {blue})",
        "rgb_values": {
            "r": red,
            "g": green,
            "b": blue,
        },
        "hsl": (
            f"hsl({hsl['h']}°, "
            f"{hsl['s']}%, "
            f"{hsl['l']}%)"
        ),
        "hsl_values": hsl,
    }


def generate_palette(base_color, count=5):
    """Generate a palette around a base color."""
    base_color = normalize_hex(base_color)

    red, green, blue = hex_to_rgb(base_color)

    base_hsl = rgb_to_hsl(red, green, blue)

    palette = []

    for index in range(count):
        lightness = 20 + (
            (60 / max(count - 1, 1)) * index
        )

        r, g, b = hsl_to_rgb(
            base_hsl["h"],
            base_hsl["s"],
            lightness,
        )

        palette.append(
            rgb_to_hex(r, g, b)
        )

    return palette


def generate_random_palette(count=5):
    """Generate a random color palette."""
    count = max(2, min(int(count), 10))

    return [
        "#{:06X}".format(
            random.randint(0, 0xFFFFFF)
        )
        for _ in range(count)
    ]


def relative_luminance(red, green, blue):
    """Calculate relative luminance."""
    values = [red, green, blue]
    converted = []

    for value in values:
        value /= 255

        if value <= 0.03928:
            converted.append(value / 12.92)
        else:
            converted.append(
                ((value + 0.055) / 1.055) ** 2.4
            )

    r, g, b = converted

    return (
        0.2126 * r
        + 0.7152 * g
        + 0.0722 * b
    )


def contrast_ratio(color1, color2):
    """Calculate WCAG-style contrast ratio."""
    color1 = normalize_hex(color1)
    color2 = normalize_hex(color2)

    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)

    luminance1 = relative_luminance(*rgb1)
    luminance2 = relative_luminance(*rgb2)

    lighter = max(luminance1, luminance2)
    darker = min(luminance1, luminance2)

    return round(
        (lighter + 0.05) / (darker + 0.05),
        2,
    )


def contrast_level(ratio):
    """Return accessibility-oriented contrast information."""
    return {
        "aa_normal": ratio >= 4.5,
        "aa_large": ratio >= 3,
        "aaa_normal": ratio >= 7,
        "aaa_large": ratio >= 4.5,
    }


def generate_gradient(
    color1,
    color2,
    gradient_type="linear",
    direction="to right",
):
    """Generate CSS gradient code."""
    color1 = normalize_hex(color1)
    color2 = normalize_hex(color2)

    if gradient_type == "radial":
        css = (
            f"radial-gradient(circle, "
            f"{color1}, {color2})"
        )
    else:
        css = (
            f"linear-gradient("
            f"{direction}, "
            f"{color1}, {color2})"
        )

    return {
        "css": css,
        "property": f"background: {css};",
    }