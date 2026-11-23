import {
  exceedsDuration,
  isFutureStart,
  isValidInterval,
  overlaps,
  type BookingRequest,
} from './bookingRules';

export { MINUTES_PER_DAY, MAX_BOOKING_MINUTES } from './bookingRules';

export function canBook({ start, end, now, blocked, bookings }: BookingRequest): boolean {
  if (!isValidInterval(start, end)) return false;
  if (!isFutureStart(start, now)) return false;
  if (exceedsDuration(start, end)) return false;
  if (blocked) return false;
  for (const b of bookings) {
    if (overlaps(start, end, b.start, b.end)) return false;
  }
  return true;
}
