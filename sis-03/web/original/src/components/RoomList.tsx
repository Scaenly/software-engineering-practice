import { Clock, MapPin, Users } from 'lucide-react';
import type { Room } from '../types';
import { minutesToTime } from '../availability';

interface RoomListProps {
  rooms: Room[];
  selectedRoomId: string | null;
  onSelect: (roomId: string) => void;
  bookingsByRoom: Map<string, { start: number; end: number; title: string }[]>;
}

export default function RoomList({
  rooms,
  selectedRoomId,
  onSelect,
  bookingsByRoom,
}: RoomListProps) {
  return (
    <div className="space-y-3">
      {rooms.map((room) => {
        const isSelected = room.id === selectedRoomId;
        const roomBookings = bookingsByRoom.get(room.id) ?? [];
        return (
          <button
            key={room.id}
            type="button"
            onClick={() => onSelect(room.id)}
            className={[
              'w-full rounded-xl border p-4 text-left transition-all duration-200',
              'focus:outline-none focus:ring-2 focus:ring-sky-400 focus:ring-offset-1',
              room.blocked
                ? 'border-rose-200 bg-rose-50/60 cursor-not-allowed'
                : isSelected
                  ? 'border-sky-400 bg-sky-50 shadow-sm ring-1 ring-sky-200'
                  : 'border-slate-200 bg-white hover:border-slate-300 hover:shadow-sm',
            ].join(' ')}
            aria-pressed={isSelected}
            disabled={room.blocked}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                <h3 className="flex items-center gap-2 font-semibold text-slate-900">
                  <span className="truncate">{room.name}</span>
                  {room.blocked && (
                    <span className="rounded-full bg-rose-100 px-2 py-0.5 text-[10px] font-bold uppercase tracking-wide text-rose-700">
                      Blocked
                    </span>
                  )}
                </h3>
                <div className="mt-1 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-slate-500">
                  <span className="inline-flex items-center gap-1">
                    <MapPin className="h-3.5 w-3.5" />
                    {room.building}
                  </span>
                  <span className="inline-flex items-center gap-1">
                    <Users className="h-3.5 w-3.5" />
                    {room.capacity} seats
                  </span>
                </div>
              </div>
              <div
                className={[
                  'mt-0.5 h-3 w-3 flex-none rounded-full',
                  room.blocked ? 'bg-rose-400' : isSelected ? 'bg-sky-500' : 'bg-slate-300',
                ].join(' ')}
                aria-hidden
              />
            </div>

            {roomBookings.length > 0 && (
              <ul className="mt-3 space-y-1">
                {roomBookings
                  .slice()
                  .sort((a, b) => a.start - b.start)
                  .map((b, i) => (
                    <li
                      key={i}
                      className="flex items-center gap-2 text-xs text-slate-600"
                    >
                      <Clock className="h-3 w-3 flex-none text-slate-400" />
                      <span className="font-mono tabular-nums text-slate-700">
                        {minutesToTime(b.start)}–{minutesToTime(b.end)}
                      </span>
                      <span className="truncate text-slate-500">{b.title}</span>
                    </li>
                  ))}
              </ul>
            )}
          </button>
        );
      })}
    </div>
  );
}
