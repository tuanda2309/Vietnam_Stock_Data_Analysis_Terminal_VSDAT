import { Activity } from 'lucide-react';

import { useLanguage } from '../../i18n/LanguageContext';
import { formatCurrency, formatIndicator, formatNumber } from '../../utils/formatters';
import MiniMetric from './MiniMetric';
import SectionCard from './SectionCard';

function TechnicalMetricsCard({ technical }) {
  const { t } = useLanguage();

  return (
    <SectionCard title={t('technical.title')} icon={<Activity className='h-4 w-4 text-blue-400' />}>
      <div className='grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3'>
        <MiniMetric label={t('technical.rsi14')} value={formatIndicator(technical.rsi14)} />
        <MiniMetric label={t('technical.ma20')} value={formatCurrency(technical.ma20)} />
        <MiniMetric label={t('technical.ma50')} value={formatCurrency(technical.ma50)} />
        <MiniMetric label={t('technical.ma100')} value={formatCurrency(technical.ma100)} />
        <MiniMetric label={t('technical.ma200')} value={formatCurrency(technical.ma200)} />
        <MiniMetric label={t('technical.macd')} value={formatIndicator(technical.macd)} />
        <MiniMetric label={t('technical.signal')} value={formatIndicator(technical.macdSignal)} />
        <MiniMetric label={t('technical.histogram')} value={formatIndicator(technical.macdHistogram)} />
        <MiniMetric label={t('technical.volume')} value={formatNumber(technical.volume)} />
        <MiniMetric label={t('technical.avgVol20')} value={formatNumber(technical.avgVolume20)} />
      </div>
    </SectionCard>
  );
}

export default TechnicalMetricsCard;
