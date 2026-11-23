export type Room = {
  id: string;
  name: string;
  building?: string;
  capacity: number;
  equipment: string[];
  blocked: boolean;
  bookings: { start: number; end: number; title?: string }[];
};

// Fictional catalog. The clock is fixed at 09:00 for a repeatable demo.
export const DEMO_NOW = 540;
export const EQUIPMENT = ['projector', 'whiteboard', 'screen'];

export const ROOMS: Room[] = [
  { id: 'r1', name: 'Thesis Hall', building: 'North Wing', capacity: 120, equipment: ['projector', 'whiteboard', 'screen'], blocked: false,
    bookings: [{ start: 540, end: 600, title: 'Algorithms seminar' }, { start: 720, end: 780, title: 'Faculty review' }] },
  { id: 'r2', name: 'Innovation Lab', building: 'East Wing', capacity: 30, equipment: ['projector', 'whiteboard'], blocked: false,
    bookings: [{ start: 600, end: 690, title: 'Robotics workshop' }, { start: 480, end: 540, title: 'Office hours' }] },
  { id: 'r3', name: 'Faculty Lounge', building: 'South Wing', capacity: 12, equipment: ['whiteboard'], blocked: true,
    bookings: [] },
  { id: 'r4', name: 'Project Studio B', building: 'West Wing', capacity: 24, equipment: ['whiteboard', 'screen'], blocked: false,
    bookings: [{ start: 810, end: 870, title: 'Design critique' }] },
  { id: 'r5', name: 'Auditorium 9', building: 'Central', capacity: 240, equipment: ['projector', 'screen'], blocked: false,
    bookings: [{ start: 900, end: 1020, title: 'Guest keynote' }] },
];
