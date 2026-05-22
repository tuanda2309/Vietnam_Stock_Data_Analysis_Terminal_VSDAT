import { Minus, TrendingDown, TrendingUp } from 'lucide-react';

import { useLanguage } from '../../i18n/LanguageContext';
import { formatCurrency, formatNumber, formatPercent } from '../../utils/formatters';

const toNumberOrNull = (value) => {
  if (value === null || value === undefined || value === '') return null;
  const numberValue = Number(value);
  return Number.isFinite(numberValue) ? numberValue : null;
};

function PriceCard({ stockData, statusColorClass }) {
  const { t } = useLanguage();
  const priceChange = toNumberOrNull(stockData.priceChange);
  const status = stockData.status || 'unknown';

  const statusLabel = status === 'up'
    ? t('price.up')
    : status === 'down'
      ? t('price.down')
      : status === 'unchanged'
        ? t('price.unchanged')
        : '--';

  const iconClass = status === 'up'
    ? 'bg-emerald-500/10 text-emerald-400'
    : status === 'down'
      ? 'bg-rose-500/10 text-rose-400'
      : status === 'unchanged'
        ? 'bg-amber-500/10 text-amber-400'
        : 'bg-slate-500/10 text-slate-400';

  return (
    <div className='bg-[#131A35] p-5 rounded-xl border border-slate-800 shadow-lg flex items-center justify-between'>
      <div>
        <h2 className='text-sm font-semibold text-slate-400 uppercase tracking-wider'>{t('price.current')} ({stockData.symbol})</h2>
        <p className={`text-3xl font-extrabold mt-2 tracking-tight ${statusColorClass}`}>
          {formatCurrency(stockData.currentPrice)}
        </p>
        <div className={`flex items-center gap-1.5 text-xs font-bold mt-1.5 ${statusColorClass}`}>
          <span>{priceChange !== null && priceChange > 0 ? '+' : ''}{formatNumber(priceChange)}đ</span>
          <span>({formatPercent(stockData.percentChange)})</span>
          <span className='sr-only'>{statusLabel}</span>
        </div>
      </div>
      <div title={statusLabel} className={`p-3 rounded-lg ${iconClass}`}>
        {status === 'up'
          ? <TrendingUp className='h-6 w-6' />
          : status === 'down'
            ? <TrendingDown className='h-6 w-6' />
            : <Minus className='h-6 w-6' />}
      </div>
    </div>
  );
}

export default PriceCard;
