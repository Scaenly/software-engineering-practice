import type { Booking, Room } from './types';

export const SAMPLE_ROOMS: Room[] = [
  { id: 'r1', name: 'Demo Room', building: 'Fictional Campus', capacity: 12, blocked: false },
];

export const SAMPLE_BOOKINGS: Booking[] = [
  { id: 'b1', roomId: 'r1', title: 'Fictional session A', start: 540, end: 600 },
  { id: 'b2', roomId: 'r1', title: 'Fictional session B', start: 720, end: 780 },
];
