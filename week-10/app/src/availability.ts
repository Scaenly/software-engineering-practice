import type { Booking, Room } from './types';
import {
  MINUTES_PER_DAY,
  MAX_BOOKING_MINUTES,
} from './booking';

export const MINUTES_PER_DAY_VALUE = MINUTES_PER_DAY;
export const MAX_BOOKING_MINUTES_VALUE = MAX_BOOKING_MINUTES;

/** Convert HH:MM to minutes since midnight. */
export function timeToMinutes(value: string): number | null {
  const match = /^([01]?\d|2[0-3]):([0-5]\d)$/.exec(value.trim());

  if (!match) return null;

  const hours = parseInt(match[1], 10);
  const minutes = parseInt(match[2], 10);

  return hours * 60 + minutes;
}

/** Format minutes since midnight as HH:MM. */
export function minutesToTime(min: number): string {
  const clamped =
    ((Math.round(min) % MINUTES_PER_DAY) + MINUTES_PER_DAY) %
    MINUTES_PER_DAY;

  const h = Math.floor(clamped / 60);
  const m = clamped % 60;

  return `${h.toString().padStart(2, '0')}:${m
    .toString()
    .padStart(2, '0')}`;
}

/** Touching endpoints are not an overlap. */
function overlaps(
  aStart: number,
  aEnd: number,
  bStart: number,
  bEnd: number,
): boolean {
  return aStart < bEnd && bStart < aEnd;
}

/**
 * Build validation messages for the page.
 * The availability decision itself is made by canBook.
 */
export function getAvailabilityReasons(
  room: Room | null,
  start: number,
  end: number,
  currentTimeMinutes: number,
  bookings: Booking[],
): string[] {
  const reasons: string[] = [];

  if (start < 0 || end > MINUTES_PER_DAY || start >= end) {
    reasons.push('Interval must satisfy 0 ≤ start < end ≤ 1440 minutes.');
  }

  if (start <= currentTimeMinutes) {
    reasons.push(
      `Start time must be after the current time (${minutesToTime(
        currentTimeMinutes,
      )}).`,
    );
  }

  if (end - start > MAX_BOOKING_MINUTES) {
    reasons.push(
      `Booking length is ${
        end - start
      } min, which exceeds the 120-minute maximum.`,
    );
  }

  if (!room) {
    reasons.push('Please select a room.');
  } else if (room.blocked) {
    reasons.push(`${room.name} is currently blocked and cannot be booked.`);
  }

  if (room && start >= 0 && start < end && end <= MINUTES_PER_DAY) {
    const conflicts = bookings.filter(
      (booking) =>
        booking.roomId === room.id &&
        overlaps(start, end, booking.start, booking.end),
    );

    for (const conflict of conflicts) {
      reasons.push(
        `Overlaps "${conflict.title}" (${minutesToTime(
          conflict.start,
        )}–${minutesToTime(conflict.end)}).`,
      );
    }
  }

  return reasons;
}