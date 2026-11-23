import { EQUIPMENT } from '../rooms';

type Props = {
  attendees: number;
  equipment: string[];
  onAttendees: (value: number) => void;
  onEquipment: (value: string[]) => void;
};

export default function RoomFilters({ attendees, equipment, onAttendees, onEquipment }: Props) {
  return (
    <div className="mb-4 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <label className="block text-sm font-medium text-slate-700">
        Attendees
        <input type="number" min="1" step="1" value={attendees || ''}
          onChange={event => onAttendees(Number(event.target.value))}
          className="ml-3 w-24 rounded-lg border border-slate-300 px-3 py-2" />
      </label>
      <fieldset className="mt-3">
        <legend className="text-xs font-semibold text-slate-500">Required equipment — all selected items</legend>
        <div className="mt-2 flex flex-wrap gap-4">
          {EQUIPMENT.map(item => (
            <label key={item} className="flex items-center gap-2 py-1 text-sm capitalize text-slate-600">
              <input type="checkbox" checked={equipment.includes(item)}
                onChange={event => onEquipment(event.target.checked ? [...equipment, item] : equipment.filter(value => value !== item))}
                className="h-4 w-4 accent-sky-600" />
              {item}
            </label>
          ))}
        </div>
      </fieldset>
    </div>
  );
}
