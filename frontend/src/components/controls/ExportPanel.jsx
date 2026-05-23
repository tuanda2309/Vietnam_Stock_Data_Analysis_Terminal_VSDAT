import { Download, FileSpreadsheet, Loader2 } from 'lucide-react';

import { useLanguage } from '../../i18n/LanguageContext';

function ExportPanel({ startDate, endDate, setStartDate, setEndDate, exportExcel, exporting, loading, todayDate }) {
  const { t } = useLanguage();
  const disabled = exporting || loading;

  return (
    <div className='lg:col-span-7 bg-[#131A35] p-5 md:p-6 rounded-xl shadow-xl border border-slate-800 flex flex-col justify-center hover:border-amber-500/30 transition-all duration-300'>
      <div className='space-y-4 w-full'>
        <div className='flex items-center gap-2 border-b border-slate-800 pb-2.5'>
          <FileSpreadsheet className='h-4 w-4 text-amber-400' />
          <label className='block text-xs font-bold uppercase text-amber-400 tracking-wider'>
            {t('export.title')}
          </label>
        </div>

        <div className='grid grid-cols-1 sm:grid-cols-3 gap-3'>
          <div className='relative'>
            <span className='absolute -top-2 left-2 px-1 text-[10px] text-slate-400 bg-[#131A35] font-medium z-10'>{t('export.fromDate')}</span>
            <input
              type='date'
              value={startDate}
              max={todayDate}
              disabled={disabled}
              onChange={(e) => setStartDate(e.target.value)}
              className='p-3 pt-3.5 rounded-lg text-white bg-[#1E264A] border border-slate-700 w-full focus:outline-none focus:ring-2 focus:ring-amber-500 transition-all text-sm font-medium disabled:opacity-60'
            />
          </div>

          <div className='relative'>
            <span className='absolute -top-2 left-2 px-1 text-[10px] text-slate-400 bg-[#131A35] font-medium z-10'>{t('export.toDate')}</span>
            <input
              type='date'
              value={endDate}
              max={todayDate}
              disabled={disabled}
              onChange={(e) => setEndDate(e.target.value)}
              className='p-3 pt-3.5 rounded-lg text-white bg-[#1E264A] border border-slate-700 w-full focus:outline-none focus:ring-2 focus:ring-amber-500 transition-all text-sm font-medium disabled:opacity-60'
            />
          </div>

          <button
            onClick={exportExcel}
            disabled={disabled}
            className='bg-amber-600 hover:bg-amber-500 disabled:bg-slate-800 disabled:text-slate-500 p-3 rounded-lg text-slate-950 font-bold transition-all flex items-center gap-2 shadow-md w-full justify-center whitespace-nowrap active:scale-95 text-sm h-full'
          >
            {exporting ? <Loader2 className='h-4 w-4 animate-spin text-slate-950' /> : <Download className='h-4 w-4 text-slate-950' />}
            {t('export.button')}
          </button>
        </div>
      </div>
    </div>
  );
}

export default ExportPanel;
