import { useState } from 'react';

import { useLanguage } from '../i18n/LanguageContext';
import { exportStockExcel, fetchStockAnalysis } from '../services/stockApi';

const SYMBOL_PATTERN = /^[A-Z0-9]{1,10}$/;
const MAX_EXPORT_DAYS = 365 * 10;

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

const normalizeSymbol = (value) => value.replace(/\s+/g, '').toUpperCase();

const getTodayDateString = () => {
  const now = new Date();
  const timezoneOffset = now.getTimezoneOffset() * 60000;
  return new Date(now.getTime() - timezoneOffset).toISOString().slice(0, 10);
};

const isFutureDate = (dateString) => dateString > getTodayDateString();

const getDateDiffDays = (startDate, endDate) => {
  const start = new Date(`${startDate}T00:00:00`);
  const end = new Date(`${endDate}T00:00:00`);
  return Math.round((end - start) / (1000 * 60 * 60 * 24));
};

const validateSymbol = (value) => {
  const symbol = normalizeSymbol(value);
  if (!symbol) {
    return { symbol: '', error: 'Mã cổ phiếu không được để trống.' };
  }
  if (!SYMBOL_PATTERN.test(symbol)) {
    return { symbol, error: 'Mã cổ phiếu không hợp lệ. Chỉ nhập chữ cái/số, tối đa 10 ký tự.' };
  }
  return { symbol, error: null };
};

const validateExportDates = (startDate, endDate) => {
  if (!startDate || !endDate) {
    return 'Vui lòng chọn ngày bắt đầu và ngày kết thúc trước khi xuất Excel.';
  }
  if (startDate > endDate) {
    return 'Ngày bắt đầu không được lớn hơn ngày kết thúc.';
  }
  if (isFutureDate(startDate) || isFutureDate(endDate)) {
    return 'Không thể xuất dữ liệu cho ngày tương lai.';
  }
  if (getDateDiffDays(startDate, endDate) > MAX_EXPORT_DAYS) {
    return 'Khoảng ngày xuất Excel quá dài. Vui lòng chọn tối đa 10 năm.';
  }
  return null;
};

const extractErrorMessage = async (err, fallbackMessage) => {
  const responseData = err?.response?.data;

  if (!responseData) {
    return fallbackMessage;
  }

  if (responseData.error) {
    return responseData.error;
  }

  if (responseData instanceof Blob) {
    try {
      const textBlob = await responseData.text();
      const parsedError = JSON.parse(textBlob);
      return parsedError.error || fallbackMessage;
    } catch {
      return fallbackMessage;
    }
  }

  return fallbackMessage;
};

const normalizeStockResponse = (data) => {
  const currentPrice = toNumberOrNull(data?.currentPrice ?? data?.current_price ?? data?.close);
  const previousClose = toNumberOrNull(
    data?.previousClose ?? data?.previous_close ?? data?.referencePrice ?? data?.reference_price
  );

  let priceChange = toNumberOrNull(data?.priceChange ?? data?.price_change ?? data?.change);
  if (priceChange === null && currentPrice !== null && previousClose !== null) {
    priceChange = currentPrice - previousClose;
  }

  let percentChange = toNumberOrNull(data?.percentChange ?? data?.changePercent ?? data?.price_change_percent);
  if (percentChange === null && priceChange !== null && previousClose) {
    percentChange = (priceChange / previousClose) * 100;
  }

  const status = data?.status || getStatusFromChange(priceChange);
  const color = data?.color || getColorFromStatus(status);
  const chartData = Array.isArray(data?.data) ? data.data : [];

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
    data: chartData,
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
    setSymbol(normalizeSymbol(e.target.value));
  };

  const getStock = async () => {
    if (loading) return;

    const { symbol: cleanSymbol, error: symbolError } = validateSymbol(symbol);
    if (symbolError) {
      setError(symbolError || t('errors.stockRequired'));
      return;
    }

    setLoading(true);
    setError(null);
    setStockData(null);

    try {
      const res = await fetchStockAnalysis(cleanSymbol);
      const normalizedData = normalizeStockResponse(res.data || {});
      setStockData(normalizedData);
      setSymbol(cleanSymbol);
    } catch (err) {
      const message = await extractErrorMessage(err, t('errors.connectBackend'));
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const exportExcel = async () => {
    if (exporting) return;

    const { symbol: cleanSymbol, error: symbolError } = validateSymbol(symbol);
    if (symbolError) {
      setError(symbolError || t('errors.exportStockRequired'));
      return;
    }

    const dateError = validateExportDates(startDate, endDate);
    if (dateError) {
      setError(dateError || t('errors.exportDateRequired'));
      return;
    }

    setExporting(true);
    setError(null);

    try {
      const response = await exportStockExcel(cleanSymbol, startDate, endDate);

      const blob = new Blob([response.data], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      });
      const downloadUrl = window.URL.createObjectURL(blob);
      const tempLink = document.createElement('a');
      tempLink.href = downloadUrl;
      tempLink.setAttribute('download', `${cleanSymbol}_VSDAT_${startDate}_${endDate}.xlsx`);
      document.body.appendChild(tempLink);
      tempLink.click();
      tempLink.remove();
      window.URL.revokeObjectURL(downloadUrl);
      setSymbol(cleanSymbol);
    } catch (err) {
      const message = await extractErrorMessage(err, t('errors.exportDefault'));
      setError(message);
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
    todayDate: getTodayDateString(),
    handleSymbolChange,
    getStock,
    exportExcel,
    setStartDate,
    setEndDate,
  };
}
