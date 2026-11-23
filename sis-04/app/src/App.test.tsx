// @vitest-environment jsdom
import { afterEach, expect, test } from 'vitest';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import App from './App';
import type { Room } from './rooms';

const catalog: Room[] = [
  { id: 'alpha', name: 'Alpha', capacity: 8, equipment: ['projector'], blocked: false, bookings: [] },
  { id: 'beta', name: 'Beta', capacity: 12, equipment: ['whiteboard'], blocked: false, bookings: [{ start: 600, end: 660 }] },
  { id: 'blocked', name: 'Blocked', capacity: 12, equipment: [], blocked: true, bookings: [] },
  { id: 'delta', name: 'Delta', capacity: 20, equipment: ['projector', 'whiteboard'], blocked: false, bookings: [] },
];

afterEach(cleanup);

test('UI01 INT F5: selecting a different room immediately refreshes feedback', () => {
  render(<App catalog={catalog} />);
  fireEvent.click(screen.getByRole('button', { name: 'Check availability' }));
  expect(screen.getByRole('status').textContent).toContain('Available — this slot is free.');
  fireEvent.click(screen.getByRole('button', { name: /Beta/ }));
  expect(screen.getByRole('status').textContent).toContain('Unavailable — this slot cannot be booked.');
  expect(screen.getByRole('status').textContent).toContain('Beta · 10:00–11:00');
});

test('UI02 INT F4: empty filtering shows guidance and disables checking', () => {
  render(<App catalog={catalog} />);
  fireEvent.change(screen.getByRole('spinbutton', { name: 'Attendees' }), { target: { value: '100' } });
  expect(screen.getByRole('heading', { name: 'No rooms match' }).textContent).toBe('No rooms match');
  expect(screen.getByRole('button', { name: 'Check availability' }).hasAttribute('disabled')).toBe(true);
  expect(screen.queryByRole('button', { name: /Alpha/ })).toBe(null);
});

test('UI03 INT F3 F5: blocked selection rejects and filtering clears old feedback', () => {
  render(<App catalog={catalog} />);
  fireEvent.click(screen.getByRole('button', { name: /Blocked/ }));
  fireEvent.click(screen.getByRole('button', { name: 'Check availability' }));
  expect(screen.getByRole('status').textContent).toContain('Unavailable — this slot cannot be booked.');
  fireEvent.change(screen.getByRole('spinbutton', { name: 'Attendees' }), { target: { value: '13' } });
  expect(screen.queryByRole('status')).toBe(null);
  expect(screen.getByRole('button', { name: /Delta/ }).getAttribute('aria-pressed')).toBe('true');
  fireEvent.click(screen.getByRole('button', { name: 'Check availability' }));
  expect(screen.getByRole('status').textContent).toContain('Available — this slot is free.');
});
