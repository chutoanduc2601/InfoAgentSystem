/**
 * Service layer for calling the Backend Gateway (Spring Boot)
 */

const API_BASE_URL = 'http://localhost:8080/api';

// ─────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────

export interface HistoryItem {
  queryId:   string;
  queryText: string;
  status:    'processing' | 'done' | 'error';
  createdAt: string;
  report:    ReportData | null;
}

export interface ForecastData {
  actual_values:    number[];
  actual_labels:    string[];
  forecast_values:  number[];
  forecast_labels:  string[];
  unit:             string;
  title:            string;
}

export interface ReportData {
  confidence_label: string;
  quick_summary:    string[];
  detailed_report:  string;
  sources:          { url: string; confidence: number }[];
  recommendations:  string[];
  intent?:          string;
  intent_confidence?: number;
  forecast?:        ForecastData | null;
}

// ─────────────────────────────────────────────────────
// Query Service
// ─────────────────────────────────────────────────────

export const queryService = {
  /**
   * Submits a search query to the backend.
   * Returns { success, queryId, data } where data is the AI report.
   */
  async submitQuery(text: string, userId?: string) {
    const response = await fetch(`${API_BASE_URL}/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: text, userId: userId ?? null }),
    });

    const data = await response.json().catch(() => ({}));
    return data as { success: boolean; queryId?: string; data?: ReportData; error?: string };
  },
};

// ─────────────────────────────────────────────────────
// History Service
// ─────────────────────────────────────────────────────

export const historyService = {
  /**
   * Lấy toàn bộ lịch sử tra cứu của một user từ DB.
   */
  async getHistory(userId: string): Promise<HistoryItem[]> {
    const response = await fetch(`${API_BASE_URL}/history/${encodeURIComponent(userId)}`);
    const data = await response.json().catch(() => ({ success: false, data: [] }));
    return data.data as HistoryItem[];
  },

  async deleteHistory(queryId: string): Promise<boolean> {
    const response = await fetch(`${API_BASE_URL}/history/${queryId}`, {
      method: 'DELETE',
    });
    const data = await response.json().catch(() => ({ success: false }));
    return data.success;
  },

  async renameHistory(queryId: string, title: string): Promise<boolean> {
    const response = await fetch(`${API_BASE_URL}/history/${queryId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title }),
    });
    const data = await response.json().catch(() => ({ success: false }));
    return data.success;
  }
};
