import { Activity } from 'lucide-react';

import { useLanguage } from '../../i18n/LanguageContext';
import { formatIndicator } from '../../utils/formatters';

function RsiCard({ technical, stockData }) {
  const { t } = useLanguage();

  const rsiValue = technical.rsi14 ?? stockData.rsi;

  return (
    <div className='bg-[#131A35] p-5 rounded-xl border border-slate-800 shadow-lg flex items-center justify-between'>
      <div>
        <h2 className='text-sm font-semibold text-slate-400 uppercase tracking-wider'>{t('rsi.title')}</h2>
        <p className={`text-3xl font-extrabold mt-2 ${rsiValue >= 70 ? 'text-red-400' : rsiValue <= 30 ? 'text-blue-400' : 'text-slate-200'}`}>
          {formatIndicator(rsiValue)}
        </p>
        <span className='text-xs font-bold mt-1 block text-slate-500'>
          {rsiValue >= 70 ? `⚠️ ${t('rsi.overbought')}` : rsiValue <= 30 ? `📉 ${t('rsi.oversold')}` : `⚖️ ${t('rsi.neutral')}`}
        </span>
      </div>
      <div className='bg-slate-700/20 p-3 rounded-lg text-slate-300'><Activity className='h-6 w-6' /></div>
    </div>
  );
}

export default RsiCard;
