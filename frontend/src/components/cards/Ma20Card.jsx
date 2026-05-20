import { BarChart3 } from 'lucide-react';

import { useLanguage } from '../../i18n/LanguageContext';
import { formatCurrency } from '../../utils/formatters';

function Ma20Card({ technical, stockData }) {
  const { t } = useLanguage();

  return (
    <div className='bg-[#131A35] p-5 rounded-xl border border-slate-800 shadow-lg flex items-center justify-between'>
      <div>
        <h2 className='text-sm font-semibold text-slate-400 uppercase tracking-wider'>{t('ma.ma20Title')}</h2>
        <p className='text-3xl font-extrabold mt-2 text-blue-400'>{formatCurrency(technical.ma20 ?? stockData.ma20)}</p>
      </div>
      <div className='bg-blue-500/10 p-3 rounded-lg text-blue-400'><BarChart3 className='h-6 w-6' /></div>
    </div>
  );
}

export default Ma20Card;
