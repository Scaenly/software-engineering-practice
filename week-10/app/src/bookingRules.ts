// Shared pure predicates: no clock, browser, state, or data mutation.
export const MINUTES_PER_DAY = 1440;
export const MAX_BOOKING_MINUTES = 120;

export type BookingInterval = {
  start: number;
  end: number;
};

export type BookingRequest = {
  start: number;
  end: number;
  now: number;
  blocked: boolean;
  bookings: readonly BookingInterval[];
};

export function isValidInterval(start: number, end: number): boolean {
  return 0 <= start && start < end && end <= MINUTES_PER_DAY;
}

export function isFutureStart(start: number, now: number): boolean {
  return start > now;
}

export function exceedsDuration(start: number, end: number): boolean {
  return end - start > MAX_BOOKING_MINUTES;
}

export function overlaps(
  start: number,
  end: number,
  bookingStart: number,
  bookingEnd: number,
): boolean {
  return start < bookingEnd && end > bookingStart;
}
