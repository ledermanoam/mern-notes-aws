import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { Pool } from 'pg';

dotenv.config();

const app = express();
const port = process.env.PORT || 4000;
const corsOrigin = process.env.CORS_ORIGIN || '*';

app.use(cors({ origin: corsOrigin, credentials: true }));
app.use(express.json());

let pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.DATABASE_SSL === 'true' ? { rejectUnauthorized: false } : false,
});

export function setPool(newPool) {
  pool = newPool;
}

async function ensureTable() {
  const createSql = `
    CREATE TABLE IF NOT EXISTS notes (
      id SERIAL PRIMARY KEY,
      title TEXT NOT NULL,
      body TEXT DEFAULT '',
      created_at TIMESTAMPTZ DEFAULT NOW()
    );
  `;
  await pool.query(createSql);
}

app.get('/api/health', async (_req, res) => {
  try {
    await pool.query('SELECT 1');
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
  } catch (err) {
    res.status(500).json({ status: 'error', message: err.message });
  }
});

app.get('/api/notes', async (_req, res) => {
  try {
    const { rows } = await pool.query(
      'SELECT id AS "_id", title, body, created_at AS "createdAt" FROM notes ORDER BY created_at DESC'
    );
    res.json(rows);
  } catch (err) {
    res.status(500).json({ message: 'Failed to list notes', error: err.message });
  }
});

app.post('/api/notes', async (req, res) => {
  const { title, body = '' } = req.body || {};
  if (!title) return res.status(400).json({ message: 'Title is required' });

  try {
    const { rows } = await pool.query(
      'INSERT INTO notes (title, body) VALUES ($1, $2) RETURNING id AS "_id", title, body, created_at AS "createdAt"',
      [title, body]
    );
    res.status(201).json(rows[0]);
  } catch (err) {
    res.status(500).json({ message: 'Failed to create note', error: err.message });
  }
});

app.delete('/api/notes/:id', async (req, res) => {
  const id = Number(req.params.id);
  if (!Number.isInteger(id)) return res.status(400).json({ message: 'Invalid id' });

  try {
    await pool.query('DELETE FROM notes WHERE id = $1', [id]);
    res.status(204).send();
  } catch (err) {
    res.status(500).json({ message: 'Failed to delete note', error: err.message });
  }
});

async function start() {
  if (!process.env.DATABASE_URL) {
    console.error('DATABASE_URL is required');
    process.exit(1);
  }

  try {
    await ensureTable();
    console.log('Connected to Postgres');

    app.listen(port, () => {
      console.log(`API listening on port ${port}`);
    });
  } catch (err) {
    console.error('Failed to start server:', err.message);
    process.exit(1);
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  start();
}

export { app };
