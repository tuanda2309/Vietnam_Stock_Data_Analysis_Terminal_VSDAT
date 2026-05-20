import { Activity } from 'lucide-react';

import { formatCurrency, formatIndicator, formatNumber } from '../../utils/formatters';
import MiniMetric from './MiniMetric';
import SectionCard from './SectionCard';

function TechnicalMetricsCard({ technical }) {
  return (
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
  );
}

export default TechnicalMetricsCard;
