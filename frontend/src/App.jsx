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
  LineChart
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
  LineChart as ChartIcon
} from 'lucide-react';

const API_BASE_URL = import.meta.env?.VITE_API_URL || 'http://127.0.0.1:5000';

function App() {
  const [symbol, setSymbol] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [exporting, setExporting] = useState(false); 
  const [error, setError] = useState(null);

  const formatCurrency = (value) => {
    if (!value && value !== 0) return '0 đ';
    return value.toLocaleString('vi-VN', { style: 'currency', currency: 'VND' });
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
      console.log("=== DEBUG DỮ LIỆU NHẬN TỪ BACKEND ===");
      console.log(res.data);
      console.log("======================================");
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

      const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
      const downloadUrl = window.URL.createObjectURL(blob);
      const tempLink = document.createElement('a');
      tempLink.href = downloadUrl;
      tempLink.setAttribute('download', `${symbol}_Technical_Report_${startDate}.xlsx`);
      document.body.appendChild(tempLink);
      tempLink.click();
      tempLink.parentNode.removeChild(tempLink);
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

  return (
    <div className='min-h-screen bg-[#0A0F24] text-slate-100 p-4 md:p-10 font-sans antialiased'>
      <div className='max-w-7xl mx-auto'>
        
        {/* HEADER SECTION */}
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

        {/* =========================================================================
            KHU VỰC ĐIỀU KHIỂN - TRUY VẤN PHÂN TÍCH KỸ THUẬT & XUẤT DỮ LIỆU LỊCH SỬ EXCEL
           ========================================================================= */}
        <div className='grid grid-cols-1 lg:grid-cols-12 gap-6 mb-6 items-stretch'>
          
          {/* CARD 1: TRUY VẤN PHÂN TÍCH KỸ THUẬT (Chiếm 5 cột trên màn hình lớn) */}
          <div className='lg:col-span-5 bg-[#131A35] p-5 md:p-6 rounded-xl shadow-xl border border-slate-800 flex flex-col justify-center hover:border-emerald-500/30 transition-all duration-300'>
            <div className='space-y-4 w-full'>
              <div className='flex items-center gap-2 border-b border-slate-800 pb-2.5'>
                <ChartIcon className='h-4 w-4 text-emerald-400' />
                <label className='block text-xs font-bold uppercase text-emerald-400 tracking-wider'>
                  Truy vấn phân tích kỹ thuật
                </label>
              </div>
              
              {/* Chuyển sang Grid 3 cột tương thích 100% với cấu trúc của Card 2 */}
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

          {/* CARD 2: XUẤT DỮ LIỆU LỊCH SỬ EXCEL (Chiếm 7 cột trên màn hình lớn) */}
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

        {/* ERROR DISPLAY */}
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

        {/* THÀNH PHẦN HIỂN THỊ THẺ CHỈ SỐ VÀ ĐỒ THỊ */}
        {stockData && !loading && (
          <div className='space-y-6 animate-fadeIn'>
            
            <div className='grid grid-cols-1 md:grid-cols-3 gap-5'>
              <div className='bg-[#131A35] p-5 rounded-xl border border-slate-800 shadow-lg flex items-center justify-between'>
                <div>
                  <h2 className='text-sm font-semibold text-slate-400 uppercase tracking-wider'>Giá Hiện Tại ({stockData.symbol})</h2>
                  <p className={`text-3xl font-extrabold mt-2 tracking-tight ${
                    stockData.status === 'up' ? 'text-emerald-400' : 
                    stockData.status === 'down' ? 'text-rose-400' : 'text-amber-400'
                  }`}>
                    {formatCurrency(stockData.currentPrice)}
                  </p>
                  <div className={`flex items-center gap-1.5 text-xs font-bold mt-1.5 ${
                    stockData.status === 'up' ? 'text-emerald-400' : 
                    stockData.status === 'down' ? 'text-rose-400' : 'text-amber-400'
                  }`}>
                    <span>{stockData.priceChange > 0 ? '+' : ''}{stockData.priceChange.toLocaleString('vi-VN')}đ</span>
                    <span>({stockData.percentChange > 0 ? '+' : ''}{stockData.percentChange}%)</span>
                  </div>
                </div>
                <div className={`p-3 rounded-lg ${
                  stockData.status === 'up' ? 'bg-emerald-500/10 text-emerald-400' : 
                  stockData.status === 'down' ? 'bg-rose-500/10 text-rose-400' : 'bg-amber-500/10 text-amber-400'
                }`}>
                  {stockData.status === 'up' ? <TrendingUp className='h-6 w-6' /> : 
                   stockData.status === 'down' ? <TrendingDown className='h-6 w-6' /> : 
                   <Minus className='h-6 w-6' />}
                </div>
              </div>

              <div className='bg-[#131A35] p-5 rounded-xl border border-slate-800 shadow-lg flex items-center justify-between'>
                <div>
                  <h2 className='text-sm font-semibold text-slate-400 uppercase tracking-wider'>Chỉ số RSI (14 Phiên)</h2>
                  <p className={`text-3xl font-extrabold mt-2 ${stockData.rsi >= 70 ? 'text-red-400' : stockData.rsi <= 30 ? 'text-blue-400' : 'text-slate-200'}`}>
                    {stockData.rsi}
                  </p>
                  <span className='text-xs font-bold mt-1 block text-slate-500'>
                    {stockData.rsi >= 70 ? '⚠️ Quá Mua' : stockData.rsi <= 30 ? '📉 Quá Bán' : '⚖️ Trung Tính'}
                  </span>
                </div>
                <div className='bg-slate-700/20 p-3 rounded-lg text-slate-300'><Activity className='h-6 w-6' /></div>
              </div>

              <div className='bg-[#131A35] p-5 rounded-xl border border-slate-800 shadow-lg flex items-center justify-between'>
                <div>
                  <h2 className='text-sm font-semibold text-slate-400 uppercase tracking-wider'>Giá Trị Trung Bình MA20</h2>
                  <p className='text-3xl font-extrabold mt-2 text-blue-400'>{formatCurrency(stockData.ma20)}</p>
                </div>
                <div className='bg-blue-500/10 p-3 rounded-lg text-blue-400'><BarChart3 className='h-6 w-6' /></div>
              </div>
            </div>

            <div className='bg-[#131A35] p-4 md:p-6 rounded-xl border border-slate-800 shadow-lg'>
              <h3 className='text-base font-bold text-slate-300 mb-4 uppercase tracking-wider'>Biểu đồ diễn biến giá xu hướng & Khối lượng giao dịch</h3>
              <div className='h-[400px] w-full'>
                <ResponsiveContainer width="100%" height="100%">
                  <ComposedChart data={stockData.data} margin={{ top: 10, right: 5, left: -15, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1E264A" />
                    <XAxis dataKey="time" stroke="#64748B" fontSize={11} tickLine={false} />
                    <YAxis yAxisId="price" domain={[(dataMin) => Math.floor(dataMin * 0.98), (dataMax) => Math.ceil(dataMax * 1.02)]} stroke="#64748B" fontSize={11} orientation="left" tickFormatter={(v) => v.toLocaleString('vi-VN')} />
                    <YAxis yAxisId="volume" domain={['0', 'dataMax * 4']} orientation="right" hide />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#0D132E', borderColor: '#1E264A', borderRadius: '8px', color: '#fff' }}
                      formatter={(value, name) => [name === 'Khối lượng' ? value.toLocaleString() : formatCurrency(value), name]}
                    />
                    <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                    <Bar yAxisId="volume" dataKey="volume" name="Khối lượng" fill="#3B82F6" opacity={0.15} radius={[2, 2, 0, 0]} />
                    <Line yAxisId="price" type="monotone" dataKey="close" name="Giá đóng cửa" stroke="#34D399" strokeWidth={2.5} dot={false} />
                    <Line yAxisId="price" type="monotone" dataKey="MA20" name="MA20" stroke="#60A5FA" strokeWidth={1.5} dot={false} />
                    <Line yAxisId="price" type="monotone" dataKey="MA50" name="MA50" stroke="#F59E0B" strokeWidth={1.5} dot={false} />
                    <Line yAxisId="price" type="monotone" dataKey="MA100" name="MA100" stroke="#EC4899" strokeWidth={1.5} dot={false} />
                    <Line yAxisId="price" type="monotone" dataKey="MA200" name="MA200" stroke="#8B5CF6" strokeWidth={1.5} dot={false} />
                  </ComposedChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className='bg-[#131A35] p-4 md:p-6 rounded-xl border border-slate-800 shadow-lg'>
              <h3 className='text-base font-bold text-slate-300 mb-4 uppercase tracking-wider'>Động lượng thị trường - Chỉ số Sức mạnh Tương đối (RSI)</h3>
              <div className='h-[150px] w-full'>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={stockData.data} margin={{ top: 5, right: 5, left: -15, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1E264A" />
                    <XAxis dataKey="time" stroke="#64748B" fontSize={11} tickLine={false} />
                    <YAxis domain={[0, 100]} ticks={[30, 50, 70]} stroke="#64748B" fontSize={11} />
                    <Tooltip contentStyle={{ backgroundColor: '#0D132E', borderColor: '#1E264A', borderRadius: '8px' }} />
                    <Line type="monotone" dataKey="RSI" name="Chỉ số RSI" stroke="#F43F5E" strokeWidth={2} dot={false} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

          </div>
        )}
        
      </div>
    </div>
  );
}

export default App;