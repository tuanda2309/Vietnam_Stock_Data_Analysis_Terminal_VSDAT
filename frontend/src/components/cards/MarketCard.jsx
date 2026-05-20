import { Landmark } from 'lucide-react';

import { formatIndicator, formatPercent } from '../../utils/formatters';
import InfoRow from './InfoRow';
import SectionCard from './SectionCard';

function MarketCard({ market }) {
  return (
    <SectionCard title='Thị trường chung' icon={<Landmark className='h-4 w-4 text-amber-400' />}>
      {market.vnindexTrend === 'UNKNOWN' || !market.vnindexTrend ? (
        <p className='text-slate-400 text-sm'>Chưa có dữ liệu thị trường chung.</p>
      ) : (
        <>
          <InfoRow label='VNINDEX' value={formatIndicator(market.vnindexPrice)} />
          <InfoRow label='Thay đổi' value={formatPercent(market.vnindexChangePercent)} />
          <InfoRow label='VNINDEX MA20' value={formatIndicator(market.vnindexMa20)} />
          <InfoRow label='Trend' value={market.vnindexTrend} />
          <InfoRow label='Condition' value={market.marketCondition} />
        </>
      )}
    </SectionCard>
  );
}

export default MarketCard;
