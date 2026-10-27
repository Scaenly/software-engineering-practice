import { useEffect, useMemo, useState } from 'react';
import { CheckCircle2, Clock4, DoorClosed, XCircle } from 'lucide-react';
import RoomList from './components/RoomList';
import { SAMPLE_BOOKINGS, SAMPLE_ROOMS } from './sampleData';
import {
  MAX_BOOKING_MINUTES_VALUE,
  MINUTES_PER_DAY_VALUE,
  checkAvailability,
  minutesToTime,
  timeToMinutes,
} from './availability';
import type { AvailabilityResult, Booking, Room } from './types';

function useNowMinutes(): number {
  const [now, setNow] = useState(() => {
    const d = new Date();
    return d.getHours() * 60 + d.getMinutes();
  });
  useEffect(() => {
    const id = window.setInterval(() => {
      const d = new Date();
      setNow(d.getHours() * 60 + d.getMinutes());
    }, 30_000);
    return () => window.clearInterval(id);
  }, []);
  return now;
}

export default function App() {
  const [rooms] = useState<Room[]>(SAMPLE_ROOMS);
  const [bookings] = useState<Booking[]>(SAMPLE_BOOKINGS);
  const nowMinutes = useNowMinutes();

  const [selectedRoomId, setSelectedRoomId] = useState<string | null>(SAMPLE_ROOMS[0].id ?? null);
  const [startTime, setStartTime] = useState('09:00');
  const [endTime, setEndTime] = useState('10:00');
  const [result, setResult] = useState<AvailabilityResult | null>(null);

  const selectedRoom = useMemo(
    () => rooms.find((r) => r.id === selectedRoomId) ?? null,
    [rooms, selectedRoomId],
  );

  const bookingsByRoom = useMemo(() => {
    const map = new Map<string, { start: number; end: number; title: string }[]>();
    for (const b of bookings) {
      const arr = map.get(b.roomId) ?? [];
      arr.push({ start: b.start, end: b.end, title: b.title });
      map.set(b.roomId, arr);
    }
    return map;
  }, [bookings]);

  const startMin = timeToMinutes(startTime);
  const endMin = timeToMinutes(endTime);

  function handleCheck(e: React.FormEvent) {
    e.preventDefault();
    if (startMin === null || endMin === null) {
      setResult({
        available: false,
        reasons: ['Enter valid times in HH:MM (24-hour) format.'],
      });
      return;
    }
    setResult(checkAvailability(selectedRoom, startMin, endMin, nowMinutes, bookings));
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-slate-50 to-sky-50 text-slate-900">
      <div className="mx-auto flex min-h-screen max-w-6xl flex-col px-4 py-6 sm:px-6 lg:py-10">
        {/* Header */}
        <header className="mb-6 flex flex-col gap-3 sm:mb-8 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full bg-sky-100 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-sky-700">
              <DoorClosed className="h-3.5 w-3.5" />
              Campus Facilities
            </div>
            <h1 className="mt-3 text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl">
              Smart Campus Room Availability
            </h1>
            <p className="mt-1 max-w-2xl text-sm text-slate-600">
              Check whether a room is free for your requested time slot before booking it.
              Touching endpoints are allowed; bookings are capped at 120 minutes.
            </p>
          </div>
          <div className="inline-flex items-center gap-2 self-start rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm shadow-sm sm:self-auto">
            <Clock4 className="h-4 w-4 text-slate-500" />
            <span className="text-slate-500">Current time</span>
            <span className="font-mono font-semibold tabular-nums text-slate-900">
              {minutesToTime(nowMinutes)}
            </span>
          </div>
        </header>

        <div className="grid flex-1 gap-6 lg:grid-cols-5">
          {/* Room picker */}
          <section className="lg:col-span-3" aria-label="Available rooms">
            <div className="mb-3 flex items-baseline justify-between">
              <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500">
                Rooms
              </h2>
              <span className="text-xs text-slate-400">{rooms.length} total</span>
            </div>
            <RoomList
              rooms={rooms}
              selectedRoomId={selectedRoomId}
              onSelect={setSelectedRoomId}
              bookingsByRoom={bookingsByRoom}
            />
          </section>

          {/* Checker panel */}
          <section className="lg:col-span-2" aria-label="Availability checker">
            <form
              onSubmit={handleCheck}
              className="sticky top-6 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
            >
              <h2 className="text-base font-semibold text-slate-900">Check a time slot</h2>
              <p className="mt-1 text-xs text-slate-500">
                Times are 24-hour. A slot must start after the current time and end within the day
                ({minutesToTime(0)}–{minutesToTime(MINUTES_PER_DAY_VALUE)}).
              </p>

              <div className="mt-4 grid grid-cols-2 gap-3">
                <label className="block">
                  <span className="text-xs font-medium text-slate-600">Start</span>
                  <input
                    type="time"
                    value={startTime}
                    onChange={(e) => {
                      setStartTime(e.target.value);
                      setResult(null);
                    }}
                    className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm font-mono tabular-nums focus:border-sky-400 focus:outline-none focus:ring-2 focus:ring-sky-200"
                    aria-label="Start time"
                  />
                </label>
                <label className="block">
                  <span className="text-xs font-medium text-slate-600">End</span>
                  <input
                    type="time"
                    value={endTime}
                    onChange={(e) => {
                      setEndTime(e.target.value);
                      setResult(null);
                    }}
                    className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm font-mono tabular-nums focus:border-sky-400 focus:outline-none focus:ring-2 focus:ring-sky-200"
                    aria-label="End time"
                  />
                </label>
              </div>

              <div className="mt-3 rounded-lg bg-slate-50 px-3 py-2 text-xs text-slate-500">
                {selectedRoom ? (
                  <>
                    Checking <span className="font-semibold text-slate-700">{selectedRoom.name}</span>
                    {' · '}Max length {MAX_BOOKING_MINUTES_VALUE} min
                  </>
                ) : (
                  'Select a room to check.'
                )}
              </div>

              <button
                type="submit"
                className="mt-4 w-full rounded-lg bg-sky-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-sky-700 focus:outline-none focus:ring-2 focus:ring-sky-300 focus:ring-offset-1"
              >
                Check availability
              </button>

              {result && (
                <div
                  role="status"
                  className={[
                    'mt-4 rounded-xl border p-4 transition-all',
                    result.available
                      ? 'border-emerald-200 bg-emerald-50'
                      : 'border-rose-200 bg-rose-50',
                  ].join(' ')}
                >
                  <div className="flex items-center gap-2">
                    {result.available ? (
                      <CheckCircle2 className="h-5 w-5 flex-none text-emerald-600" />
                    ) : (
                      <XCircle className="h-5 w-5 flex-none text-rose-600" />
                    )}
                    <p
                      className={[
                        'text-sm font-semibold',
                        result.available ? 'text-emerald-800' : 'text-rose-800',
                      ].join(' ')}
                    >
                      {result.available
                        ? 'Available — this slot is free.'
                        : 'Unavailable — this slot cannot be booked.'}
                    </p>
                  </div>
                  {result.reasons.length > 0 && (
                    <ul className="mt-2 list-disc space-y-1 pl-5 text-xs text-rose-700">
                      {result.reasons.map((r, i) => (
                        <li key={i}>{r}</li>
                      ))}
                    </ul>
                  )}
                </div>
              )}

              <p className="mt-4 text-[11px] leading-relaxed text-slate-400">
                This checker only reads existing booking data to produce a decision — it never
                modifies the schedule.
              </p>
            </form>
          </section>
        </div>

        <footer className="mt-8 border-t border-slate-200 pt-4 text-center text-xs text-slate-400">
          Fictional sample data · Campus Facilities demo
        </footer>
      </div>
    </div>
  );
}
