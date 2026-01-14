import { useEffect, useMemo, useState } from 'react';

const defaultApiUrl = 'http://localhost:4000/api';

export default function App() {
  const [notes, setNotes] = useState([]);
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const apiUrl = useMemo(
    () => import.meta.env.VITE_API_URL?.replace(/\/$/, '') || defaultApiUrl,
    []
  );

  useEffect(() => {
    fetchNotes();
  }, [apiUrl]);

  async function fetchNotes() {
    try {
      setLoading(true);
      setError('');
      const res = await fetch(`${apiUrl}/notes`);
      const data = await res.json();
      setNotes(data);
    } catch (err) {
      setError('Could not load notes');
    } finally {
      setLoading(false);
    }
  }

  async function addNote(e) {
    e.preventDefault();
    if (!title.trim()) return setError('Title is required');
    try {
      setError('');
      const res = await fetch(`${apiUrl}/notes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: title.trim(), body }),
      });
      if (!res.ok) throw new Error('Failed to save note');
      setTitle('');
      setBody('');
      await fetchNotes();
    } catch (err) {
      setError('Failed to save note');
    }
  }

  async function deleteNote(id) {
    try {
      await fetch(`${apiUrl}/notes/${id}`, { method: 'DELETE' });
      await fetchNotes();
    } catch (err) {
      setError('Failed to delete note');
    }
  }

  return (
    <main className="page">
      <header>
        <div>
          <p className="eyebrow">MERN • AWS</p>
          <h1>Notes on the Cloud</h1>
          <p className="subhead">
            Simple notes app deployed with React, Express, and Postgres on AWS.
          </p>
        </div>
        <span className="env">API: {apiUrl}</span>
      </header>

      <section className="card">
        <form onSubmit={addNote}>
          <div className="field">
            <label htmlFor="title">Title</label>
            <input
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Take deployment notes..."
              required
            />
          </div>
          <div className="field">
            <label htmlFor="body">Body</label>
            <textarea
              id="body"
              value={body}
              onChange={(e) => setBody(e.target.value)}
              placeholder="What changed, links, or commands..."
              rows={4}
            />
          </div>
          <div className="actions">
            <button type="submit">Save note</button>
            <button type="button" className="ghost" onClick={fetchNotes}>
              Refresh
            </button>
          </div>
        </form>
      </section>

      <section className="list card">
        <div className="list-head">
          <h2>Recent notes</h2>
          {loading && <span className="badge">Loading...</span>}
          {error && <span className="error">{error}</span>}
        </div>
        {notes.length === 0 && !loading ? (
          <p className="muted">No notes yet. Add one above.</p>
        ) : (
          <ul>
            {notes.map((note) => (
              <li key={note._id}>
                <div>
                  <h3>{note.title}</h3>
                  {note.body && <p>{note.body}</p>}
                  <p className="meta">
                    {new Date(note.createdAt).toLocaleString()}
                  </p>
                </div>
                <button className="ghost" onClick={() => deleteNote(note._id)}>
                  Delete
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
