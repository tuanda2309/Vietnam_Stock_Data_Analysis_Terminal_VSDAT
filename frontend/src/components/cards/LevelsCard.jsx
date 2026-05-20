import { Target } from 'lucide-react';

import { useLanguage } from '../../i18n/LanguageContext';
import { formatCurrency, formatPercent } from '../../utils/formatters';
import InfoRow from './InfoRow';
import SectionCard from './SectionCard';

function LevelsCard({ levels }) {
  const { t } = useLanguage();

  return (
    <SectionCard title={t('levels.title')} icon={<Target className='h-4 w-4 text-blue-400' />}>
      <InfoRow label={t('levels.supportNearest')} value={formatCurrency(levels.supportNearest)} />
      <InfoRow label={t('levels.resistanceNearest')} value={formatCurrency(levels.resistanceNearest)} />
      <InfoRow label={t('levels.distanceToSupport')} value={formatPercent(levels.distanceToSupportPercent)} />
      <InfoRow label={t('levels.distanceToResistance')} value={formatPercent(levels.distanceToResistancePercent)} />
    </SectionCard>
  );
}

export default LevelsCard;
