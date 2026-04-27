import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../../services/auth';

export default function Login() {
  const navigate = useNavigate();
  const [email,    setEmail]    = useState('');
  const [password, setPassword] = useState('');
  const [error,    setError]    = useState('');
  const [loading,  setLoading]  = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(''); setLoading(true);
    try {
      await login(email, password);
      navigate('/admin');
    } catch (err) {
      setError('Invalid email or password.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={styles.main}>
      <div style={styles.card}>
        <div style={styles.logo}>
          <span style={styles.logoName}>Geoscientific Solutions</span>
          <span style={styles.logoSub}>Admin Access</span>
        </div>

        <h1 style={styles.title}>Sign In</h1>

        <form onSubmit={handleSubmit} style={styles.form}>
          <label style={styles.label}>Email</label>
          <input
            type="email" required autoComplete="email"
            value={email} onChange={e => setEmail(e.target.value)}
            style={styles.input}
            placeholder="admin@geoscientificsolutions.com"
          />

          <label style={styles.label}>Password</label>
          <input
            type="password" required autoComplete="current-password"
            value={password} onChange={e => setPassword(e.target.value)}
            style={styles.input}
          />

          {error && <p style={styles.error}>{error}</p>}

          <button type="submit" disabled={loading} style={styles.btn}>
            {loading ? 'Signing in…' : 'Sign In →'}
          </button>
        </form>
      </div>
    </main>
  );
}

const styles = {
  main: {
    minHeight: '100vh', display: 'flex',
    alignItems: 'center', justifyContent: 'center',
    padding: '2rem',
  },
  card: {
    width: '100%', maxWidth: '400px',
    background: 'var(--ink-80)',
    border: '1px solid var(--rule)',
    padding: '2.5rem',
  },
  logo: {
    display: 'flex', flexDirection: 'column', gap: '0.15rem',
    marginBottom: '2rem',
  },
  logoName: {
    fontFamily: 'var(--ff-serif)', fontSize: '1.1rem', fontWeight: 400,
    color: 'var(--parchment)',
  },
  logoSub: {
    fontSize: '0.6rem', letterSpacing: '0.2em', textTransform: 'uppercase',
    color: 'var(--ochre)',
  },
  title: {
    fontFamily: 'var(--ff-serif)', fontSize: '1.8rem', fontWeight: 300,
    color: 'var(--parchment)', marginBottom: '1.75rem',
  },
  form: { display: 'flex', flexDirection: 'column', gap: '0.5rem' },
  label: {
    fontSize: '0.65rem', letterSpacing: '0.16em', textTransform: 'uppercase',
    color: 'var(--ochre)', marginTop: '0.75rem',
  },
  input: {
    background: 'var(--ink-60)', border: '1px solid var(--rule-light)',
    color: 'var(--parchment)', padding: '0.75rem 1rem',
    fontSize: '0.9rem', outline: 'none', width: '100%',
  },
  error: {
    fontSize: '0.8rem', color: '#e07070', marginTop: '0.5rem',
  },
  btn: {
    marginTop: '1.5rem',
    background: 'var(--ochre)', color: 'var(--ink)',
    border: 'none', padding: '0.9rem',
    fontFamily: 'var(--ff-sans)', fontSize: '0.78rem',
    fontWeight: 500, letterSpacing: '0.14em', textTransform: 'uppercase',
    cursor: 'pointer', transition: 'background 0.2s',
  },
};
