import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { logout } from '../services/auth';

export default function Nav() {
  const { user }   = useAuth();
  const { pathname } = useLocation();
  const isAdmin    = pathname.startsWith('/admin');

  return (
    <nav style={styles.nav}>
      <Link to="/" style={styles.logo}>
        <span style={styles.logoName}>Geoscientific Solutions</span>
        <span style={styles.logoSub}>GIS Consulting · Dallas, Texas</span>
      </Link>

      <div style={styles.links}>
        <Link to="/"         style={styles.link}>Portfolio</Link>
        <a href="../../index.html" style={styles.link}>Main Site</a>
        {user
          ? <>
              <Link to="/admin" style={{ ...styles.link, color: 'var(--ochre)' }}>Admin</Link>
              <button onClick={logout} style={styles.btnLogout}>Sign Out</button>
            </>
          : !isAdmin &&
              <Link to="/admin/login" style={styles.btnCta}>Admin</Link>
        }
      </div>
    </nav>
  );
}

const styles = {
  nav: {
    position: 'fixed', top: 0, left: 0, right: 0,
    zIndex: 100,
    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
    padding: '1.25rem 3rem',
    background: 'rgba(13,15,12,0.88)',
    borderBottom: '1px solid var(--rule-light)',
    backdropFilter: 'blur(12px)',
  },
  logo: {
    display: 'flex', flexDirection: 'column', gap: '0.1rem',
    textDecoration: 'none',
  },
  logoName: {
    fontFamily: 'var(--ff-serif)', fontSize: '1.1rem', fontWeight: 400,
    color: 'var(--parchment)', letterSpacing: '0.04em', lineHeight: 1,
  },
  logoSub: {
    fontFamily: 'var(--ff-sans)', fontSize: '0.58rem', fontWeight: 400,
    color: 'var(--ochre)', letterSpacing: '0.22em', textTransform: 'uppercase',
  },
  links: {
    display: 'flex', alignItems: 'center', gap: '2rem',
  },
  link: {
    fontFamily: 'var(--ff-sans)', fontSize: '0.72rem', fontWeight: 400,
    color: 'var(--slate-l)', letterSpacing: '0.14em', textTransform: 'uppercase',
    transition: 'color 0.2s',
  },
  btnCta: {
    fontFamily: 'var(--ff-sans)', fontSize: '0.7rem', fontWeight: 500,
    color: 'var(--ochre)', letterSpacing: '0.14em', textTransform: 'uppercase',
    padding: '0.5rem 1.25rem',
    border: '1px solid var(--ochre)',
    background: 'transparent',
  },
  btnLogout: {
    fontFamily: 'var(--ff-sans)', fontSize: '0.7rem', fontWeight: 400,
    color: 'var(--slate)', letterSpacing: '0.12em', textTransform: 'uppercase',
    background: 'none', border: 'none', padding: 0,
    cursor: 'pointer',
  },
};
