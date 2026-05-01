import React, { createContext, useContext, useState, ReactNode } from 'react';
import { queryService } from '../services/api';

interface QueryContextType {
  query: string;
  report: any | null;
  isLoading: boolean;
  error: string | null;
  currentStep: number;
  submitQuery: (text: string) => Promise<void>;
}

const QueryContext = createContext<QueryContextType | undefined>(undefined);

export const QueryProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [query, setQuery] = useState('');
  const [report, setReport] = useState<any | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentStep, setCurrentStep] = useState(-1);

  const submitQuery = async (text: string) => {
    setQuery(text);
    setIsLoading(true);
    setError(null);
    setReport(null);
    setCurrentStep(0); // Orchestrator

    try {
      // Simulate pipeline steps for UI feedback
      const steps = [0, 1, 2, 3, 4];
      for (const step of steps) {
        setCurrentStep(step);
        await new Promise(r => setTimeout(r, 800)); // Visual delay
      }

      const result = await queryService.submitQuery(text);
      setReport(result);
      setCurrentStep(5); // Complete
    } catch (err: any) {
      setError(err.message || 'Đã xảy ra lỗi không xác định');
      setCurrentStep(-1);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <QueryContext.Provider value={{ query, report, isLoading, error, currentStep, submitQuery }}>
      {children}
    </QueryContext.Provider>
  );
};

export const useQueryContext = () => {
  const context = useContext(QueryContext);
  if (context === undefined) {
    throw new Error('useQueryContext must be used within a QueryProvider');
  }
  return context;
};
