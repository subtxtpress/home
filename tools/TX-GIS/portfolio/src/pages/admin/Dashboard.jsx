import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getProjects, deleteProject, updateProject } from '../../services/projects';

const CLIENT_LABELS = {
  municipality: 'Municipality',
  county:       'County',
  esd:          'ESD',
  district:     'Special District',
};

export default function Dashboard() {
  const [projects, setProjects] = useState([]);
  const [loading,  setLoading]  = useState(true);
  const [deleting, setDeleting] = useState(null);

  async function load() {
    setLoading(true);
    try { setProjects(await getProjects()); }
    finally { setLoading(false); }
  }

  useEffect(() => { load(); }, []);

  async function handleDelete(id) {
    if (!window.confirm('Delete this project? This cannot be undone.')) return;
    setDeleting(id);
    try { await deleteProject(id); await load(); }
    finally { setDeleting(null); }
  }

  async function toggleFeatured(project) {
    await updateProject(project.id, { featured: !project.featured });
    await load();
  }

  return (
    <main style={styles.main}>

      {/* Header */}
      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>Portfolio Admin</h1>
          <p  style={styles.sub}>{projects.length} project{projects.length !== 1 ? 's' : ''}</p>
        </div>
        <Link to="/admin/projects/new" style={styles.btnNew}>
          + New Project
        </Link>
      </div>

      {/* Table */}
      {loading ? (
        <p style={styles.loading}>Loading…</p>
      ) : projects.length === 0 ? (
        <div style={styles.empty}>
          <p style={styles.emptyTitle}>No projects yet.</p>
          <Link to="/admin/projects/new" style={{ color: 'var(--ochre)', fontSize: '0.9rem' }}>
            Create your first project →
          </Link>
        </div>
      ) : (
        <div style={styles.tableWrap}>
          <table style={styles.table}>
            <thead>
              <tr>
                {['Order','Title','Client','Type','Year','Featured',''].map(h => (
                  <th key={h} style={styles.th}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {projects.map(p => (
                <tr key={p.id} style={styles.tr}>
                  <td style={styles.td}>{p.order ?? '—'}</td>
                  <td style={{ ...styles.td, ...styles.tdTitle }}>{p.title}</td>
                  <td style={styles.td}>{p.client}</td>
                  <td style={styles.td}>{CLIENT_LABELS[p.clientType] ?? p.clientType}</td>
                  <td style={styles.td}>{p.year}</td>
                  <td style={styles.td}>
                    <button
                      onClick={() => toggleFeatured(p)}
                      style={{ ...styles.featuredToggle, ...(p.featured ? styles.featuredOn : {}) }}
                    >
                      {p.featured ? '★ Featured' : '☆ Feature'}
                    </button>
                  </td>
                  <td style={{ ...styles.td, ...styles.tdActions }}>
                    <Link to={`/admin/projects/${p.id}/edit`} style={styles.btnEdit}>Edit</Link>
                    <button
                      onClick={() => handleDelete(p.id)}
                      disabled={deleting === p.id}
                      style={styles.btnDelete}
                    >
                      {deleting === p.id ? '…' : 'Delete'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

    </main>
  );
}

const styles = {
  main:  { padding: '7rem 4rem 4rem', maxWidth: '1200px', margin: '0 auto' },
  header: {
    display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between',
    marginBottom: '2.5rem', paddingBottom: '2rem',
    borderBottom: '1px solid var(--rule-light)',
  },
  title: {
    fontFamily: 'var(--ff-serif)', fontSize: '2rem', fontWeight: 300,
    color: 'var(--parchment)',
  },
  sub: { fontSize: '0.78rem', color: 'var(--slate)', marginTop: '0.25rem' },
  btnNew: {
    fontFamily: 'var(--ff-sans)', fontSize: '0.75rem', fontWeight: 500,
    letterSpacing: '0.12em', textTransform: 'uppercase',
    background: 'var(--ochre)', color: 'var(--ink)',
    padding: '0.8rem 1.75rem', border: 'none', cursor: 'pointer',
  },
  loading: { fontFamily: 'var(--ff-serif)', color: 'var(--slate)', fontSize: '1rem', padding: '2rem 0' },
  empty:   { padding: '4rem', textAlign: 'center', border: '1px solid var(--rule-light)' },
  emptyTitle: { fontFamily: 'var(--ff-serif)', fontSize: '1.3rem', color: 'var(--parchment)', marginBottom: '0.75rem' },
  tableWrap: { overflowX: 'auto' },
  table: { width: '100%', borderCollapse: 'collapse' },
  th: {
    fontFamily: 'var(--ff-sans)', fontSize: '0.6rem', fontWeight: 400,
    letterSpacing: '0.18em', textTransform: 'uppercase', color: 'var(--ochre)',
    padding: '0.75rem 1rem', borderBottom: '1px solid var(--rule)',
    textAlign: 'left', whiteSpace: 'nowrap',
  },
  tr: { borderBottom: '1px solid var(--rule-light)' },
  td: { padding: '1rem', fontSize: '0.85rem', color: 'var(--slate-l)', verticalAlign: 'middle' },
  tdTitle: { color: 'var(--parchment)', fontFamily: 'var(--ff-serif)', fontSize: '0.95rem' },
  tdActions: { display: 'flex', gap: '0.75rem', alignItems: 'center' },
  featuredToggle: {
    fontFamily: 'var(--ff-sans)', fontSize: '0.65rem', letterSpacing: '0.1em',
    background: 'none', border: '1px solid var(--rule-light)',
    color: 'var(--slate)', padding: '0.3rem 0.65rem', cursor: 'pointer',
  },
  featuredOn: { borderColor: 'var(--ochre)', color: 'var(--ochre)' },
  btnEdit: {
    fontFamily: 'var(--ff-sans)', fontSize: '0.68rem', letterSpacing: '0.1em',
    color: 'var(--slate-l)', border: '1px solid var(--rule-light)',
    padding: '0.3rem 0.75rem',
  },
  btnDelete: {
    fontFamily: 'var(--ff-sans)', fontSize: '0.68rem', letterSpacing: '0.1em',
    color: '#e07070', background: 'none', border: '1px solid rgba(224,112,112,0.2)',
    padding: '0.3rem 0.75rem', cursor: 'pointer',
  },
};
