import { useState, useEffect, useRef } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { createProject, updateProject, getProject } from '../../services/projects';
import { uploadProjectImage } from '../../services/storage';

const SERVICE_OPTIONS = [
  'Parcel Mapping', 'Utility GIS', 'Emergency Management',
  'Zoning & Planning', 'Web GIS', 'GIS Training', 'Spatial Analysis',
  'Infrastructure Planning', 'FEMA Compliance',
];

const CLIENT_TYPES = [
  { value: 'municipality', label: 'City / Municipality' },
  { value: 'county',       label: 'County Government'  },
  { value: 'esd',          label: 'Emergency Services District' },
  { value: 'district',     label: 'Special Purpose District' },
];

const EMPTY = {
  title: '', client: '', clientType: 'municipality', year: new Date().getFullYear(),
  services: [], summary: '', description: '', outcomes: [],
  imageUrl: '', featured: false, order: 0,
  demoUrl: '', demoLabel: '',
};

export default function ProjectForm() {
  const { id }     = useParams();
  const navigate   = useNavigate();
  const isEdit     = Boolean(id);
  const fileRef    = useRef();

  const [form,     setForm]     = useState(EMPTY);
  const [loading,  setLoading]  = useState(isEdit);
  const [saving,   setSaving]   = useState(false);
  const [error,    setError]    = useState('');
  const [upload,   setUpload]   = useState(null); // { progress, name }
  const [outcome,  setOutcome]  = useState('');   // scratch input for outcomes

  useEffect(() => {
    if (!isEdit) return;
    getProject(id).then(p => {
      if (p) setForm({ ...EMPTY, ...p });
    }).finally(() => setLoading(false));
  }, [id]);

  function set(key, val) {
    setForm(f => ({ ...f, [key]: val }));
  }

  function toggleService(s) {
    set('services', form.services.includes(s)
      ? form.services.filter(x => x !== s)
      : [...form.services, s]
    );
  }

  function addOutcome() {
    if (!outcome.trim()) return;
    set('outcomes', [...form.outcomes, outcome.trim()]);
    setOutcome('');
  }

  function removeOutcome(i) {
    set('outcomes', form.outcomes.filter((_, idx) => idx !== i));
  }

  async function handleImageUpload(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    const tempId = id || `temp_${Date.now()}`;
    setUpload({ progress: 0, name: file.name });
    try {
      const { url } = await uploadProjectImage(file, tempId, p => setUpload(u => ({ ...u, progress: p })));
      set('imageUrl', url);
    } catch {
      setError('Image upload failed. Please try again.');
    } finally {
      setUpload(null);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError(''); setSaving(true);
    try {
      if (isEdit) {
        await updateProject(id, form);
      } else {
        await createProject(form);
      }
      navigate('/admin');
    } catch (err) {
      setError('Save failed: ' + err.message);
    } finally {
      setSaving(false);
    }
  }

  if (loading) return (
    <main style={styles.main}>
      <p style={styles.loadingText}>Loading project…</p>
    </main>
  );

  return (
    <main style={styles.main}>
      <div style={styles.header}>
        <h1 style={styles.title}>{isEdit ? 'Edit Project' : 'New Project'}</h1>
        <button onClick={() => navigate('/admin')} style={styles.btnBack}>← Back</button>
      </div>

      <form onSubmit={handleSubmit} style={styles.form}>

        {/* ── Section: Basic Info ── */}
        <section style={styles.section}>
          <h2 style={styles.sectionTitle}>Basic Information</h2>
          <div style={styles.row}>
            <Field label="Project Title *" style={{ flex: 2 }}>
              <input required value={form.title}
                onChange={e => set('title', e.target.value)}
                style={styles.input} placeholder="e.g. City of Waco Utility GIS Inventory" />
            </Field>
            <Field label="Year" style={{ flex: 0.5 }}>
              <input type="number" value={form.year} min="2000" max="2099"
                onChange={e => set('year', +e.target.value)}
                style={styles.input} />
            </Field>
            <Field label="Display Order" style={{ flex: 0.5 }}>
              <input type="number" value={form.order} min="0"
                onChange={e => set('order', +e.target.value)}
                style={styles.input} />
            </Field>
          </div>
          <div style={styles.row}>
            <Field label="Client Name *" style={{ flex: 2 }}>
              <input required value={form.client}
                onChange={e => set('client', e.target.value)}
                style={styles.input} placeholder="e.g. City of Waco, TX" />
            </Field>
            <Field label="Client Type *" style={{ flex: 1 }}>
              <select value={form.clientType}
                onChange={e => set('clientType', e.target.value)}
                style={{ ...styles.input, ...styles.select }}>
                {CLIENT_TYPES.map(t => (
                  <option key={t.value} value={t.value}>{t.label}</option>
                ))}
              </select>
            </Field>
          </div>
          <div style={styles.checkRow}>
            <label style={styles.checkLabel}>
              <input type="checkbox" checked={form.featured}
                onChange={e => set('featured', e.target.checked)}
                style={styles.checkbox} />
              <span>Feature on portfolio homepage</span>
            </label>
          </div>
        </section>

        {/* ── Section: Description ── */}
        <section style={styles.section}>
          <h2 style={styles.sectionTitle}>Description</h2>
          <Field label="Short Summary * (shown on card)">
            <textarea required rows={2} value={form.summary}
              onChange={e => set('summary', e.target.value)}
              style={{ ...styles.input, ...styles.textarea }}
              placeholder="1–2 sentences describing the project." />
          </Field>
          <Field label="Full Description">
            <textarea rows={6} value={form.description}
              onChange={e => set('description', e.target.value)}
              style={{ ...styles.input, ...styles.textarea }}
              placeholder="Detailed project description, scope, approach…" />
          </Field>
        </section>

        {/* ── Section: Outcomes ── */}
        <section style={styles.section}>
          <h2 style={styles.sectionTitle}>Outcomes &amp; Results</h2>
          <div style={styles.row}>
            <input value={outcome} onChange={e => setOutcome(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && (e.preventDefault(), addOutcome())}
              style={{ ...styles.input, flex: 1 }}
              placeholder="e.g. Reduced meter reading errors by 40%" />
            <button type="button" onClick={addOutcome} style={styles.btnAdd}>Add</button>
          </div>
          {form.outcomes.length > 0 && (
            <ul style={styles.outcomeList}>
              {form.outcomes.map((o, i) => (
                <li key={i} style={styles.outcomeItem}>
                  <span style={{ color: 'var(--ochre)', marginRight: '0.5rem' }}>—</span>
                  {o}
                  <button type="button" onClick={() => removeOutcome(i)} style={styles.btnRemove}>×</button>
                </li>
              ))}
            </ul>
          )}
        </section>

        {/* ── Section: Services ── */}
        <section style={styles.section}>
          <h2 style={styles.sectionTitle}>Services Provided</h2>
          <div style={styles.serviceGrid}>
            {SERVICE_OPTIONS.map(s => (
              <label key={s} style={styles.serviceLabel}>
                <input type="checkbox"
                  checked={form.services.includes(s)}
                  onChange={() => toggleService(s)}
                  style={styles.checkbox} />
                <span style={form.services.includes(s) ? styles.serviceActive : {}}>
                  {s}
                </span>
              </label>
            ))}
          </div>
        </section>

        {/* ── Section: Live Demo ── */}
        <section style={styles.section}>
          <h2 style={styles.sectionTitle}>Live Demo</h2>
          <div style={styles.row}>
            <Field label="Demo URL" style={{ flex: 2 }}>
              <input value={form.demoUrl}
                onChange={e => set('demoUrl', e.target.value)}
                style={styles.input}
                placeholder="e.g. ../parcel_demo/parcel_map.html" />
            </Field>
            <Field label="Button Label" style={{ flex: 1 }}>
              <input value={form.demoLabel}
                onChange={e => set('demoLabel', e.target.value)}
                style={styles.input}
                placeholder="Live Demo (default)" />
            </Field>
          </div>
          <p style={styles.fieldNote}>
            Use a relative path (e.g. <code style={styles.code}>../parcel_demo/parcel_map.html</code>) for demos
            hosted alongside the portfolio, or a full URL for external demos.
            Leave blank to hide the button.
          </p>
        </section>

        {/* ── Section: Image ── */}
        <section style={styles.section}>
          <h2 style={styles.sectionTitle}>Hero Image</h2>
          <div style={styles.imageUploadArea}>
            {form.imageUrl && (
              <div style={styles.imagePreviewWrap}>
                <img src={form.imageUrl} alt="Preview" style={styles.imagePreview} />
                <button type="button" onClick={() => set('imageUrl', '')} style={styles.btnRemoveImg}>
                  Remove
                </button>
              </div>
            )}
            {!form.imageUrl && (
              <div style={styles.uploadZone} onClick={() => fileRef.current?.click()}>
                <input ref={fileRef} type="file" accept="image/*"
                  style={{ display: 'none' }} onChange={handleImageUpload} />
                <div style={styles.uploadIcon}>↑</div>
                <p style={styles.uploadText}>Click to upload project image</p>
                <p style={styles.uploadSub}>JPG, PNG, WEBP — max 10MB</p>
              </div>
            )}
            {upload && (
              <div style={styles.uploadProgress}>
                <div style={styles.uploadBar}>
                  <div style={{ ...styles.uploadFill, width: `${upload.progress}%` }} />
                </div>
                <span style={styles.uploadPct}>{upload.progress}% — {upload.name}</span>
              </div>
            )}
          </div>
        </section>

        {/* ── Submit ── */}
        {error && <p style={styles.error}>{error}</p>}
        <div style={styles.formActions}>
          <button type="button" onClick={() => navigate('/admin')} style={styles.btnCancel}>
            Cancel
          </button>
          <button type="submit" disabled={saving} style={styles.btnSave}>
            {saving ? 'Saving…' : isEdit ? 'Save Changes' : 'Create Project'}
          </button>
        </div>

      </form>
    </main>
  );
}

function Field({ label, children, style }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem', ...style }}>
      <label style={{
        fontSize: '0.62rem', letterSpacing: '0.16em',
        textTransform: 'uppercase', color: 'var(--ochre)',
      }}>{label}</label>
      {children}
    </div>
  );
}

const styles = {
  main:        { padding: '7rem 4rem 5rem', maxWidth: '900px', margin: '0 auto' },
  loadingText: { fontFamily: 'var(--ff-serif)', color: 'var(--slate)', fontSize: '1rem' },
  header: {
    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
    marginBottom: '2.5rem', paddingBottom: '2rem',
    borderBottom: '1px solid var(--rule-light)',
  },
  title: { fontFamily: 'var(--ff-serif)', fontSize: '2rem', fontWeight: 300, color: 'var(--parchment)' },
  btnBack: {
    fontFamily: 'var(--ff-sans)', fontSize: '0.72rem', letterSpacing: '0.12em',
    color: 'var(--slate)', background: 'none', border: 'none', cursor: 'pointer',
  },
  form:    { display: 'flex', flexDirection: 'column', gap: '0' },
  section: { padding: '2rem 0', borderBottom: '1px solid var(--rule-light)' },
  sectionTitle: {
    fontFamily: 'var(--ff-serif)', fontSize: '1.1rem', fontWeight: 400,
    color: 'var(--parchment)', marginBottom: '1.25rem',
  },
  row:     { display: 'flex', gap: '1rem', marginBottom: '1rem', flexWrap: 'wrap' },
  input: {
    background: 'var(--ink-60)', border: '1px solid var(--rule-light)',
    color: 'var(--parchment)', padding: '0.7rem 0.9rem',
    fontSize: '0.9rem', outline: 'none', width: '100%',
  },
  select: { appearance: 'none', cursor: 'pointer' },
  textarea: { resize: 'vertical', lineHeight: 1.6, minHeight: '80px' },
  checkRow: { display: 'flex', alignItems: 'center', gap: '1rem', marginTop: '0.5rem' },
  checkLabel: {
    display: 'flex', alignItems: 'center', gap: '0.6rem',
    fontSize: '0.85rem', color: 'var(--slate-l)', cursor: 'pointer',
  },
  checkbox: { accentColor: 'var(--ochre)', width: '14px', height: '14px' },
  btnAdd: {
    background: 'var(--ink-60)', border: '1px solid var(--rule)',
    color: 'var(--ochre)', padding: '0.7rem 1.25rem',
    fontFamily: 'var(--ff-sans)', fontSize: '0.78rem', cursor: 'pointer',
    whiteSpace: 'nowrap',
  },
  outcomeList: { listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem', marginTop: '0.75rem' },
  outcomeItem: {
    display: 'flex', alignItems: 'center', gap: '0.25rem',
    fontSize: '0.85rem', color: 'var(--slate-l)',
    padding: '0.4rem 0.75rem', background: 'var(--ink-60)',
    border: '1px solid var(--rule-light)',
  },
  btnRemove: {
    marginLeft: 'auto', background: 'none', border: 'none',
    color: 'var(--slate)', fontSize: '1rem', cursor: 'pointer', lineHeight: 1,
  },
  serviceGrid: {
    display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
    gap: '0.6rem',
  },
  serviceLabel: {
    display: 'flex', alignItems: 'center', gap: '0.6rem',
    fontSize: '0.82rem', color: 'var(--slate-l)', cursor: 'pointer',
  },
  serviceActive: { color: 'var(--ochre)' },
  imageUploadArea: { display: 'flex', flexDirection: 'column', gap: '1rem' },
  imagePreviewWrap: { position: 'relative', display: 'inline-block' },
  imagePreview: {
    maxWidth: '400px', maxHeight: '240px', objectFit: 'cover',
    border: '1px solid var(--rule)',
  },
  btnRemoveImg: {
    position: 'absolute', top: '0.5rem', right: '0.5rem',
    background: 'rgba(13,15,12,0.8)', border: '1px solid var(--rule)',
    color: 'var(--slate-l)', padding: '0.3rem 0.75rem',
    fontFamily: 'var(--ff-sans)', fontSize: '0.65rem', cursor: 'pointer',
  },
  uploadZone: {
    border: '1px dashed var(--rule)', padding: '3rem',
    display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem',
    cursor: 'pointer', transition: 'border-color 0.2s',
  },
  uploadIcon: { fontSize: '1.5rem', color: 'var(--ochre)', opacity: 0.6 },
  uploadText: { fontSize: '0.9rem', color: 'var(--slate-l)' },
  uploadSub:  { fontSize: '0.72rem', color: 'var(--slate)' },
  uploadProgress: { display: 'flex', flexDirection: 'column', gap: '0.4rem' },
  uploadBar:  { height: '3px', background: 'var(--ink-60)', borderRadius: '2px' },
  uploadFill: { height: '100%', background: 'var(--ochre)', transition: 'width 0.2s' },
  uploadPct:  { fontSize: '0.72rem', color: 'var(--slate)' },
  fieldNote: { fontSize: '0.72rem', color: 'var(--slate)', marginTop: '0.5rem', lineHeight: 1.6 },
  code: { fontFamily: 'monospace', color: 'var(--ochre)', fontSize: '0.72rem' },
  error: { color: '#e07070', fontSize: '0.82rem', padding: '0.5rem 0' },
  formActions: {
    display: 'flex', gap: '1rem', justifyContent: 'flex-end',
    paddingTop: '2rem',
  },
  btnCancel: {
    fontFamily: 'var(--ff-sans)', fontSize: '0.75rem', letterSpacing: '0.12em',
    textTransform: 'uppercase', color: 'var(--slate)',
    background: 'none', border: '1px solid var(--rule-light)',
    padding: '0.8rem 1.75rem', cursor: 'pointer',
  },
  btnSave: {
    fontFamily: 'var(--ff-sans)', fontSize: '0.75rem', fontWeight: 500,
    letterSpacing: '0.12em', textTransform: 'uppercase',
    background: 'var(--ochre)', color: 'var(--ink)',
    border: 'none', padding: '0.8rem 2rem', cursor: 'pointer',
  },
};
