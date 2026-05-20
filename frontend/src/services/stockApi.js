import axios from 'axios';

import { API_BASE_URL } from '../config/api';

export const fetchStockAnalysis = (symbol) => {
  return axios.get(`${API_BASE_URL}/stock/${symbol}`);
};

export const exportStockExcel = (symbol, startDate, endDate) => {
  return axios.get(
    `${API_BASE_URL}/export/${symbol}/${startDate}/${endDate}`,
    { responseType: 'blob' }
  );
};
