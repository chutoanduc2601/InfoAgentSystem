import { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { MainLayout } from './components/layout/MainLayout';
import { SearchDashboard } from './components/dashboard/SearchDashboard';
import { ReportView } from './components/report/ReportView';
import { AuthPage } from './pages/AuthPage';
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
        <Route 
          path="/auth" 
          element={!isAuthenticated ? <AuthPage onAuthSuccess={() => setIsAuthenticated(true)} /> : <Navigate to="/" replace />} 
        />
        <Route 
          path="/" 
          element={isAuthenticated ? <MainLayout><SearchDashboard /></MainLayout> : <Navigate to="/auth" replace />} 
        />
        <Route 
          path="/report" 
          element={isAuthenticated ? <MainLayout><ReportView /></MainLayout> : <Navigate to="/auth" replace />} 
        />
      </Routes>
    </QueryProvider>
  );
}

export default App;
