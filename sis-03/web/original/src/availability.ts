import type { AvailabilityResult, Booking, Room } from './types';

const MINUTES_PER_DAY = 1440;
const MAX_BOOKING_MINUTES = 120;

export const MINUTES_PER_DAY_VALUE = MINUTES_PER_DAY;
export const MAX_BOOKING_MINUTES_VALUE = MAX_BOOKING_MINUTES;

/** Convert "HH:MM" (24h) to minutes since midnight. Returns null when malformed. */
export function timeToMinutes(value: string): number | null {
  const match = /^([01]?\d|2[0-3]):([0-5]\d)$/.exec(value.trim());
  if (!match) return null;
  const hours = parseInt(match[1], 10);
  const minutes = parseInt(match[2], 10);
  return hours * 60 + minutes;
}

/** Format minutes since midnight as "HH:MM". */
export function minutesToTime(min: number): string {
  const clamped = ((Math.round(min) % MINUTES_PER_DAY) + MINUTES_PER_DAY) % MINUTES_PER_DAY;
  const h = Math.floor(clamped / 60);
  const m = clamped % 60;
  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}`;
}

/** True when [aStart,aEnd) and [bStart,bEnd) overlap. Touching endpoints are NOT an overlap. */
function overlaps(aStart: number, aEnd: number, bStart: number, bEnd: number): boolean {
  return aStart < bEnd && bStart < aEnd;
}

/**
 * Evaluate a candidate booking interval against all acceptance criteria.
 * Returns a clear Available / Unavailable decision without mutating any data (AC5).
 */
export function checkAvailability(
  room: Room | null,
  start: number,
  end: number,
  currentTimeMinutes: number,
  bookings: Booking[],
): AvailabilityResult {
  const reasons: string[] = [];

  // AC1: valid interval bounds + start after current time
  if (start < 0 || end > MINUTES_PER_DAY || start >= end) {
    reasons.push('Interval must satisfy 0 ≤ start < end ≤ 1440 minutes.');
  }
  if (start <= currentTimeMinutes) {
    reasons.push(`Start time must be after the current time (${minutesToTime(currentTimeMinutes)}).`);
  }

  // AC2: no booking longer than 120 minutes
  if (end - start > MAX_BOOKING_MINUTES) {
    reasons.push(`Booking length is ${end - start} min, which exceeds the 120-minute maximum.`);
  }

  // AC3: reject when the selected room is blocked
  if (!room) {
    reasons.push('Please select a room.');
  } else if (room.blocked) {
    reasons.push(`${room.name} is currently blocked and cannot be booked.`);
  }

  // AC4: reject any interval overlapping an existing booking (touching endpoints allowed)
  if (room && start >= 0 && start < end && end <= MINUTES_PER_DAY) {
    const conflicts = bookings.filter(
      (b) => b.roomId === room.id && overlaps(start, end, b.start, b.end),
    );
    for (const c of conflicts) {
      reasons.push(
        `Overlaps "${c.title}" (${minutesToTime(c.start)}–${minutesToTime(c.end)}).`,
      );
    }
  }

  return { available: reasons.length === 0, reasons };
}
