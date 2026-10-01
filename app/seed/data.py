from app.extensions import db
from app.models import Category, Tool


CATEGORIES = [
    {
        "name": "Text Tools",
        "slug": "text-tools",
        "description": "Useful tools for counting, converting, sorting, and transforming text.",
        "icon": "bi-file-text",
        "tools": [
            {
                "name": "Word Counter",
                "slug": "word-counter",
                "description": "Count words, sentences, paragraphs, and lines in text.",
            },
            {
                "name": "Character Counter",
                "slug": "character-counter",
                "description": "Count characters with and without spaces.",
            },
            {
                "name": "Case Converter",
                "slug": "case-converter",
                "description": "Convert text between uppercase, lowercase, title case, and more.",
            },
            {
                "name": "Remove Duplicate Lines",
                "slug": "remove-duplicate-lines",
                "description": "Remove duplicate lines from a block of text.",
            },
            {
                "name": "Text Sorter",
                "slug": "text-sorter",
                "description": "Sort text lines alphabetically or numerically.",
            },
            {
                "name": "Text Reverser",
                "slug": "text-reverser",
                "description": "Reverse characters or lines in text.",
            },
        ],
    },
    {
        "name": "JSON Tools",
        "slug": "json-tools",
        "description": "Format, validate, convert, sort, and manipulate JSON data.",
        "icon": "bi-braces",
        "tools": [
            {
                "name": "JSON Formatter",
                "slug": "json-formatter",
                "description": "Format and beautify JSON data.",
            },
            {
                "name": "JSON Validator",
                "slug": "json-validator",
                "description": "Validate JSON syntax and identify formatting errors.",
            },
            {
                "name": "JSON Minifier",
                "slug": "json-minifier",
                "description": "Minify JSON by removing unnecessary whitespace.",
            },
            {
                "name": "JSON to CSV",
                "slug": "json-to-csv",
                "description": "Convert JSON data into CSV format.",
            },
            {
                "name": "JSON Sorter",
                "slug": "json-sorter",
                "description": "Sort JSON object keys for easier organization.",
            },
            {
                "name": "JSON Escape/Unescape",
                "slug": "json-escape-unescape",
                "description": "Escape and unescape JSON strings.",
            },
        ],
    },
    {
        "name": "Security Tools",
        "slug": "security-tools",
        "description": "Developer-focused tools for passwords, hashes, UUIDs, and secure tokens.",
        "icon": "bi-shield-lock",
        "tools": [
            {
                "name": "Password Generator",
                "slug": "password-generator",
                "description": "Generate secure random passwords.",
            },
            {
                "name": "Password Strength Checker",
                "slug": "password-strength-checker",
                "description": "Analyze password strength using common security rules.",
            },
            {
                "name": "Hash Generator",
                "slug": "hash-generator",
                "description": "Generate cryptographic hashes from text.",
            },
            {
                "name": "Hash Identifier",
                "slug": "hash-identifier",
                "description": "Identify possible hash algorithms from hash strings.",
            },
            {
                "name": "UUID Generator",
                "slug": "uuid-generator",
                "description": "Generate universally unique identifiers.",
            },
            {
                "name": "Random Token Generator",
                "slug": "random-token-generator",
                "description": "Generate random tokens for development and testing.",
            },
        ],
    },
    {
        "name": "CSS Tools",
        "slug": "css-tools",
        "description": "Generate, format, and optimize commonly used CSS.",
        "icon": "bi-palette",
        "tools": [
            {
                "name": "CSS Minifier",
                "slug": "css-minifier",
                "description": "Minify CSS by removing unnecessary whitespace.",
            },
            {
                "name": "CSS Formatter",
                "slug": "css-formatter",
                "description": "Format compressed or poorly structured CSS.",
            },
            {
                "name": "CSS Box Shadow Generator",
                "slug": "css-box-shadow-generator",
                "description": "Generate CSS box-shadow declarations.",
            },
            {
                "name": "CSS Gradient Generator",
                "slug": "css-gradient-generator",
                "description": "Create CSS linear and radial gradients.",
            },
            {
                "name": "CSS Flexbox Generator",
                "slug": "css-flexbox-generator",
                "description": "Generate CSS Flexbox layouts and properties.",
            },
        ],
    },
    {
        "name": "Color Tools",
        "slug": "color-tools",
        "description": "Work with colors, palettes, gradients, and accessibility contrast.",
        "icon": "bi-droplet",
        "tools": [
            {
                "name": "Color Converter",
                "slug": "color-converter",
                "description": "Convert colors between HEX, RGB, HSL, and related formats.",
            },
            {
                "name": "Color Picker",
                "slug": "color-picker",
                "description": "Select and inspect colors using a visual color picker.",
            },
            {
                "name": "Color Palette Generator",
                "slug": "color-palette-generator",
                "description": "Generate useful color palettes for applications and websites.",
            },
            {
                "name": "Contrast Checker",
                "slug": "contrast-checker",
                "description": "Check foreground and background color contrast.",
            },
            {
                "name": "Gradient Generator",
                "slug": "gradient-generator",
                "description": "Generate attractive CSS color gradients.",
            },
        ],
    },
    {
        "name": "Markdown Tools",
        "slug": "markdown-tools",
        "description": "Create, preview, format, and convert Markdown content.",
        "icon": "bi-markdown",
        "tools": [
            {
                "name": "Markdown Editor",
                "slug": "markdown-editor",
                "description": "Write and edit Markdown content.",
            },
            {
                "name": "Markdown Previewer",
                "slug": "markdown-previewer",
                "description": "Preview rendered Markdown in real time.",
            },
            {
                "name": "Markdown to HTML",
                "slug": "markdown-to-html",
                "description": "Convert Markdown documents into HTML.",
            },
            {
                "name": "Markdown Formatter",
                "slug": "markdown-formatter",
                "description": "Format and organize Markdown content.",
            },
            {
                "name": "Markdown Table Generator",
                "slug": "markdown-table-generator",
                "description": "Generate Markdown tables quickly.",
            },
        ],
    },
    {
        "name": "Developer Tools",
        "slug": "developer-tools",
        "description": "General-purpose utilities for everyday software development.",
        "icon": "bi-code-slash",
        "tools": [
            {
                "name": "Regex Tester",
                "slug": "regex-tester",
                "description": "Test regular expressions against sample text.",
            },
            {
                "name": "Timestamp Converter",
                "slug": "timestamp-converter",
                "description": "Convert timestamps into readable date and time formats.",
            },
            {
                "name": "Lorem Ipsum Generator",
                "slug": "lorem-ipsum-generator",
                "description": "Generate placeholder text for development and design.",
            },
            {
                "name": "QR Code Generator",
                "slug": "qr-code-generator",
                "description": "Generate QR codes from text or URLs.",
            },
            {
                "name": "Diff Checker",
                "slug": "diff-checker",
                "description": "Compare two text blocks and identify differences.",
            },
            {
                "name": "Code Formatter",
                "slug": "code-formatter",
                "description": "Format source code for improved readability.",
            },
        ],
    },
    {
        "name": "Date & Time Tools",
        "slug": "date-time-tools",
        "description": "Calculate, convert, and work with dates and time zones.",
        "icon": "bi-calendar3",
        "tools": [
            {
                "name": "Unix Timestamp Converter",
                "slug": "unix-timestamp-converter",
                "description": "Convert Unix timestamps to readable dates and times.",
            },
            {
                "name": "Date Difference Calculator",
                "slug": "date-difference-calculator",
                "description": "Calculate the difference between two dates.",
            },
            {
                "name": "Time Zone Converter",
                "slug": "time-zone-converter",
                "description": "Convert times between different time zones.",
            },
            {
                "name": "Age Calculator",
                "slug": "age-calculator",
                "description": "Calculate age from a date of birth.",
            },
        ],
    },
    {
        "name": "API Tools",
        "slug": "api-tools",
        "description": "Utilities for working with APIs, requests, responses, and HTTP.",
        "icon": "bi-cloud-arrow-down",
        "tools": [
            {
                "name": "API Request Builder",
                "slug": "api-request-builder",
                "description": "Build and inspect HTTP API requests.",
            },
            {
                "name": "HTTP Status Code Lookup",
                "slug": "http-status-code-lookup",
                "description": "Look up HTTP status codes and their meanings.",
            },
            {
                "name": "cURL Generator",
                "slug": "curl-generator",
                "description": "Generate cURL commands for HTTP requests.",
            },
            {
                "name": "API Response Formatter",
                "slug": "api-response-formatter",
                "description": "Format and inspect API responses.",
            },
        ],
    },
    {
        "name": "Encoding Tools",
        "slug": "encoding-tools",
        "description": "Encode and decode common web and developer data formats.",
        "icon": "bi-lock",
        "tools": [
            {
                "name": "Base64 Encoder/Decoder",
                "slug": "base64-encoder-decoder",
                "description": "Encode and decode Base64 data.",
            },
            {
                "name": "URL Encoder/Decoder",
                "slug": "url-encoder-decoder",
                "description": "Encode and decode URL components.",
            },
            {
                "name": "HTML Entity Encoder/Decoder",
                "slug": "html-entity-encoder-decoder",
                "description": "Encode and decode HTML entities.",
            },
        ],
    },
]


def seed_database():
    """Create or update the DPS category and tool catalog."""

    category_count = 0
    tool_count = 0

    for category_data in CATEGORIES:
        category = Category.query.filter_by(
            slug=category_data["slug"]
        ).first()

        if not category:
            category = Category(
                name=category_data["name"],
                slug=category_data["slug"],
                description=category_data["description"],
                icon=category_data["icon"],
            )
            db.session.add(category)
            db.session.flush()
            category_count += 1
        else:
            category.name = category_data["name"]
            category.description = category_data["description"]
            category.icon = category_data["icon"]

        for tool_data in category_data["tools"]:
            tool = Tool.query.filter_by(
                slug=tool_data["slug"]
            ).first()

            if not tool:
                tool = Tool(
                    name=tool_data["name"],
                    slug=tool_data["slug"],
                    description=tool_data["description"],
                    category_id=category.id,
                    is_active=True,
                )
                db.session.add(tool)
                tool_count += 1
            else:
                tool.name = tool_data["name"]
                tool.description = tool_data["description"]
                tool.category_id = category.id
                tool.is_active = True

    db.session.commit()

    return {
        "categories_created": category_count,
        "tools_created": tool_count,
    }   