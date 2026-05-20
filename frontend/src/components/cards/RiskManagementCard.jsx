import { ShieldCheck } from 'lucide-react';

import { useLanguage } from '../../i18n/LanguageContext';
import { formatCurrency } from '../../utils/formatters';
import InfoRow from './InfoRow';
import SectionCard from './SectionCard';

function RiskManagementCard({ riskManagement, entryZone, takeProfitZone, riskRewardRatio, riskRewardWeak }) {
  const { t } = useLanguage();

  return (
    <SectionCard title={t('riskManagement.title')} icon={<ShieldCheck className='h-4 w-4 text-emerald-400' />}>
      <InfoRow label={t('riskManagement.entryZone')} value={`${formatCurrency(entryZone.from)} - ${formatCurrency(entryZone.to)}`} />
      <InfoRow label={t('riskManagement.stopLoss')} value={formatCurrency(riskManagement.stopLoss)} valueClass='text-rose-300' />
      <InfoRow label={t('riskManagement.takeProfit')} value={`${formatCurrency(takeProfitZone.from)} - ${formatCurrency(takeProfitZone.to)}`} valueClass='text-emerald-300' />
      <InfoRow label={t('riskManagement.riskReward')} value={riskRewardRatio ?? '--'} valueClass={riskRewardWeak ? 'text-amber-300' : 'text-emerald-300'} />
      {riskRewardWeak && (
        <p className='mt-3 text-xs text-amber-200 bg-amber-500/10 border border-amber-500/20 rounded-lg p-3'>
          {t('riskManagement.weakRiskReward')}
        </p>
      )}
    </SectionCard>
  );
}

export default RiskManagementCard;
