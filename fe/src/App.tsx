import { useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { MainLayout } from './components/layout/MainLayout';
import { SearchDashboard } from './components/dashboard/SearchDashboard';
import { ReportView } from './components/report/ReportView';
import { AuthPage } from './pages/AuthPage';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
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
  );
}

export default App;
