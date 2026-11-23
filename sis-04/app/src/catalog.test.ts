import { expect, test } from 'vitest';
import { filterRooms } from './filter';
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
