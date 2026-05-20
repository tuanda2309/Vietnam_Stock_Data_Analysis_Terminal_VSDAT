import { Target } from 'lucide-react';

import { formatCurrency, formatPercent } from '../../utils/formatters';
import InfoRow from './InfoRow';
import SectionCard from './SectionCard';

function LevelsCard({ levels }) {
  return (
    <SectionCard title='Hỗ trợ / kháng cự' icon={<Target className='h-4 w-4 text-blue-400' />}>
      <InfoRow label='Hỗ trợ gần nhất' value={formatCurrency(levels.supportNearest)} />
      <InfoRow label='Kháng cự gần nhất' value={formatCurrency(levels.resistanceNearest)} />
      <InfoRow label='Cách hỗ trợ' value={formatPercent(levels.distanceToSupportPercent)} />
      <InfoRow label='Cách kháng cự' value={formatPercent(levels.distanceToResistancePercent)} />
    </SectionCard>
  );
}

export default LevelsCard;
