def can_book(start, end, now, blocked, existing):
    """Return True only for a valid, available study-room time interval."""
    if type(start) is not int or type(end) is not int:
        return False
    if not (0 <= start < end <= 1440):
        return False
    if start <= now:
        return False
    if end - start > 120:
        return False
    if blocked:
        return False
    for booked_start, booked_end in existing:
        if start < booked_end and booked_start < end:
            return False
    return True
