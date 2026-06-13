import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../../frontend/src/App.jsx';

function mockFetchSequence(responses) {
  let i = 0;
  global.fetch = vi.fn(() => {
    const res = responses[i++];
    if (!res) throw new Error('Unexpected extra fetch call');
    return Promise.resolve({
      ok: res.ok ?? true,
      status: res.status ?? 200,
      json: () => Promise.resolve(res.body ?? null),
    });
  });
}

beforeEach(() => {
  vi.restoreAllMocks();
});

afterEach(() => {
  delete global.fetch;
});

describe('App', () => {
  it('renders the notes list fetched on mount', async () => {
    const notes = [
      { _id: 1, title: 'First note', body: 'hello', createdAt: '2026-06-13T10:00:00Z' },
      { _id: 2, title: 'Second note', body: '', createdAt: '2026-06-12T10:00:00Z' },
    ];
    mockFetchSequence([{ body: notes }]);

    render(<App />);

    expect(await screen.findByText('First note')).toBeDefined();
    expect(screen.getByText('Second note')).toBeDefined();
    expect(global.fetch).toHaveBeenCalledTimes(1);
    expect(global.fetch.mock.calls[0][0]).toMatch(/\/notes$/);
  });

  it('adds a note via the form and re-fetches the list', async () => {
    const user = userEvent.setup();
    const created = {
      _id: 3,
      title: 'New note',
      body: 'b',
      createdAt: '2026-06-13T12:00:00Z',
    };
    mockFetchSequence([
      { body: [] }, // initial GET
      { status: 201, body: created }, // POST
      { body: [created] }, // re-fetch
    ]);

    render(<App />);

    await screen.findByText('No notes yet. Add one above.');

    await user.type(screen.getByLabelText('Title'), 'New note');
    await user.type(screen.getByLabelText('Body'), 'b');
    await user.click(screen.getByRole('button', { name: /save note/i }));

    expect(await screen.findByText('New note')).toBeDefined();
    expect(global.fetch).toHaveBeenCalledTimes(3);
    const postCall = global.fetch.mock.calls[1];
    expect(postCall[1].method).toBe('POST');
    expect(JSON.parse(postCall[1].body)).toEqual({ title: 'New note', body: 'b' });
  });

  it('deletes a note when the Delete button is clicked', async () => {
    const user = userEvent.setup();
    const note = { _id: 7, title: 'Doomed', body: '', createdAt: '2026-06-13T10:00:00Z' };
    mockFetchSequence([
      { body: [note] }, // initial GET
      { status: 204, body: null }, // DELETE
      { body: [] }, // re-fetch
    ]);

    render(<App />);

    const item = (await screen.findByText('Doomed')).closest('li');
    await user.click(within(item).getByRole('button', { name: /delete/i }));

    await waitFor(() =>
      expect(screen.getByText('No notes yet. Add one above.')).toBeDefined()
    );
    const deleteCall = global.fetch.mock.calls[1];
    expect(deleteCall[0]).toMatch(/\/notes\/7$/);
    expect(deleteCall[1].method).toBe('DELETE');
  });
});
