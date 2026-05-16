import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) return (
    <div style={{ display:'flex', alignItems:'center', justifyContent:'center', height:'100vh' }}>
      <span style={{ fontFamily:'var(--ff-serif)', fontSize:'1.2rem', color:'var(--slate)' }}>
        Loading…
      </span>
    </div>
  );

  return user ? children : <Navigate to="/admin/login" replace />;
}
