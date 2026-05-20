import { WalletCards } from 'lucide-react';

import { formatCurrency } from '../../utils/formatters';
import InfoRow from './InfoRow';
import SectionCard from './SectionCard';

function SuggestedOrderCard({ suggestedOrder }) {
  return (
    <SectionCard title='Lệnh gợi ý' icon={<WalletCards className='h-4 w-4 text-emerald-400' />}>
      <InfoRow label='Loại lệnh' value={suggestedOrder.orderType || '--'} />
      <InfoRow label='Hành động' value={suggestedOrder.action || '--'} />
      <InfoRow label='Giá mua gợi ý' value={formatCurrency(suggestedOrder.buyPrice)} />
      <InfoRow label='Giá bán gợi ý' value={formatCurrency(suggestedOrder.sellPrice)} />
      <p className='mt-3 text-sm text-slate-300 leading-relaxed'>{suggestedOrder.note || 'Chưa có ghi chú lệnh gợi ý.'}</p>
    </SectionCard>
  );
}

export default SuggestedOrderCard;
