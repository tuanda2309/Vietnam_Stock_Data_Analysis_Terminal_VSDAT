import { WalletCards } from 'lucide-react';

import { translateActionCode, translateBackendText } from '../../i18n/backendTextTranslations';
import { useLanguage } from '../../i18n/LanguageContext';
import { formatCurrency } from '../../utils/formatters';
import InfoRow from './InfoRow';
import SectionCard from './SectionCard';

function SuggestedOrderCard({ suggestedOrder }) {
  const { language, t } = useLanguage();

  const translatedOrderType = suggestedOrder.orderType
    ? translateActionCode(suggestedOrder.orderType, language)
    : '--';

  const translatedAction = suggestedOrder.action
    ? translateActionCode(suggestedOrder.action, language)
    : '--';

  const translatedNote = suggestedOrder.note
    ? translateBackendText(suggestedOrder.note, language)
    : t('order.noNote');

  return (
    <SectionCard title={t('order.title')} icon={<WalletCards className='h-4 w-4 text-emerald-400' />}>
      <InfoRow label={t('order.orderType')} value={translatedOrderType} />
      <InfoRow label={t('order.action')} value={translatedAction} />
      <InfoRow label={t('order.buyPrice')} value={formatCurrency(suggestedOrder.buyPrice)} />
      <InfoRow label={t('order.sellPrice')} value={formatCurrency(suggestedOrder.sellPrice)} />
      <p className='mt-3 text-sm text-slate-300 leading-relaxed'>{translatedNote}</p>
    </SectionCard>
  );
}

export default SuggestedOrderCard;
