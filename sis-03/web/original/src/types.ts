export interface Room {
  id: string;
  name: string;
  building: string;
  capacity: number;
  blocked: boolean;
}

export interface Booking {
  id: string;
  roomId: string;
  title: string;
  start: number; // minutes from 00:00
  end: number; // minutes from 00:00
}

export interface AvailabilityResult {
  available: boolean;
  reasons: string[]; // empty when available
}
