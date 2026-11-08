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

  test('AC5: repeated Available decisions preserve unsorted booking data', () => {
    // Unsorted, distinct intervals expose an in-place sort or object mutation.
    const request = freshRequest(810, 870, {
      bookings: [
        { start: 900, end: 960 },
        { start: 600, end: 660 },
      ],
    });
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(true);
    expect(request.bookings).toEqual(before);
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

  test('T15 AC1: rejects a request starting one minute before now', () => {
    const request = freshRequest(539, 570);
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(false);
    expect(request.bookings).toEqual(before);
  });

  test('T16 AC1: allows a request starting one minute after now', () => {
    const request = freshRequest(541, 570);
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(true);
    expect(request.bookings).toEqual(before);
  });

  test('T17 AC1: rejects a negative start minute', () => {
    // This also starts before now; it does not isolate the lower-bound guard.
    const request = freshRequest(-1, 60);
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(false);
    expect(request.bookings).toEqual(before);
  });

  test('T18 AC1: rejects minute zero when the supplied current time is zero', () => {
    const request = freshRequest(0, 60, { now: 0, bookings: [] });
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(false);
    expect(request.bookings).toEqual(before);
  });

  test('T19 AC1: allows a one-minute booking just after midnight', () => {
    const request = freshRequest(1, 2, { now: 0, bookings: [] });
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(true);
    expect(request.bookings).toEqual(before);
  });

  test('T20 AC4: rejects a one-minute overlap at the existing booking end', () => {
    const request = freshRequest(659, 720);
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(false);
    expect(request.bookings).toEqual(before);
  });

  test('T21 AC4: rejects a one-minute overlap at the existing booking start', () => {
    const request = freshRequest(570, 601);
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(false);
    expect(request.bookings).toEqual(before);
  });

  test('T22 AC4: rejects an earlier conflict despite a later nonconflicting booking', () => {
    const request = freshRequest(720, 780, {
      bookings: [
        { start: 750, end: 810 },
        { start: 600, end: 660 },
      ],
    });
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(false);
    expect(request.bookings).toEqual(before);
  });

  test('T23 AC4: allows a gap touching both bookings in an unsorted schedule', () => {
    const request = freshRequest(660, 720, {
      bookings: [
        { start: 720, end: 780 },
        { start: 600, end: 660 },
      ],
    });
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(true);
    expect(request.bookings).toEqual(before);
  });

  test('T24 AC3: rejects a blocked room even with no existing bookings', () => {
    const request = freshRequest(630, 690, { blocked: true, bookings: [] });
    const before = structuredClone(request.bookings);

    expect(canBook(request)).toBe(false);
    expect(request.bookings).toEqual(before);
  });

  test('BUG-A AC4: allows a gap touching two neighbours in a three-booking schedule', () => {
    const request = freshRequest(780, 840, {
      bookings: [
        { start: 840, end: 900 },
        { start: 600, end: 660 },
        { start: 720, end: 780 },
      ],
    });

    expect(canBook(request)).toBe(true);
  });

  test('BUG-B AC5: a non-touching Available request leaves bookings unchanged', () => {
    const request = freshRequest(720, 780);
    const bookings = request.bookings;
    const before = structuredClone(bookings);

    expect(canBook(request)).toBe(true);
    expect(bookings).toEqual(before);
  });
});
