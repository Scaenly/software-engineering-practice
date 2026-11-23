import { expect, test } from 'vitest';
import { filterRooms } from './filter';
import { checkRoom } from './booking';
import type { Room } from './rooms';

// Independent fixtures: changing demo ROOMS must never change these expectations.
const catalog: Room[] = [
  { id: 'a', name: 'Test A', capacity: 8, equipment: ['projector', 'whiteboard'], blocked: false, bookings: [{ start: 600, end: 660 }] },
  { id: 'b', name: 'Test B', capacity: 12, equipment: ['projector'], blocked: false, bookings: [{ start: 720, end: 780 }] },
  { id: 'c', name: 'Test C', capacity: 7, equipment: ['whiteboard'], blocked: true, bookings: [] },
  { id: 'd', name: 'Test D', capacity: 20, equipment: ['projector', 'whiteboard', 'screen'], blocked: false, bookings: [] },
];

test('C01 F1 B5: capacity equal to attendees is included', () => {
  expect(filterRooms(catalog, { attendees: 8, equipment: [] }).map(room => room.id)).toEqual(['a', 'b', 'd']);
});

test('C02 F1 B6: capacity one below attendees is excluded', () => {
  expect(filterRooms(catalog, { attendees: 8, equipment: [] }).map(room => room.id)).not.toContain('c');
});

test('C03 F2: all selected equipment is required', () => {
  expect(filterRooms(catalog, { attendees: 1, equipment: ['projector', 'whiteboard'] }).map(room => room.id)).toEqual(['a', 'd']);
});

test('C04 F2: no equipment selected adds no restriction', () => {
  expect(filterRooms(catalog, { attendees: 1, equipment: [] }).map(room => room.id)).toEqual(['a', 'b', 'c', 'd']);
});

test('C05 F4: impossible capacity gives the empty-state input', () => {
  expect(filterRooms(catalog, { attendees: 21, equipment: [] })).toEqual([]);
});

test('C06 F1 F2: combined filters leave the qualifying room', () => {
  expect(filterRooms(catalog, { attendees: 9, equipment: ['projector', 'whiteboard'] }).map(room => room.id)).toEqual(['d']);
});

test('C07 F3 AC3: a blocked room is never available', () => {
  expect(checkRoom(catalog, 'c', { start: 660, end: 720, now: 540 })).toBe(false);
});

test('C08 F5: switching room uses its own bookings at identical times', () => {
  const request = { start: 600, end: 630, now: 540 };
  expect(checkRoom(catalog, 'a', request)).toBe(false);
  expect(checkRoom(catalog, 'b', request)).toBe(true);
});

test('C09 F5: an unknown room is unavailable', () => {
  expect(checkRoom(catalog, 'missing', { start: 660, end: 720, now: 540 })).toBe(false);
});

test('C10 AC5: filtering and checking leave the complete catalog unchanged', () => {
  const before = structuredClone(catalog);
  const criteria = { attendees: 8, equipment: ['projector'] };
  const request = { start: 660, end: 720, now: 540 };
  const inputs = structuredClone({ criteria, request });
  const matches = filterRooms(catalog, criteria);
  expect(checkRoom(matches, 'a', request)).toBe(true);
  expect(checkRoom(matches, 'a', request)).toBe(true);
  expect(catalog).toEqual(before);
  expect({ criteria, request }).toEqual(inputs);
});

test('C11 INT: check a room returned by the combined filter', () => {
  const matches = filterRooms(catalog, { attendees: 9, equipment: ['projector', 'whiteboard'] });
  expect(matches.map(room => room.id)).toEqual(['d']);
  expect(checkRoom(matches, matches[0].id, { start: 600, end: 630, now: 540 })).toBe(true);
});

test('C12 F2 F4: absent equipment produces no matching rooms', () => {
  expect(filterRooms(catalog, { attendees: 1, equipment: ['microscope'] })).toEqual([]);
});

test('C13 F1 F4: invalid attendees produce no matching rooms', () => {
  expect(filterRooms(catalog, { attendees: 0, equipment: [] })).toEqual([]);
  expect(filterRooms(catalog, { attendees: Number.NaN, equipment: [] })).toEqual([]);
  expect(filterRooms(catalog, { attendees: 1.5, equipment: [] })).toEqual([]);
});

test('C14 INT F3: filtering never overrides a blocked room', () => {
  const matches = filterRooms(catalog, { attendees: 7, equipment: ['whiteboard'] });
  expect(matches.map(room => room.id)).toContain('c');
  expect(checkRoom(matches, 'c', { start: 660, end: 720, now: 540 })).toBe(false);
});
