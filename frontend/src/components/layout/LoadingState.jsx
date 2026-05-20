import { Loader2 } from 'lucide-react';

import { useLanguage } from '../../i18n/LanguageContext';

function LoadingState({ loading }) {
  const { t } = useLanguage();

  if (!loading) return null;

  return (
    <div className='flex flex-col items-center justify-center p-20 bg-[#131A35] rounded-xl border border-slate-800 shadow-xl'>
      <Loader2 className='h-12 w-12 text-emerald-500 animate-spin mb-4' />
      <p className='text-slate-400 font-medium'>{t('loading.text')}</p>
    </div>
  );
}

export default LoadingState;
