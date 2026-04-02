"""ISO-8601 UTC strings with Z suffix (API contract style)."""

from datetime import datetime, timezone

from app.constants import messages as msg_c


def to_iso_z(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return (
        dt.astimezone(timezone.utc)
        .isoformat()
        .replace(msg_c.ISO_DATETIME_UTC_OFFSET_LEGACY, msg_c.ISO_DATETIME_Z_SUFFIX)
    )
