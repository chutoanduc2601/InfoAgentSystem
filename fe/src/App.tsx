import { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { MainLayout } from './components/layout/MainLayout';
import { SearchDashboard } from './components/dashboard/SearchDashboard';
import { ReportView } from './components/report/ReportView';
import { AuthPage } from './pages/AuthPage';
import { ResetPasswordForm } from './components/auth/ResetPasswordForm';
import { supabase } from './lib/supabase';
import { QueryProvider } from './context/QueryContext';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isInitializing, setIsInitializing] = useState(true);

  useEffect(() => {
    // Check active sessions and sets the user
    supabase.auth.getSession().then(({ data: { session } }) => {
      setIsAuthenticated(!!session);
      setIsInitializing(false);
    }).catch(() => {
      // Even if session check fails (e.g. invalid config), stop initializing
      setIsInitializing(false);
    });

    // Listen for changes on auth state (logged in, signed out, etc.)
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setIsAuthenticated(!!session);
    });

    return () => subscription.unsubscribe();
  }, []);

  if (isInitializing) {
    return <div className="min-h-screen flex items-center justify-center bg-gray-50">Đang tải...</div>;
  }

  return (
    <QueryProvider>
      <Routes>
        {/* Auth page — nếu đã login thì redirect về trang chính */}
        <Route 
          path="/auth" 
          element={!isAuthenticated ? <AuthPage onAuthSuccess={() => setIsAuthenticated(true)} /> : <Navigate to="/" replace />} 
        />

        {/* Reset password — luôn accessible (Supabase set session tạm từ token) */}
        <Route
          path="/auth/reset-password"
          element={<ResetPasswordForm />}
        />

        {/* Trang chính — cho phép cả khách lẫn user đã đăng nhập */}
        <Route 
          path="/" 
          element={<MainLayout><SearchDashboard /></MainLayout>} 
        />
        <Route 
          path="/report" 
          element={<MainLayout><ReportView /></MainLayout>} 
        />
      </Routes>
    </QueryProvider>
  );
}

export default App;
