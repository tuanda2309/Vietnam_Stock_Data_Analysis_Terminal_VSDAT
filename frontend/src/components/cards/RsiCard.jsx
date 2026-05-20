import { Activity } from 'lucide-react';

import { formatIndicator } from '../../utils/formatters';

function RsiCard({ technical, stockData }) {
  return (
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
  );
}

export default RsiCard;
