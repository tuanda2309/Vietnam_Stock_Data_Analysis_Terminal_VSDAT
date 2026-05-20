import { ShieldCheck } from 'lucide-react';

import { formatCurrency } from '../../utils/formatters';
import InfoRow from './InfoRow';
import SectionCard from './SectionCard';

function RiskManagementCard({ riskManagement, entryZone, takeProfitZone, riskRewardRatio, riskRewardWeak }) {
  return (
    <SectionCard title='Vùng giá & quản trị rủi ro' icon={<ShieldCheck className='h-4 w-4 text-emerald-400' />}>
      <InfoRow label='Vùng mua đẹp' value={`${formatCurrency(entryZone.from)} - ${formatCurrency(entryZone.to)}`} />
      <InfoRow label='Cắt lỗ' value={formatCurrency(riskManagement.stopLoss)} valueClass='text-rose-300' />
      <InfoRow label='Chốt lời' value={`${formatCurrency(takeProfitZone.from)} - ${formatCurrency(takeProfitZone.to)}`} valueClass='text-emerald-300' />
      <InfoRow label='Risk/Reward' value={riskRewardRatio ?? '--'} valueClass={riskRewardWeak ? 'text-amber-300' : 'text-emerald-300'} />
      {riskRewardWeak && (
        <p className='mt-3 text-xs text-amber-200 bg-amber-500/10 border border-amber-500/20 rounded-lg p-3'>
          Risk/Reward chưa hấp dẫn, không nên mua vội.
        </p>
      )}
    </SectionCard>
  );
}

export default RiskManagementCard;
