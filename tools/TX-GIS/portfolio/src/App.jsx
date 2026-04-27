import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Nav from './components/Nav';

import Portfolio   from './pages/Portfolio';
import Login       from './pages/admin/Login';
import Dashboard   from './pages/admin/Dashboard';
import ProjectForm from './pages/admin/ProjectForm';

import './styles/globals.css';

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Nav />
        <Routes>
          {/* Public */}
          <Route path="/"     element={<Portfolio />} />

          {/* Admin auth */}
          <Route path="/admin/login" element={<Login />} />

          {/* Protected admin routes */}
          <Route path="/admin" element={
            <ProtectedRoute><Dashboard /></ProtectedRoute>
          } />
          <Route path="/admin/projects/new" element={
            <ProtectedRoute><ProjectForm /></ProtectedRoute>
          } />
          <Route path="/admin/projects/:id/edit" element={
            <ProtectedRoute><ProjectForm /></ProtectedRoute>
          } />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
