from datetime import (
    date,
    datetime,
    timezone,
)
from zoneinfo import ZoneInfo


def timestamp_to_datetime(timestamp):
    """
    Convert a Unix timestamp to UTC datetime.
    """
    timestamp = float(timestamp)

    return datetime.fromtimestamp(
        timestamp,
        tz=timezone.utc,
    )


def datetime_to_timestamp(date_string):
    """
    Convert an ISO datetime string to Unix timestamp.
    """
    normalized = date_string.strip()

    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"

    parsed = datetime.fromisoformat(normalized)

    if parsed.tzinfo is None:
        parsed = parsed.replace(
            tzinfo=timezone.utc
        )

    return int(parsed.timestamp())


def calculate_date_difference(
    start_date,
    end_date,
):
    """
    Calculate the difference between two dates.
    """
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)

    difference = end - start

    total_days = abs(difference.days)

    years = total_days // 365
    remaining_days = total_days % 365

    months = total_days // 30
    remaining_month_days = total_days % 30

    return {
        "days": total_days,
        "weeks": round(total_days / 7, 2),
        "months_approx": months,
        "remaining_days_after_months": remaining_month_days,
        "years_approx": years,
        "remaining_days_after_years": remaining_days,
        "start_before_end": start <= end,
    }


def get_timezone_names():
    """
    Return commonly used timezone names.
    """
    return [
        "UTC",
        "Asia/Kolkata",
        "Asia/Dubai",
        "Asia/Singapore",
        "Asia/Tokyo",
        "Europe/London",
        "Europe/Paris",
        "Europe/Berlin",
        "America/New_York",
        "America/Chicago",
        "America/Denver",
        "America/Los_Angeles",
        "Australia/Sydney",
    ]


def convert_timezone(
    date_string,
    source_timezone,
    target_timezone,
):
    """
    Convert a datetime from one timezone to another.
    """
    normalized = date_string.strip()

    parsed = datetime.fromisoformat(normalized)

    source_zone = ZoneInfo(source_timezone)
    target_zone = ZoneInfo(target_timezone)

    if parsed.tzinfo is None:
        parsed = parsed.replace(
            tzinfo=source_zone
        )
    else:
        parsed = parsed.astimezone(
            source_zone
        )

    converted = parsed.astimezone(
        target_zone
    )

    return {
        "source": parsed,
        "target": converted,
        "source_formatted": parsed.strftime(
            "%Y-%m-%d %H:%M:%S %Z"
        ),
        "target_formatted": converted.strftime(
            "%Y-%m-%d %H:%M:%S %Z"
        ),
    }


def calculate_age(
    birth_date,
    reference_date=None,
):
    """
    Calculate age from date of birth.
    """
    birth = date.fromisoformat(birth_date)

    if reference_date:
        reference = date.fromisoformat(
            reference_date
        )
    else:
        reference = date.today()

    if birth > reference:
        raise ValueError(
            "Birth date cannot be in the future."
        )

    years = (
        reference.year
        - birth.year
        - (
            (
                reference.month,
                reference.day,
            )
            < (
                birth.month,
                birth.day,
            )
        )
    )

    last_birthday_year = (
        reference.year
        if (
            reference.month,
            reference.day,
        ) >= (
            birth.month,
            birth.day,
        )
        else reference.year - 1
    )

    last_birthday = date(
        last_birthday_year,
        birth.month,
        birth.day,
    )

    remaining_days = (
        reference - last_birthday
    ).days

    total_days = (
        reference - birth
    ).days

    return {
        "years": years,
        "remaining_days": remaining_days,
        "total_days": total_days,
        "birth_date": birth,
        "reference_date": reference,
    }