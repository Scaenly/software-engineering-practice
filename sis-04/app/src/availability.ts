import { MINUTES_PER_DAY } from './booking';

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
  if (min === MINUTES_PER_DAY) return '24:00';
  const clamped =
    ((Math.round(min) % MINUTES_PER_DAY) + MINUTES_PER_DAY) %
    MINUTES_PER_DAY;

  const h = Math.floor(clamped / 60);
  const m = clamped % 60;

  return `${h.toString().padStart(2, '0')}:${m
    .toString()
    .padStart(2, '0')}`;
}
