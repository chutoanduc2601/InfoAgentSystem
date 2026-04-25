import { Routes, Route } from 'react-router-dom';
import { MainLayout } from './components/layout/MainLayout';
import { SearchDashboard } from './components/dashboard/SearchDashboard';
import { ReportView } from './components/report/ReportView';

function App() {
  return (
    <MainLayout>
      <Routes>
        <Route path="/" element={<SearchDashboard />} />
        <Route path="/report" element={<ReportView />} />
      </Routes>
    </MainLayout>
  );
}

export default App;
