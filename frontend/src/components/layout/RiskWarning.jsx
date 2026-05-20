import { AlertTriangle } from 'lucide-react';

import { useLanguage } from '../../i18n/LanguageContext';

function RiskWarning() {
  const { t } = useLanguage();

  return (
    <div className='mb-6 bg-amber-500/10 border border-amber-500/30 rounded-xl p-4 flex items-start gap-3 text-sm text-amber-100'>
      <AlertTriangle className='h-5 w-5 text-amber-300 shrink-0 mt-0.5' />
      <p>
        <span className='font-bold'>{t('risk.title')}</span> {t('risk.text')}
      </p>
    </div>
  );
}

export default RiskWarning;
