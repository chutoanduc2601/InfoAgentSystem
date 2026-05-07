import React, { createContext, useContext, useState, type ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { queryService, type HistoryItem, type ReportData } from '../services/api';
import { supabase } from '../lib/supabase';

// ─────────────────────────────────────────────────────
// Context shape
// ─────────────────────────────────────────────────────

interface QueryContextType {
  query:             string;
  report:            ReportData | null;
  isLoading:         boolean;
  error:             string | null;
  currentStep:       number;
  currentQueryId:    string | null;
  queryTimestamp:    string | null;
  /** Key tăng mỗi khi có query mới → Sidebar lắng nghe để tự refresh */
  sidebarRefreshKey: number;
  submitQuery:       (text: string) => Promise<void>;
  /** Load một báo cáo cũ từ lịch sử (không gọi lại AI) */
  loadFromHistory:   (item: HistoryItem) => void;
}

const QueryContext = createContext<QueryContextType | undefined>(undefined);

// ─────────────────────────────────────────────────────
// Provider Component
// ─────────────────────────────────────────────────────

export const QueryProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [query,             setQuery]             = useState('');
  const [report,            setReport]            = useState<ReportData | null>(null);
  const [isLoading,         setIsLoading]         = useState(false);
  const [error,             setError]             = useState<string | null>(null);
  const [currentStep,       setCurrentStep]       = useState(-1);
  const [currentQueryId,    setCurrentQueryId]    = useState<string | null>(null);
  const [queryTimestamp,    setQueryTimestamp]    = useState<string | null>(null);
  const [sidebarRefreshKey, setSidebarRefreshKey] = useState(0);

  const navigate = useNavigate();

  // ───── Lấy userId từ Supabase session ─────
  const getCurrentUserId = async (): Promise<string | undefined> => {
    const { data: { user } } = await supabase.auth.getUser();
    return user?.id;
  };

  // ───── Submit query mới → gọi AI → lưu DB ─────
  const submitQuery = async (text: string) => {
    setQuery(text);
    setIsLoading(true);
    setError(null);
    setReport(null);
    setCurrentQueryId(null);
    setQueryTimestamp(null);
    setCurrentStep(0);

    try {
      const userId = await getCurrentUserId();

      // Visual pipeline animation
      const steps = [0, 1, 2, 3];
      for (const step of steps) {
        setCurrentStep(step);
        await new Promise(r => setTimeout(r, 700));
      }

      const result = await queryService.submitQuery(text, userId);

      if (!result.success || !result.data) {
        throw new Error(result.error || 'Lỗi không xác định từ AI Service');
      }

      const now = new Date().toISOString();
      setReport(result.data);
      setCurrentQueryId(result.queryId ?? null);
      setQueryTimestamp(now);
      setCurrentStep(4); // Complete

      // Báo Sidebar refresh để hiển thị item mới
      setSidebarRefreshKey(prev => prev + 1);

      navigate('/report');
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Đã xảy ra lỗi không xác định';
      setError(message);
      setCurrentStep(-1);
    } finally {
      setIsLoading(false);
    }
  };

  // ───── Tải báo cáo cũ từ lịch sử (KHÔNG gọi AI) ─────
  const loadFromHistory = (item: HistoryItem) => {
    if (!item.report) return;
    setQuery(item.queryText);
    setReport(item.report);
    setCurrentQueryId(item.queryId);
    setQueryTimestamp(item.createdAt);
    setError(null);
    setCurrentStep(4);
    navigate('/report');
  };

  return (
    <QueryContext.Provider value={{
      query, report, isLoading, error, currentStep,
      currentQueryId, queryTimestamp, sidebarRefreshKey,
      submitQuery, loadFromHistory,
    }}>
      {children}
    </QueryContext.Provider>
  );
};

// ─────────────────────────────────────────────────────
// Hook
// ─────────────────────────────────────────────────────

export const useQueryContext = () => {
  const context = useContext(QueryContext);
  if (context === undefined) {
    throw new Error('useQueryContext must be used within a QueryProvider');
  }
  return context;
};
