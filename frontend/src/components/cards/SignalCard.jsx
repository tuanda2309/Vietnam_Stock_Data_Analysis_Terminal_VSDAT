import { Gauge } from 'lucide-react';

import { translateActionCode, translateBackendText } from '../../i18n/backendTextTranslations';
import { useLanguage } from '../../i18n/LanguageContext';

function SignalCard({ signal, actionStyle }) {
  const { language, t } = useLanguage();

  const translatedAction = signal.action
    ? translateActionCode(signal.action, language)
    : t('signal.noSignalUpper');

  const translatedTitle = signal.title
    ? translateBackendText(signal.title, language)
    : t('signal.noSignal');

  const translatedSummary = signal.summary
    ? translateBackendText(signal.summary, language)
    : t('signal.noSignalSummary');

  return (
    <div className={`rounded-2xl border ${actionStyle.border} ${actionStyle.bg} p-5 md:p-6 shadow-xl`}>
      <div className='flex flex-col lg:flex-row lg:items-center lg:justify-between gap-5'>
        <div className='space-y-3'>
          <div className='flex items-center gap-3 flex-wrap'>
            <span className={`px-4 py-2 rounded-full text-sm font-black tracking-widest ${actionStyle.badge}`}>
              {translatedAction}
            </span>
            <span className='text-slate-400 text-sm font-medium'>{t('signal.confidence')}</span>
            <span className={`text-2xl font-extrabold ${actionStyle.text}`}>{signal.confidence ?? '--'}%</span>
          </div>
          <h2 className='text-2xl md:text-3xl font-extrabold text-slate-100'>
            {translatedTitle}
          </h2>
          <p className='text-slate-300 max-w-3xl leading-relaxed'>
            {translatedSummary}
          </p>
        </div>
        <div className='bg-[#0A0F24]/60 border border-slate-800 rounded-xl p-4 min-w-[220px]'>
          <div className='flex items-center gap-2 text-slate-400 text-xs uppercase font-bold tracking-wider mb-2'>
            <Gauge className='h-4 w-4' />
            {t('signal.quickSummary')}
          </div>
          <p className='text-sm text-slate-300'>{t('signal.quickSummaryText')}</p>
        </div>
      </div>
    </div>
  );
}

export default SignalCard;
