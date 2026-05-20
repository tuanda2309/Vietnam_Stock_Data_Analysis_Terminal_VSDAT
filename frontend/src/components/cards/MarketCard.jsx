import { Landmark } from 'lucide-react';

import { useLanguage } from '../../i18n/LanguageContext';
import { formatIndicator, formatPercent } from '../../utils/formatters';
import InfoRow from './InfoRow';
import SectionCard from './SectionCard';

function MarketCard({ market }) {
  const { t } = useLanguage();

  return (
    <SectionCard title={t('market.title')} icon={<Landmark className='h-4 w-4 text-amber-400' />}>
      {market.vnindexTrend === 'UNKNOWN' || !market.vnindexTrend ? (
        <p className='text-slate-400 text-sm'>{t('market.noData')}</p>
      ) : (
        <>
          <InfoRow label={t('market.vnindex')} value={formatIndicator(market.vnindexPrice)} />
          <InfoRow label={t('market.change')} value={formatPercent(market.vnindexChangePercent)} />
          <InfoRow label={t('market.vnindexMa20')} value={formatIndicator(market.vnindexMa20)} />
          <InfoRow label={t('market.trend')} value={market.vnindexTrend} />
          <InfoRow label={t('market.condition')} value={market.marketCondition} />
        </>
      )}
    </SectionCard>
  );
}

export default MarketCard;
