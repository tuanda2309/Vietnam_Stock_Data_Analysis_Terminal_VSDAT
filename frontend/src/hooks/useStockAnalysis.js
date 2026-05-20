import { useState } from 'react';

import { fetchStockAnalysis, exportStockExcel } from '../services/stockApi';

export function useStockAnalysis() {
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
      setError('Vui lòng điền mã cổ phiếu trước khi phân tích!');
      return;
    }

    setLoading(true);
    setError(null);
    setStockData(null);

    try {
      const res = await fetchStockAnalysis(symbol.trim());
      console.log('=== DEBUG DỮ LIỆU NHẬN TỪ BACKEND ===');
      console.log(res.data);
      console.log('======================================');
      setStockData(res.data);
    } catch (err) {
      console.error(err);
      if (err.response && err.response.data && err.response.data.error) {
        setError(err.response.data.error);
      } else {
        setError('Không thể kết nối đến máy chủ API Backend. Vui lòng kiểm tra lại!');
      }
    } finally {
      setLoading(false);
    }
  };

  const exportExcel = async () => {
    if (!symbol.trim()) {
      setError('Vui lòng điền mã cổ phiếu ở Card truy vấn trước khi xuất dữ liệu!');
      return;
    }
    if (!startDate || !endDate) {
      setError('Vui lòng chọn đầy đủ cả Ngày bắt đầu và Ngày kết thúc để xuất file Excel!');
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
          setError(parsedError.error || 'Lỗi trích xuất tệp báo cáo từ hệ thống.');
        } catch {
          setError('Hệ thống gặp lỗi trong quá trình cấu hình biên soạn tệp Excel.');
        }
      } else {
        setError('Kết nối mạng gián đoạn. Không thể gửi yêu cầu xuất file báo cáo!');
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
