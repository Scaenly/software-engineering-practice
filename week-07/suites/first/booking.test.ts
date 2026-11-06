import { describe, expect, test } from 'vitest';
import { canBook } from './booking';

type BookingRequest = Parameters<typeof canBook>[0];

// New request, array and booking objects for every test. Time is always supplied.
function freshRequest(
  start: number,
  end: number,
  overrides: Partial<BookingRequest> = {},
): BookingRequest {
  return {
    start,
    end,
    now: 540,
    blocked: false,
    bookings: [{ start: 600, end: 660 }],
    ...overrides,
  };
}

// Expected decisions come from the reviewed case table and AC1–AC5.
// AC6 and the visible AC5 labels need separate page checks.
// Invalid existing bookings have no specified expected decision and are omitted.
describe('canBook — reviewed booking cases', () => {
  test('T01 AC4: allows touching after an existing booking', () => {
    const request = freshRequest(660, 720);
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(true);
    expect(request.bookings).toEqual(before);
  });

  test('T02 AC1: rejects a request starting exactly now', () => {
    const request = freshRequest(540, 570);
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(false);
    expect(request.bookings).toEqual(before);
  });

  test('T03 AC1: rejects zero duration', () => {
    const request = freshRequest(720, 720);
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(false);
    expect(request.bookings).toEqual(before);
  });

  test('T04 AC1: rejects an end before the start', () => {
    const request = freshRequest(750, 720);
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(false);
    expect(request.bookings).toEqual(before);
  });

  test('T05 AC1: rejects an end past minute 1440', () => {
    const request = freshRequest(1380, 1441);
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(false);
    expect(request.bookings).toEqual(before);
  });

  test('T06 AC2: allows exactly 120 minutes', () => {
    const request = freshRequest(720, 840);
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(true);
    expect(request.bookings).toEqual(before);
  });

  test('T07 AC2: rejects 121 minutes', () => {
    const request = freshRequest(720, 841);
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(false);
    expect(request.bookings).toEqual(before);
  });

  test('T08 AC4: allows touching before an existing booking', () => {
    const request = freshRequest(570, 600);
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(true);
    expect(request.bookings).toEqual(before);
  });

  test('T09 AC4: rejects a partial overlap', () => {
    const request = freshRequest(630, 690);
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(false);
    expect(request.bookings).toEqual(before);
  });

  test('T10 AC4: rejects a request containing an existing booking', () => {
    const request = freshRequest(570, 690);
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(false);
    expect(request.bookings).toEqual(before);
  });

  test('T11 AC4: rejects a request inside an existing booking', () => {
    const request = freshRequest(615, 645);
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(false);
    expect(request.bookings).toEqual(before);
  });

  test('T12 AC4: rejects an identical interval', () => {
    const request = freshRequest(600, 660);
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(false);
    expect(request.bookings).toEqual(before);
  });

  test('T13 AC3: rejects a blocked room for an otherwise valid request', () => {
    const request = freshRequest(660, 720, { blocked: true });
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(false);
    expect(request.bookings).toEqual(before);
  });

  test('T14 AC4: allows a valid request when there are no existing bookings', () => {
    const request = freshRequest(630, 690, { bookings: [] });
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(true);
    expect(request.bookings).toEqual(before);
  });

  test('AC5: an Available decision preserves the booking array and its objects', () => {
    const request = freshRequest(660, 720);
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(true);
    expect(request.bookings).toEqual(before);
  });

  test('X1 AC1: allows an end exactly at minute 1440', () => {
    const request = freshRequest(1380, 1440);
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(true);
    expect(request.bookings).toEqual(before);
  });

  test('X2 AC4: rejects an overlap with the second booking', () => {
    const request = freshRequest(720, 780, {
      bookings: [
        { start: 600, end: 660 },
        { start: 750, end: 810 },
      ],
    });
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(false);
    expect(request.bookings).toEqual(before);
  });
});
