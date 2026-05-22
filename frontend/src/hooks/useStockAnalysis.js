import { useState } from 'react';

import { useLanguage } from '../i18n/LanguageContext';
import { fetchStockAnalysis, exportStockExcel } from '../services/stockApi';

const toNumberOrNull = (value) => {
  if (value === null || value === undefined || value === '') return null;
  const numberValue = Number(value);
  return Number.isFinite(numberValue) ? numberValue : null;
};

const getStatusFromChange = (priceChange) => {
  if (priceChange === null || priceChange === undefined) return 'unknown';
  if (priceChange > 0) return 'up';
  if (priceChange < 0) return 'down';
  return 'unchanged';
};

const getColorFromStatus = (status) => {
  if (status === 'up') return 'green';
  if (status === 'down') return 'red';
  if (status === 'unchanged') return 'yellow';
  return 'gray';
};

const normalizeStockResponse = (data) => {
  const currentPrice = toNumberOrNull(data.currentPrice ?? data.current_price ?? data.close);
  const previousClose = toNumberOrNull(
    data.previousClose ?? data.previous_close ?? data.referencePrice ?? data.reference_price
  );

  let priceChange = toNumberOrNull(data.priceChange ?? data.price_change ?? data.change);
  if (priceChange === null && currentPrice !== null && previousClose !== null) {
    priceChange = currentPrice - previousClose;
  }

  let percentChange = toNumberOrNull(data.percentChange ?? data.changePercent ?? data.price_change_percent);
  if (percentChange === null && priceChange !== null && previousClose) {
    percentChange = (priceChange / previousClose) * 100;
  }

  const status = data.status || getStatusFromChange(priceChange);
  const color = data.color || getColorFromStatus(status);

  return {
    ...data,
    currentPrice,
    previousClose,
    referencePrice: previousClose,
    priceChange,
    percentChange,
    change: priceChange,
    changePercent: percentChange,
    status,
    color,
  };
};

export function useStockAnalysis() {
  const { t } = useLanguage();

  const [symbol, setSymbol] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [exporting, setExporting] = useState(false);
  const [error, setError] = useState(null);

  const handleSymbolChange = (e) => {
    const cleanValue = e.target.value.replace(/\s+/g, '').toUpperCase();
    setSymbol(cleanValue);
  };

  const getStock = async () => {
    if (!symbol.trim()) {
      setError(t('errors.stockRequired'));
      return;
    }

    setLoading(true);
    setError(null);
    setStockData(null);

    try {
      const res = await fetchStockAnalysis(symbol.trim());
      const normalizedData = normalizeStockResponse(res.data);
      console.log('=== DEBUG DỮ LIỆU NHẬN TỪ BACKEND ===');
      console.log(normalizedData);
      console.log('API response gốc:', res.data);
      console.log('======================================');
      setStockData(normalizedData);
    } catch (err) {
      console.error(err);
      if (err.response && err.response.data && err.response.data.error) {
        setError(err.response.data.error);
      } else {
        setError(t('errors.connectBackend'));
      }
    } finally {
      setLoading(false);
    }
  };

  const exportExcel = async () => {
    if (!symbol.trim()) {
      setError(t('errors.exportStockRequired'));
      return;
    }
    if (!startDate || !endDate) {
      setError(t('errors.exportDateRequired'));
      return;
    }

    setExporting(true);
    setError(null);

    try {
      const response = await exportStockExcel(symbol.trim(), startDate, endDate);

      const blob = new Blob([response.data], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      });
      const downloadUrl = window.URL.createObjectURL(blob);
      const tempLink = document.createElement('a');
      tempLink.href = downloadUrl;
      tempLink.setAttribute('download', `${symbol}_Technical_Report_${startDate}.xlsx`);
      document.body.appendChild(tempLink);
      tempLink.click();
      tempLink.parentNode.removeChild(tempLink);
      window.URL.revokeObjectURL(downloadUrl);
    } catch (err) {
      console.error(err);
      if (err.response && err.response.data) {
        const textBlob = await err.response.data.text();
        try {
          const parsedError = JSON.parse(textBlob);
          setError(parsedError.error || t('errors.exportDefault'));
        } catch {
          setError(t('errors.exportConfig'));
        }
      } else {
        setError(t('errors.exportNetwork'));
      }
    } finally {
      setExporting(false);
    }
  };

  return {
    symbol,
    startDate,
    endDate,
    stockData,
    loading,
    exporting,
    error,
    handleSymbolChange,
    getStock,
    exportExcel,
    setStartDate,
    setEndDate,
  };
}
