/**
 * Service layer for calling the Backend Gateway (Spring Boot)
 */

const API_BASE_URL = 'http://localhost:8080/api';

export const queryService = {
  /**
   * Submits a search query to the backend
   */
  async submitQuery(text: string) {
    const response = await fetch(`${API_BASE_URL}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: text }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `Lỗi hệ thống: ${response.status}`);
    }

    return response.json();
  }
};
