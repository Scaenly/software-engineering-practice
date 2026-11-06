export const MINUTES_PER_DAY = 1440;
export const MAX_BOOKING_MINUTES = 120;

type BookingInterval = {
  start: number;
  end: number;
};

type BookingRequest = {
  start: number;
  end: number;
  now: number;
  blocked: boolean;
  bookings: readonly BookingInterval[];
};

export function canBook({
  start,
  end,
  now,
  blocked,
  bookings,
}: BookingRequest): boolean {
  if (start < 0 || end > MINUTES_PER_DAY || start >= end) {
    return false;
  }

  if (start <= now) return false;
  if (end - start > MAX_BOOKING_MINUTES) return false;
  if (blocked) return false;

  for (const booking of bookings) {
    if (start < booking.end && booking.start < end) {
      return false;
    }
  }

  return true;
}