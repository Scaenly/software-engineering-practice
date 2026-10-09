from typing import List, Tuple


def can_book(
    start: int,
    end: int,
    now: int = 540,
    blocked: bool = False,
    existing: List[Tuple[int, int]] = None
) -> bool:
    """
    Evaluates whether a requested booking can be placed based on minute offsets.
    Uses half-open intervals [start, end).
    """
    if existing is None:
        existing = []

    # AC3: A blocked room accepts nothing
    if blocked:
        return False

    # AC1: Time order, day bounds (0..1440), and start must be in the future (>= now)
    if not (0 <= start < end <= 1440):
        return False
    if start < now:
        return False

    # AC2: Maximum duration is 120 minutes
    if (end - start) > 120:
        return False

    # AC4: Check for overlaps with existing bookings [ex_start, ex_end)
    for ex_start, ex_end in existing:
        if max(start, ex_start) < min(end, ex_end):
            return False

    # AC5: Return a real boolean
    return True