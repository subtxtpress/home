import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getProjects } from '../services/projects';

const SERVICE_COLORS = {
  'Parcel Mapping':          '#c8883a',
  'Utility GIS':             '#4e6a5e',
  'Emergency Management':    '#7d8c82',
  'Zoning & Planning':       '#c8883a',
  'Web GIS':                 '#4e6a5e',
  'GIS Training':            '#7d8c82',
};

const CLIENT_LABELS = {
  municipality: 'Municipality',
  county:       'County',
  esd:          'Emergency Services District',
  district:     'Special District',
};

export default function Portfolio() {
  const [projects, setProjects] = useState([]);
  const [loading,  setLoading]  = useState(true);
  const [filter,   setFilter]   = useState('all');

  useEffect(() => {
    getProjects()
      .then(setProjects)
      .finally(() => setLoading(false));
  }, []);

  const clientTypes = ['all', ...new Set(projects.map(p => p.clientType).filter(Boolean))];
  const filtered = filter === 'all'
    ? projects
    : projects.filter(p => p.clientType === filter);

  return (
    <main style={styles.main}>

      {/* ── Hero ── */}
      <section style={styles.hero}>
        <div style={styles.heroEyebrow}>
          <span style={styles.eyebrowLine}/>
          Case Studies &amp; Portfolio
        </div>
        <h1 style={styles.heroTitle}>
          GIS work that moves<br />
          <em style={styles.heroItalic}>Texas forward.</em>
        </h1>
        <p style={styles.heroSub}>
          A selection of Geographic Information System projects delivered to Texas municipalities,
          counties, and special districts — from parcel fabric to emergency management.
        </p>
      </section>

      {/* ── Filter ── */}
      {clientTypes.length > 1 && (
        <div style={styles.filterBar}>
          {clientTypes.map(type => (
            <button
              key={type}
              onClick={() => setFilter(type)}
              style={{
                ...styles.filterBtn,
                ...(filter === type ? styles.filterBtnActive : {}),
              }}
            >
              {type === 'all' ? 'All Projects' : CLIENT_LABELS[type] ?? type}
            </button>
          ))}
        </div>
      )}

      {/* ── Grid ── */}
      <section style={styles.grid}>
        {loading && (
          <div style={styles.loading}>
            <span style={styles.loadingText}>Loading projects…</span>
          </div>
        )}

        {!loading && filtered.length === 0 && (
          <div style={styles.empty}>
            <p style={styles.emptyTitle}>No projects yet.</p>
            <p style={styles.emptySub}>Check back soon — or <Link to="/admin" style={{ color: 'var(--ochre)' }}>add one</Link>.</p>
          </div>
        )}

        {filtered.map(project => (
          <ProjectCard key={project.id} project={project} />
        ))}
      </section>

      {/* ── CTA strip ── */}
      <section style={styles.cta}>
        <p style={styles.ctaText}>Ready to start a project?</p>
        <a href="../index.html#contact" style={styles.ctaBtn}>
          Schedule a Consultation
          <span style={{ marginLeft: '0.5rem' }}>→</span>
        </a>
      </section>

    </main>
  );
}

function ProjectCard({ project }) {
  const [hovered, setHovered] = useState(false);

  return (
    <article
      style={{ ...styles.card, ...(hovered ? styles.cardHover : {}) }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      {/* Image */}
      <div style={styles.cardImg}>
        {project.imageUrl
          ? <img src={project.imageUrl} alt={project.title} style={styles.img} />
          : <div style={styles.imgPlaceholder}>
              <PlaceholderMap />
            </div>
        }
        {project.featured && (
          <span style={styles.featuredBadge}>Featured</span>
        )}
      </div>

      {/* Body */}
      <div style={styles.cardBody}>
        <div style={styles.cardMeta}>
          <span style={styles.clientType}>{CLIENT_LABELS[project.clientType] ?? project.clientType}</span>
          {project.year && <span style={styles.year}>{project.year}</span>}
        </div>

        <h2 style={styles.cardTitle}>{project.title}</h2>
        <p  style={styles.cardClient}>{project.client}</p>
        <p  style={styles.cardSummary}>{project.summary}</p>

        {/* Services tags */}
        {project.services?.length > 0 && (
          <div style={styles.tags}>
            {project.services.map(s => (
              <span key={s} style={styles.tag}>{s}</span>
            ))}
          </div>
        )}

        {/* Outcomes */}
        {project.outcomes?.length > 0 && (
          <ul style={styles.outcomes}>
            {project.outcomes.slice(0, 3).map((o, i) => (
              <li key={i} style={styles.outcome}>
                <span style={styles.outcomeDot}>—</span> {o}
              </li>
            ))}
          </ul>
        )}

        {/* Live Demo */}
        {project.demoUrl && (
          <div style={styles.demoWrap}>
            <a
              href={project.demoUrl}
              target="_blank"
              rel="noopener noreferrer"
              style={styles.demoBtn}
            >
              {project.demoLabel || 'Live Demo'}
              <span style={{ marginLeft: '0.4rem' }}>↗</span>
            </a>
          </div>
        )}
      </div>

      {/* Hover bottom bar */}
      <div style={{
        ...styles.cardBar,
        transform: hovered ? 'scaleX(1)' : 'scaleX(0)',
      }} />
    </article>
  );
}

function PlaceholderMap() {
  return (
    <svg viewBox="0 0 400 240" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="400" height="240" fill="#1a1d18"/>
      <pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse">
        <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(200,136,58,0.08)" strokeWidth="0.5"/>
      </pattern>
      <rect width="400" height="240" fill="url(#g)"/>
      <circle cx="200" cy="120" r="80" fill="none" stroke="rgba(200,136,58,0.15)" strokeWidth="1" strokeDasharray="4 4"/>
      <circle cx="200" cy="120" r="50" fill="none" stroke="rgba(200,136,58,0.10)" strokeWidth="1" strokeDasharray="3 5"/>
      <line x1="200" y1="20"  x2="200" y2="220" stroke="rgba(200,136,58,0.08)" strokeWidth="0.5"/>
      <line x1="20"  y1="120" x2="380" y2="120" stroke="rgba(200,136,58,0.08)" strokeWidth="0.5"/>
      <circle cx="200" cy="120" r="5" fill="#c8883a" opacity="0.7"/>
    </svg>
  );
}

const styles = {
  main: { paddingTop: '6rem' },

  // Hero
  hero: {
    padding: '5rem 4rem 3rem',
    borderBottom: '1px solid var(--rule-light)',
    maxWidth: '800px',
  },
  heroEyebrow: {
    display: 'inline-flex', alignItems: 'center', gap: '0.75rem',
    fontSize: '0.68rem', letterSpacing: '0.22em', textTransform: 'uppercase',
    color: 'var(--ochre)', marginBottom: '1.5rem',
  },
  eyebrowLine: {
    display: 'inline-block', width: '2rem', height: '1px',
    background: 'var(--ochre)',
  },
  heroTitle: {
    fontFamily: 'var(--ff-serif)', fontSize: 'clamp(2.4rem,4vw,3.5rem)',
    fontWeight: 300, lineHeight: 1.1, color: 'var(--parchment)',
    marginBottom: '1.25rem',
  },
  heroItalic: { fontStyle: 'italic', color: 'var(--ochre-l)' },
  heroSub: {
    fontSize: '1rem', lineHeight: 1.7, color: 'var(--slate-l)', maxWidth: '52ch',
  },

  // Filter
  filterBar: {
    display: 'flex', gap: '0.5rem', flexWrap: 'wrap',
    padding: '1.75rem 4rem',
    borderBottom: '1px solid var(--rule-light)',
  },
  filterBtn: {
    fontFamily: 'var(--ff-sans)', fontSize: '0.7rem', fontWeight: 400,
    letterSpacing: '0.12em', textTransform: 'uppercase',
    color: 'var(--slate-l)', background: 'none',
    border: '1px solid var(--rule-light)',
    padding: '0.45rem 1rem', cursor: 'pointer',
    transition: 'all 0.2s',
  },
  filterBtnActive: {
    color: 'var(--ochre)', borderColor: 'var(--ochre)',
    background: 'rgba(200,136,58,0.06)',
  },

  // Grid
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))',
    gap: '1px',
    background: 'var(--rule-light)',
    border: '1px solid var(--rule-light)',
    margin: '3rem 4rem',
  },
  loading: {
    padding: '4rem', textAlign: 'center', background: 'var(--ink)',
    gridColumn: '1/-1',
  },
  loadingText: {
    fontFamily: 'var(--ff-serif)', fontSize: '1.1rem', color: 'var(--slate)',
  },
  empty: {
    padding: '5rem', textAlign: 'center', background: 'var(--ink)',
    gridColumn: '1/-1',
  },
  emptyTitle: {
    fontFamily: 'var(--ff-serif)', fontSize: '1.4rem', color: 'var(--parchment)',
    marginBottom: '0.5rem',
  },
  emptySub: { fontSize: '0.9rem', color: 'var(--slate)' },

  // Card
  card: {
    background: 'var(--ink)', position: 'relative', overflow: 'hidden',
    display: 'flex', flexDirection: 'column',
    transition: 'background 0.3s',
  },
  cardHover: { background: 'var(--ink-60)' },
  cardImg: { position: 'relative', height: '200px', overflow: 'hidden' },
  img: { width: '100%', height: '100%', objectFit: 'cover' },
  imgPlaceholder: { width: '100%', height: '100%' },
  featuredBadge: {
    position: 'absolute', top: '0.75rem', right: '0.75rem',
    background: 'var(--ochre)', color: 'var(--ink)',
    fontFamily: 'var(--ff-sans)', fontSize: '0.58rem', fontWeight: 500,
    letterSpacing: '0.15em', textTransform: 'uppercase',
    padding: '0.25rem 0.6rem',
  },
  cardBody: { padding: '1.75rem', flex: 1 },
  cardMeta: {
    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
    marginBottom: '0.75rem',
  },
  clientType: {
    fontSize: '0.62rem', letterSpacing: '0.16em', textTransform: 'uppercase',
    color: 'var(--ochre)',
  },
  year: { fontSize: '0.72rem', color: 'var(--slate)', fontFamily: 'var(--ff-serif)' },
  cardTitle: {
    fontFamily: 'var(--ff-serif)', fontSize: '1.3rem', fontWeight: 400,
    color: 'var(--parchment)', marginBottom: '0.3rem', lineHeight: 1.2,
  },
  cardClient: { fontSize: '0.78rem', color: 'var(--slate)', marginBottom: '0.85rem' },
  cardSummary: { fontSize: '0.85rem', lineHeight: 1.65, color: 'var(--slate-l)', marginBottom: '1.25rem' },
  tags: { display: 'flex', flexWrap: 'wrap', gap: '0.4rem', marginBottom: '1.25rem' },
  tag: {
    fontSize: '0.62rem', letterSpacing: '0.1em', textTransform: 'uppercase',
    color: 'var(--slate)', border: '1px solid var(--rule-light)',
    padding: '0.2rem 0.6rem',
  },
  outcomes: { listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.4rem' },
  outcome: { fontSize: '0.8rem', color: 'var(--slate-l)', lineHeight: 1.5 },
  outcomeDot: { color: 'var(--ochre)', marginRight: '0.3rem' },
  demoWrap: { marginTop: '1.25rem' },
  demoBtn: {
    display: 'inline-flex', alignItems: 'center',
    fontFamily: 'var(--ff-sans)', fontSize: '0.65rem', fontWeight: 500,
    letterSpacing: '0.14em', textTransform: 'uppercase',
    color: 'var(--ochre)', border: '1px solid var(--ochre)',
    padding: '0.4rem 0.9rem', textDecoration: 'none',
    transition: 'background 0.2s, color 0.2s',
  },
  cardBar: {
    position: 'absolute', bottom: 0, left: 0, right: 0,
    height: '2px', background: 'var(--ochre)',
    transformOrigin: 'left', transition: 'transform 0.4s cubic-bezier(0.16,1,0.3,1)',
  },

  // CTA
  cta: {
    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
    padding: '3rem 4rem',
    borderTop: '1px solid var(--rule-light)',
    margin: '0 4rem 4rem',
  },
  ctaText: {
    fontFamily: 'var(--ff-serif)', fontSize: '1.5rem', fontWeight: 300,
    color: 'var(--parchment)',
  },
  ctaBtn: {
    fontFamily: 'var(--ff-sans)', fontSize: '0.75rem', fontWeight: 500,
    letterSpacing: '0.14em', textTransform: 'uppercase',
    color: 'var(--ink)', background: 'var(--ochre)',
    padding: '0.9rem 2rem', display: 'inline-flex', alignItems: 'center',
  },
};
