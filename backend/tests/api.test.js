import { describe, it, expect, beforeEach, vi } from 'vitest';
import request from 'supertest';
import { app, setPool } from '../server.js';

// Minimal in-memory mock of pg.Pool
function createMockPool() {
  return {
    query: vi.fn(),
  };
}

let pool;

beforeEach(() => {
  pool = createMockPool();
  setPool(pool);
});

describe('GET /api/health', () => {
  it('returns 200 with status ok when DB ping succeeds', async () => {
    pool.query.mockResolvedValueOnce({ rows: [{ '?column?': 1 }] });

    const res = await request(app).get('/api/health');

    expect(res.status).toBe(200);
    expect(res.body.status).toBe('ok');
    expect(res.body.timestamp).toBeDefined();
    expect(pool.query).toHaveBeenCalledWith('SELECT 1');
  });
});

describe('GET /api/notes', () => {
  it('returns 200 with notes ordered by created_at DESC', async () => {
    const rows = [
      { _id: 2, title: 'Newer', body: 'b', createdAt: '2026-06-13T12:00:00Z' },
      { _id: 1, title: 'Older', body: '', createdAt: '2026-06-12T12:00:00Z' },
    ];
    pool.query.mockResolvedValueOnce({ rows });

    const res = await request(app).get('/api/notes');

    expect(res.status).toBe(200);
    expect(res.body).toEqual(rows);
    expect(pool.query.mock.calls[0][0]).toMatch(/ORDER BY created_at DESC/);
  });
});

describe('POST /api/notes', () => {
  it('returns 201 with the created note on happy path', async () => {
    const created = {
      _id: 1,
      title: 'Hello',
      body: 'world',
      createdAt: '2026-06-13T12:00:00Z',
    };
    pool.query.mockResolvedValueOnce({ rows: [created] });

    const res = await request(app)
      .post('/api/notes')
      .send({ title: 'Hello', body: 'world' });

    expect(res.status).toBe(201);
    expect(res.body).toEqual(created);
    expect(pool.query).toHaveBeenCalledWith(
      expect.stringMatching(/INSERT INTO notes/),
      ['Hello', 'world']
    );
  });

  it('returns 400 when title is missing', async () => {
    const res = await request(app).post('/api/notes').send({ body: 'no title' });

    expect(res.status).toBe(400);
    expect(res.body.message).toBe('Title is required');
    expect(pool.query).not.toHaveBeenCalled();
  });
});

describe('DELETE /api/notes/:id', () => {
  it('returns 204 on happy path', async () => {
    pool.query.mockResolvedValueOnce({ rowCount: 1 });

    const res = await request(app).delete('/api/notes/42');

    expect(res.status).toBe(204);
    expect(pool.query).toHaveBeenCalledWith(
      'DELETE FROM notes WHERE id = $1',
      [42]
    );
  });

  it('returns 400 when id is not an integer', async () => {
    const res = await request(app).delete('/api/notes/not-a-number');

    expect(res.status).toBe(400);
    expect(res.body.message).toBe('Invalid id');
    expect(pool.query).not.toHaveBeenCalled();
  });
});
