import type { Booking, Room } from './types';

export const SAMPLE_ROOMS: Room[] = [
  { id: 'r1', name: 'Thesis Hall', building: 'North Wing', capacity: 120, blocked: false },
  { id: 'r2', name: 'Innovation Lab', building: 'East Wing', capacity: 30, blocked: false },
  { id: 'r3', name: 'Faculty Lounge', building: 'South Wing', capacity: 12, blocked: true },
  { id: 'r4', name: 'Project Studio B', building: 'West Wing', capacity: 24, blocked: false },
  { id: 'r5', name: 'Auditorium 9', building: 'Central', capacity: 240, blocked: false },
];

export const SAMPLE_BOOKINGS: Booking[] = [
  { id: 'b1', roomId: 'r1', title: 'Intro Algorithms Lecture', start: 540, end: 600 },
  { id: 'b2', roomId: 'r1', title: 'Faculty Review', start: 720, end: 780 },
  { id: 'b3', roomId: 'r2', title: 'Robotics Workshop', start: 600, end: 690 },
  { id: 'b4', roomId: 'r4', title: 'Design Critique', start: 810, end: 870 },
  { id: 'b5', roomId: 'r5', title: 'Guest Keynote', start: 900, end: 1020 },
  { id: 'b6', roomId: 'r2', title: 'Office Hours', start: 480, end: 540 },
];
