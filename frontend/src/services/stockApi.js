import axios from 'axios';

import { API_BASE_URL } from '../config/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

export const fetchStockAnalysis = (symbol) => {
  return apiClient.get(`/stock/${encodeURIComponent(symbol)}`);
};

export const exportStockExcel = (symbol, startDate, endDate) => {
  return apiClient.get(
    `/export/${encodeURIComponent(symbol)}/${encodeURIComponent(startDate)}/${encodeURIComponent(endDate)}`,
    {
      responseType: 'blob',
      timeout: 60000,
    }
  );
};
