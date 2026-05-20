import { useState } from 'react';
import axios from 'axios';
import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  ReferenceLine,
} from 'recharts';
import {
  Loader2,
  Download,
  TrendingUp,
  TrendingDown,
  Minus,
  Activity,
  BarChart3,
  AlertTriangle,
  FileSpreadsheet,
  LineChart as ChartIcon,
  CheckCircle2,
  Target,
  ShieldCheck,
  Landmark,
  WalletCards,
  ListChecks,
  Gauge,
} from 'lucide-react';

const API_BASE_URL = import.meta.env?.VITE_API_URL || 'http://127.0.0.1:5000';

const ACTION_STYLES = {
  BUY: {
    text: 'text-emerald-300',
    bg: 'bg-emerald-500/10',
    border: 'border-emerald-500/40',
    badge: 'bg-emerald-500 text-slate-950',
  },
  WATCH: {
    text: 'text-amber-300',
    bg: 'bg-amber-500/10',
    border: 'border-amber-500/40',
    badge: 'bg-amber-400 text-slate-950',
  },
  HOLD: {
    text: 'text-blue-300',
    bg: 'bg-blue-500/10',
    border: 'border-blue-500/40',
    badge: 'bg-blue-500 text-white',
  },
  SELL: {
    text: 'text-orange-300',
    bg: 'bg-orange-500/10',
    border: 'border-orange-500/40',
    badge: 'bg-orange-500 text-white',
  },
  CUT_LOSS: {
    text: 'text-red-300',
    bg: 'bg-red-500/10',
    border: 'border-red-500/40',
    badge: 'bg-red-600 text-white',
  },
  DEFAULT: {
    text: 'text-slate-300',
    bg: 'bg-slate-500/10',
    border: 'border-slate-700',
    badge: 'bg-slate-600 text-white',
  },
};

function App() {
  const [symbol, setSymbol] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [exporting, setExporting] = useState(false);
  const [error, setError] = useState(null);

  const technical = stockData?.technical || {};
  const levels = stockData?.levels || {};
  const riskManagement = stockData?.riskManagement || {};
  const market = stockData?.market || {};
  const signal = stockData?.signal || {};
  const suggestedOrder = stockData?.suggestedOrder || {};
  const reasons = Array.isArray(stockData?.reasons) ? stockData.reasons : [];
  const warnings = Array.isArray(stockData?.warnings) ? stockData.warnings : [];

  const formatCurrency = (value) => {
    if (value === null || value === undefined || Number.isNaN(Number(value))) return '--';
    return Number(value).toLocaleString('vi-VN', { style: 'currency', currency: 'VND' });
  };

  const formatNumber = (value) => {
    if (value === null || value === undefined || Number.isNaN(Number(value))) return '--';
    return Number(value).toLocaleString('vi-VN');
  };

  const formatIndicator = (value, digits = 2) => {
    if (value === null || value === undefined || Number.isNaN(Number(value))) return '--';
    return Number(value).toLocaleString('vi-VN', {
      minimumFractionDigits: 0,
      maximumFractionDigits: digits,
    });
  };

  const formatPercent = (value) => {
    if (value === null || value === undefined || Number.isNaN(Number(value))) return '--';
    const num = Number(value);
    const sign = num > 0 ? '+' : '';
    return `${sign}${num.toFixed(2)}%`;
  };

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
      const res = await axios.get(`${API_BASE_URL}/stock/${symbol.trim()}`);
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
      const response = await axios.get(
        `${API_BASE_URL}/export/${symbol.trim()}/${startDate}/${endDate}`,
        { responseType: 'blob' }
      );

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

  const statusColorClass = stockData?.status === 'up'
    ? 'text-emerald-400'
    : stockData?.status === 'down'
      ? 'text-rose-400'
      : 'text-amber-400';

  const actionStyle = ACTION_STYLES[signal?.action] || ACTION_STYLES.DEFAULT;
  const entryZone = riskManagement?.entryZone || {};
  const takeProfitZone = riskManagement?.takeProfitZone || {};
  const riskRewardRatio = riskManagement?.riskRewardRatio;
  const riskRewardWeak = riskRewardRatio !== null && riskRewardRatio !== undefined && Number(riskRewardRatio) < 1.5;

  return (
    <div className='min-h-screen bg-[#0A0F24] text-slate-100 p-4 md:p-10 font-sans antialiased'>
      <div className='max-w-7xl mx-auto'>
        <header className='mb-10 border-b border-slate-800 pb-8 flex flex-col items-center text-center'>
          <div className='relative mb-5 group'>
            <div className='absolute -inset-1 bg-gradient-to-r from-emerald-500 to-blue-500 rounded-full blur opacity-40 group-hover:opacity-70 transition duration-500'></div>
            <img
              src='/cat-logo.png'
              alt='Cat Intelligence Logo'
              className='relative w-24 h-24 md:w-28 md:h-28 rounded-full object-cover border-2 border-slate-700 bg-[#131A35] p-1 shadow-2xl'
            />
          </div>

          <h1 className='text-3xl md:text-4xl lg:text-5xl font-extrabold tracking-tight bg-gradient-to-r from-emerald-400 to-blue-500 bg-clip-text text-transparent px-4 max-w-3xl'>
            Vietnam Stock Data Analysis Terminal (VSDAT)
          </h1>
          <p className='text-slate-400 text-sm md:text-base mt-3 max-w-xl font-medium px-4 leading-relaxed'>
            Hệ thống phân tích kỹ thuật nâng cao và định lượng chuỗi thời gian thị trường chứng khoán Việt Nam
          </p>
        </header>

        <div className='grid grid-cols-1 lg:grid-cols-12 gap-6 mb-6 items-stretch'>
          <div className='lg:col-span-5 bg-[#131A35] p-5 md:p-6 rounded-xl shadow-xl border border-slate-800 flex flex-col justify-center hover:border-emerald-500/30 transition-all duration-300'>
            <div className='space-y-4 w-full'>
              <div className='flex items-center gap-2 border-b border-slate-800 pb-2.5'>
                <ChartIcon className='h-4 w-4 text-emerald-400' />
                <label className='block text-xs font-bold uppercase text-emerald-400 tracking-wider'>
                  Truy vấn phân tích kỹ thuật
                </label>
              </div>

              <div className='grid grid-cols-1 sm:grid-cols-3 gap-3 items-center'>
                <div className='relative sm:col-span-2'>
                  <input
                    type='text'
                    placeholder='NHẬP MÃ CỔ PHIẾU'
                    value={symbol}
                    onChange={handleSymbolChange}
                    onKeyDown={(e) => e.key === 'Enter' && !loading && getStock()}
                    className='p-3 rounded-lg text-white bg-[#1E264A] border border-slate-700 w-full focus:outline-none focus:ring-2 focus:ring-emerald-500 font-bold placeholder-slate-500 uppercase tracking-widest text-base transition-all'
                  />
                </div>

                <button
                  onClick={getStock}
                  disabled={loading}
                  className='bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-800 disabled:text-slate-500 p-3 rounded-lg text-white font-semibold transition-all flex items-center gap-2 shadow-md w-full justify-center active:scale-95 text-sm h-full whitespace-nowrap'
                >
                  {loading ? <Loader2 className='h-4 w-4 animate-spin' /> : <Activity className='h-4 w-4' />}
                  Phân tích
                </button>
              </div>
            </div>
          </div>

          <div className='lg:col-span-7 bg-[#131A35] p-5 md:p-6 rounded-xl shadow-xl border border-slate-800 flex flex-col justify-center hover:border-amber-500/30 transition-all duration-300'>
            <div className='space-y-4 w-full'>
              <div className='flex items-center gap-2 border-b border-slate-800 pb-2.5'>
                <FileSpreadsheet className='h-4 w-4 text-amber-400' />
                <label className='block text-xs font-bold uppercase text-amber-400 tracking-wider'>
                  Xuất dữ liệu lịch sử (Excel)
                </label>
              </div>

              <div className='grid grid-cols-1 sm:grid-cols-3 gap-3'>
                <div className='relative'>
                  <span className='absolute -top-2 left-2 px-1 text-[10px] text-slate-400 bg-[#131A35] font-medium z-10'>Từ ngày</span>
                  <input
                    type='date'
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                    className='p-3 pt-3.5 rounded-lg text-white bg-[#1E264A] border border-slate-700 w-full focus:outline-none focus:ring-2 focus:ring-amber-500 transition-all text-sm font-medium'
                  />
                </div>

                <div className='relative'>
                  <span className='absolute -top-2 left-2 px-1 text-[10px] text-slate-400 bg-[#131A35] font-medium z-10'>Đến ngày</span>
                  <input
                    type='date'
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    className='p-3 pt-3.5 rounded-lg text-white bg-[#1E264A] border border-slate-700 w-full focus:outline-none focus:ring-2 focus:ring-amber-500 transition-all text-sm font-medium'
                  />
                </div>

                <button
                  onClick={exportExcel}
                  disabled={exporting}
                  className='bg-amber-600 hover:bg-amber-500 disabled:bg-slate-800 disabled:text-slate-500 p-3 rounded-lg text-slate-950 font-bold transition-all flex items-center gap-2 shadow-md w-full justify-center whitespace-nowrap active:scale-95 text-sm h-full'
                >
                  {exporting ? <Loader2 className='h-4 w-4 animate-spin text-slate-950' /> : <Download className='h-4 w-4 text-slate-950' />}
                  Xuất tệp Excel
                </button>
              </div>
            </div>
          </div>
        </div>

        <div className='mb-6 bg-amber-500/10 border border-amber-500/30 rounded-xl p-4 flex items-start gap-3 text-sm text-amber-100'>
          <AlertTriangle className='h-5 w-5 text-amber-300 shrink-0 mt-0.5' />
          <p>
            <span className='font-bold'>Cảnh báo rủi ro:</span> Thông tin chỉ mang tính tham khảo, không phải khuyến nghị đầu tư. Người dùng cần tự chịu trách nhiệm với quyết định giao dịch.
          </p>
        </div>

        {error && (
          <div className='bg-red-950/40 border border-red-900 text-red-200 p-4 rounded-lg mb-6 text-sm font-medium flex items-center gap-3 animate-fadeIn'>
            <AlertTriangle className='h-5 w-5 text-red-400 shrink-0' />
            <span>{error}</span>
          </div>
        )}

        {loading && (
          <div className='flex flex-col items-center justify-center p-20 bg-[#131A35] rounded-xl border border-slate-800 shadow-xl'>
            <Loader2 className='h-12 w-12 text-emerald-500 animate-spin mb-4' />
            <p className='text-slate-400 font-medium'>Hệ thống đang tải dữ liệu và tính toán định lượng chỉ báo...</p>
          </div>
        )}

        {stockData && !loading && (
          <div className='space-y-6 animate-fadeIn'>
            <div className='grid grid-cols-1 md:grid-cols-3 gap-5'>
              <div className='bg-[#131A35] p-5 rounded-xl border border-slate-800 shadow-lg flex items-center justify-between'>
                <div>
                  <h2 className='text-sm font-semibold text-slate-400 uppercase tracking-wider'>Giá Hiện Tại ({stockData.symbol})</h2>
                  <p className={`text-3xl font-extrabold mt-2 tracking-tight ${statusColorClass}`}>
                    {formatCurrency(stockData.currentPrice)}
                  </p>
                  <div className={`flex items-center gap-1.5 text-xs font-bold mt-1.5 ${statusColorClass}`}>
                    <span>{stockData.priceChange > 0 ? '+' : ''}{formatNumber(stockData.priceChange)}đ</span>
                    <span>({formatPercent(stockData.percentChange)})</span>
                  </div>
                </div>
                <div className={`p-3 rounded-lg ${stockData.status === 'up' ? 'bg-emerald-500/10 text-emerald-400' : stockData.status === 'down' ? 'bg-rose-500/10 text-rose-400' : 'bg-amber-500/10 text-amber-400'}`}>
                  {stockData.status === 'up' ? <TrendingUp className='h-6 w-6' /> : stockData.status === 'down' ? <TrendingDown className='h-6 w-6' /> : <Minus className='h-6 w-6' />}
                </div>
              </div>

              <div className='bg-[#131A35] p-5 rounded-xl border border-slate-800 shadow-lg flex items-center justify-between'>
                <div>
                  <h2 className='text-sm font-semibold text-slate-400 uppercase tracking-wider'>Chỉ số RSI (14 Phiên)</h2>
                  <p className={`text-3xl font-extrabold mt-2 ${technical.rsi14 >= 70 ? 'text-red-400' : technical.rsi14 <= 30 ? 'text-blue-400' : 'text-slate-200'}`}>
                    {formatIndicator(technical.rsi14 ?? stockData.rsi)}
                  </p>
                  <span className='text-xs font-bold mt-1 block text-slate-500'>
                    {technical.rsi14 >= 70 ? '⚠️ Quá mua' : technical.rsi14 <= 30 ? '📉 Quá bán' : '⚖️ Trung tính'}
                  </span>
                </div>
                <div className='bg-slate-700/20 p-3 rounded-lg text-slate-300'><Activity className='h-6 w-6' /></div>
              </div>

              <div className='bg-[#131A35] p-5 rounded-xl border border-slate-800 shadow-lg flex items-center justify-between'>
                <div>
                  <h2 className='text-sm font-semibold text-slate-400 uppercase tracking-wider'>Giá Trị Trung Bình MA20</h2>
                  <p className='text-3xl font-extrabold mt-2 text-blue-400'>{formatCurrency(technical.ma20 ?? stockData.ma20)}</p>
                </div>
                <div className='bg-blue-500/10 p-3 rounded-lg text-blue-400'><BarChart3 className='h-6 w-6' /></div>
              </div>
            </div>

            <div className={`rounded-2xl border ${actionStyle.border} ${actionStyle.bg} p-5 md:p-6 shadow-xl`}>
              <div className='flex flex-col lg:flex-row lg:items-center lg:justify-between gap-5'>
                <div className='space-y-3'>
                  <div className='flex items-center gap-3 flex-wrap'>
                    <span className={`px-4 py-2 rounded-full text-sm font-black tracking-widest ${actionStyle.badge}`}>
                      {signal.action || 'CHƯA CÓ TÍN HIỆU'}
                    </span>
                    <span className='text-slate-400 text-sm font-medium'>Độ tin cậy</span>
                    <span className={`text-2xl font-extrabold ${actionStyle.text}`}>{signal.confidence ?? '--'}%</span>
                  </div>
                  <h2 className='text-2xl md:text-3xl font-extrabold text-slate-100'>
                    {signal.title || 'Chưa có tín hiệu'}
                  </h2>
                  <p className='text-slate-300 max-w-3xl leading-relaxed'>
                    {signal.summary || 'Backend chưa trả về tín hiệu phân tích cho mã này.'}
                  </p>
                </div>
                <div className='bg-[#0A0F24]/60 border border-slate-800 rounded-xl p-4 min-w-[220px]'>
                  <div className='flex items-center gap-2 text-slate-400 text-xs uppercase font-bold tracking-wider mb-2'>
                    <Gauge className='h-4 w-4' />
                    Tóm tắt nhanh
                  </div>
                  <p className='text-sm text-slate-300'>Không có tín hiệu nào đảm bảo thắng. Luôn đặt điểm cắt lỗ trước khi vào lệnh.</p>
                </div>
              </div>
            </div>

            <div className='grid grid-cols-1 lg:grid-cols-3 gap-5'>
              <SectionCard title='Vùng giá & quản trị rủi ro' icon={<ShieldCheck className='h-4 w-4 text-emerald-400' />}>
                <InfoRow label='Vùng mua đẹp' value={`${formatCurrency(entryZone.from)} - ${formatCurrency(entryZone.to)}`} />
                <InfoRow label='Cắt lỗ' value={formatCurrency(riskManagement.stopLoss)} valueClass='text-rose-300' />
                <InfoRow label='Chốt lời' value={`${formatCurrency(takeProfitZone.from)} - ${formatCurrency(takeProfitZone.to)}`} valueClass='text-emerald-300' />
                <InfoRow label='Risk/Reward' value={riskRewardRatio ?? '--'} valueClass={riskRewardWeak ? 'text-amber-300' : 'text-emerald-300'} />
                {riskRewardWeak && (
                  <p className='mt-3 text-xs text-amber-200 bg-amber-500/10 border border-amber-500/20 rounded-lg p-3'>
                    Risk/Reward chưa hấp dẫn, không nên mua vội.
                  </p>
                )}
              </SectionCard>

              <SectionCard title='Hỗ trợ / kháng cự' icon={<Target className='h-4 w-4 text-blue-400' />}>
                <InfoRow label='Hỗ trợ gần nhất' value={formatCurrency(levels.supportNearest)} />
                <InfoRow label='Kháng cự gần nhất' value={formatCurrency(levels.resistanceNearest)} />
                <InfoRow label='Cách hỗ trợ' value={formatPercent(levels.distanceToSupportPercent)} />
                <InfoRow label='Cách kháng cự' value={formatPercent(levels.distanceToResistancePercent)} />
              </SectionCard>

              <SectionCard title='Thị trường chung' icon={<Landmark className='h-4 w-4 text-amber-400' />}>
                {market.vnindexTrend === 'UNKNOWN' || !market.vnindexTrend ? (
                  <p className='text-slate-400 text-sm'>Chưa có dữ liệu thị trường chung.</p>
                ) : (
                  <>
                    <InfoRow label='VNINDEX' value={formatIndicator(market.vnindexPrice)} />
                    <InfoRow label='Thay đổi' value={formatPercent(market.vnindexChangePercent)} />
                    <InfoRow label='VNINDEX MA20' value={formatIndicator(market.vnindexMa20)} />
                    <InfoRow label='Trend' value={market.vnindexTrend} />
                    <InfoRow label='Condition' value={market.marketCondition} />
                  </>
                )}
              </SectionCard>
            </div>

            <div className='grid grid-cols-1 lg:grid-cols-3 gap-5'>
              <SectionCard title='Lệnh gợi ý' icon={<WalletCards className='h-4 w-4 text-emerald-400' />}>
                <InfoRow label='Loại lệnh' value={suggestedOrder.orderType || '--'} />
                <InfoRow label='Hành động' value={suggestedOrder.action || '--'} />
                <InfoRow label='Giá mua gợi ý' value={formatCurrency(suggestedOrder.buyPrice)} />
                <InfoRow label='Giá bán gợi ý' value={formatCurrency(suggestedOrder.sellPrice)} />
                <p className='mt-3 text-sm text-slate-300 leading-relaxed'>{suggestedOrder.note || 'Chưa có ghi chú lệnh gợi ý.'}</p>
              </SectionCard>

              <div className='lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-5'>
                <ChecklistCard
                  title='Lý do tích cực'
                  icon={<ListChecks className='h-4 w-4 text-emerald-400' />}
                  items={reasons}
                  emptyText='Chưa có lý do tích cực rõ ràng.'
                  type='positive'
                />
                <ChecklistCard
                  title='Cảnh báo'
                  icon={<AlertTriangle className='h-4 w-4 text-amber-400' />}
                  items={warnings}
                  emptyText='Chưa có cảnh báo.'
                  type='warning'
                />
              </div>
            </div>

            <SectionCard title='Bộ chỉ báo kỹ thuật' icon={<Activity className='h-4 w-4 text-blue-400' />}>
              <div className='grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3'>
                <MiniMetric label='RSI14' value={formatIndicator(technical.rsi14)} />
                <MiniMetric label='MA20' value={formatCurrency(technical.ma20)} />
                <MiniMetric label='MA50' value={formatCurrency(technical.ma50)} />
                <MiniMetric label='MA100' value={formatCurrency(technical.ma100)} />
                <MiniMetric label='MA200' value={formatCurrency(technical.ma200)} />
                <MiniMetric label='MACD' value={formatIndicator(technical.macd)} />
                <MiniMetric label='Signal' value={formatIndicator(technical.macdSignal)} />
                <MiniMetric label='Histogram' value={formatIndicator(technical.macdHistogram)} />
                <MiniMetric label='Volume' value={formatNumber(technical.volume)} />
                <MiniMetric label='Avg Vol 20' value={formatNumber(technical.avgVolume20)} />
              </div>
            </SectionCard>

            <div className='bg-[#131A35] p-4 md:p-6 rounded-xl border border-slate-800 shadow-lg'>
              <h3 className='text-base font-bold text-slate-300 mb-4 uppercase tracking-wider'>Biểu đồ diễn biến giá xu hướng & Khối lượng giao dịch</h3>
              <div className='h-[420px] w-full'>
                <ResponsiveContainer width='100%' height='100%'>
                  <ComposedChart data={stockData.data || []} margin={{ top: 10, right: 5, left: -15, bottom: 0 }}>
                    <CartesianGrid strokeDasharray='3 3' stroke='#1E264A' />
                    <XAxis dataKey='time' stroke='#64748B' fontSize={11} tickLine={false} />
                    <YAxis
                      yAxisId='price'
                      domain={[(dataMin) => Math.floor(dataMin * 0.98), (dataMax) => Math.ceil(dataMax * 1.02)]}
                      stroke='#64748B'
                      fontSize={11}
                      orientation='left'
                      tickFormatter={(v) => Number(v).toLocaleString('vi-VN')}
                    />
                    <YAxis yAxisId='volume' domain={['0', 'dataMax * 4']} orientation='right' hide />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#0D132E', borderColor: '#1E264A', borderRadius: '8px', color: '#fff' }}
                      formatter={(value, name) => {
                        if (value === null || value === undefined) return ['--', name];
                        return [name === 'Khối lượng' ? Number(value).toLocaleString('vi-VN') : formatCurrency(value), name];
                      }}
                    />
                    <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                    {levels.supportNearest && <ReferenceLine yAxisId='price' y={levels.supportNearest} stroke='#22C55E' strokeDasharray='4 4' label={{ value: 'Support', fill: '#22C55E', fontSize: 11 }} />}
                    {levels.resistanceNearest && <ReferenceLine yAxisId='price' y={levels.resistanceNearest} stroke='#F59E0B' strokeDasharray='4 4' label={{ value: 'Resistance', fill: '#F59E0B', fontSize: 11 }} />}
                    {riskManagement.stopLoss && <ReferenceLine yAxisId='price' y={riskManagement.stopLoss} stroke='#EF4444' strokeDasharray='4 4' label={{ value: 'Stop loss', fill: '#EF4444', fontSize: 11 }} />}
                    {takeProfitZone.from && <ReferenceLine yAxisId='price' y={takeProfitZone.from} stroke='#A78BFA' strokeDasharray='4 4' label={{ value: 'Take profit', fill: '#A78BFA', fontSize: 11 }} />}
                    <Bar yAxisId='volume' dataKey='volume' name='Khối lượng' fill='#3B82F6' opacity={0.15} radius={[2, 2, 0, 0]} />
                    <Line yAxisId='price' type='monotone' dataKey='close' name='Giá đóng cửa' stroke='#34D399' strokeWidth={2.5} dot={false} />
                    <Line yAxisId='price' type='monotone' dataKey='MA20' name='MA20' stroke='#60A5FA' strokeWidth={1.5} dot={false} />
                    <Line yAxisId='price' type='monotone' dataKey='MA50' name='MA50' stroke='#F59E0B' strokeWidth={1.5} dot={false} />
                    <Line yAxisId='price' type='monotone' dataKey='MA100' name='MA100' stroke='#EC4899' strokeWidth={1.5} dot={false} />
                    <Line yAxisId='price' type='monotone' dataKey='MA200' name='MA200' stroke='#8B5CF6' strokeWidth={1.5} dot={false} />
                  </ComposedChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className='bg-[#131A35] p-4 md:p-6 rounded-xl border border-slate-800 shadow-lg'>
              <h3 className='text-base font-bold text-slate-300 mb-4 uppercase tracking-wider'>Động lượng thị trường - Chỉ số Sức mạnh Tương đối (RSI)</h3>
              <div className='h-[170px] w-full'>
                <ResponsiveContainer width='100%' height='100%'>
                  <LineChart data={stockData.data || []} margin={{ top: 5, right: 5, left: -15, bottom: 0 }}>
                    <CartesianGrid strokeDasharray='3 3' stroke='#1E264A' />
                    <XAxis dataKey='time' stroke='#64748B' fontSize={11} tickLine={false} />
                    <YAxis domain={[0, 100]} ticks={[30, 50, 70]} stroke='#64748B' fontSize={11} />
                    <Tooltip contentStyle={{ backgroundColor: '#0D132E', borderColor: '#1E264A', borderRadius: '8px' }} />
                    <ReferenceLine y={30} stroke='#60A5FA' strokeDasharray='4 4' />
                    <ReferenceLine y={50} stroke='#94A3B8' strokeDasharray='4 4' />
                    <ReferenceLine y={70} stroke='#F43F5E' strokeDasharray='4 4' />
                    <Line type='monotone' dataKey='RSI' name='Chỉ số RSI' stroke='#F43F5E' strokeWidth={2} dot={false} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className='bg-[#131A35] p-4 md:p-6 rounded-xl border border-slate-800 shadow-lg'>
              <h3 className='text-base font-bold text-slate-300 mb-4 uppercase tracking-wider'>MACD - Xu hướng động lượng</h3>
              <div className='h-[240px] w-full'>
                <ResponsiveContainer width='100%' height='100%'>
                  <ComposedChart data={stockData.data || []} margin={{ top: 5, right: 5, left: -15, bottom: 0 }}>
                    <CartesianGrid strokeDasharray='3 3' stroke='#1E264A' />
                    <XAxis dataKey='time' stroke='#64748B' fontSize={11} tickLine={false} />
                    <YAxis stroke='#64748B' fontSize={11} />
                    <Tooltip contentStyle={{ backgroundColor: '#0D132E', borderColor: '#1E264A', borderRadius: '8px' }} />
                    <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                    <ReferenceLine y={0} stroke='#64748B' strokeDasharray='4 4' />
                    <Bar dataKey='MACD_Histogram' name='Histogram' fill='#64748B' opacity={0.35} radius={[2, 2, 0, 0]} />
                    <Line type='monotone' dataKey='MACD' name='MACD' stroke='#34D399' strokeWidth={2} dot={false} />
                    <Line type='monotone' dataKey='Signal_Line' name='Signal' stroke='#F59E0B' strokeWidth={2} dot={false} />
                  </ComposedChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function SectionCard({ title, icon, children }) {
  return (
    <div className='bg-[#131A35] p-5 rounded-xl border border-slate-800 shadow-lg'>
      <div className='flex items-center gap-2 border-b border-slate-800 pb-3 mb-4'>
        {icon}
        <h3 className='text-sm font-bold uppercase tracking-wider text-slate-300'>{title}</h3>
      </div>
      {children}
    </div>
  );
}

function InfoRow({ label, value, valueClass = 'text-slate-100' }) {
  return (
    <div className='flex items-center justify-between gap-3 py-2 border-b border-slate-800/70 last:border-0'>
      <span className='text-sm text-slate-400'>{label}</span>
      <span className={`text-sm font-bold text-right ${valueClass}`}>{value}</span>
    </div>
  );
}

function MiniMetric({ label, value }) {
  return (
    <div className='bg-[#0A0F24]/60 border border-slate-800 rounded-lg p-3'>
      <p className='text-[11px] uppercase tracking-wider text-slate-500 font-bold'>{label}</p>
      <p className='text-sm md:text-base font-extrabold text-slate-100 mt-1 break-words'>{value}</p>
    </div>
  );
}

function ChecklistCard({ title, icon, items, emptyText, type }) {
  const isPositive = type === 'positive';
  return (
    <div className='bg-[#131A35] p-5 rounded-xl border border-slate-800 shadow-lg'>
      <div className='flex items-center gap-2 border-b border-slate-800 pb-3 mb-4'>
        {icon}
        <h3 className='text-sm font-bold uppercase tracking-wider text-slate-300'>{title}</h3>
      </div>
      {items.length === 0 ? (
        <p className='text-sm text-slate-500'>{emptyText}</p>
      ) : (
        <ul className='space-y-3'>
          {items.map((item, index) => (
            <li key={`${title}-${index}`} className='flex items-start gap-2 text-sm leading-relaxed text-slate-300'>
              {isPositive ? (
                <CheckCircle2 className='h-4 w-4 text-emerald-400 shrink-0 mt-0.5' />
              ) : (
                <AlertTriangle className='h-4 w-4 text-amber-400 shrink-0 mt-0.5' />
              )}
              <span>{item}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
