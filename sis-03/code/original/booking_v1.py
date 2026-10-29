from datetime import datetime, timedelta
from typing import List, Tuple, Optional, Any, Dict, Protocol

# Protocol or Dataclass-like structure assumed for type hinting:
# Existing bookings can be tuples/lists of (start, end) or objects with .start and .end attributes.

def can_book(
    booking_start: datetime,
    booking_end: datetime,
    slot_start: datetime,
    slot_end: datetime,
    existing_bookings: List[Any],
    min_duration: Optional[timedelta] = None,
    max_duration: Optional[timedelta] = None,
    step_minutes: Optional[int] = None,
    buffer_minutes: int = 0
) -> bool:
    """
    Evaluates whether a requested booking can be placed.
    Uses half-open intervals [start, end).
    """
    # Helper to pull (start, end) from objects or tuples
    def get_bounds(item: Any) -> Tuple[datetime, datetime]:
        if isinstance(item, (tuple, list)):
            return item[0], item[1]
        return getattr(item, "start"), getattr(item, "end")

    # Condition 1 (AC1): Valid Chronological Order & Duration Constraints
    if booking_start >= booking_end:
        return False
    
    duration = booking_end - booking_start
    if min_duration and duration < min_duration:
        return False
    if max_duration and duration > max_duration:
        return False

    # Condition 2 (AC2): Slot Boundary Enforcement
    if booking_start < slot_start or booking_end > slot_end:
        return False

    # Condition 3 (AC3): Alignment / Step Granularity Constraints
    if step_minutes and step_minutes > 0:
        start_delta = (booking_start - slot_start).total_seconds() / 60
        end_delta = (booking_end - booking_start).total_seconds() / 60
        if start_delta % step_minutes != 0 or end_delta % step_minutes != 0:
            return False

    # Condition 4 (AC4): Buffer Calculation Setup
    buffer = timedelta(minutes=buffer_minutes)
    buffered_start = booking_start - buffer
    buffered_end = booking_end + buffer

    # Condition 5 (AC5): Overlap Check against Existing Bookings
    for existing in existing_bookings:
        ex_start, ex_end = get_bounds(existing)
        
        # Overlap rule for half-open intervals [start, end):
        # max(start1, start2) < min(end1, end2)
        if max(buffered_start, ex_start) < min(buffered_end, ex_end):
            return False

    return True