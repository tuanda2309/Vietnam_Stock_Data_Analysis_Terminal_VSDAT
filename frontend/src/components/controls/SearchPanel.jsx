import { Activity, LineChart as ChartIcon, Loader2 } from 'lucide-react';

function SearchPanel({ symbol, handleSymbolChange, getStock, loading }) {
  return (
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
  );
}

export default SearchPanel;
