import axios from 'axios';

import { API_BASE_URL } from '../config/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  // Render Free may take 50+ seconds to wake the backend after it spins down.
  timeout: 180000,
});

export const fetchStockAnalysis = (symbol) => {
  return apiClient.get(`/stock/${encodeURIComponent(symbol)}`);
};

export const exportStockExcel = (symbol, startDate, endDate) => {
  return apiClient.get(
    `/export/${encodeURIComponent(symbol)}/${encodeURIComponent(startDate)}/${encodeURIComponent(endDate)}`,
    {
      responseType: 'blob',
      // Long exports may fetch up to ten years in bounded date chunks.
      timeout: 240000,
    }
  );
};
