import { Globe2 } from 'lucide-react';

import { useLanguage } from '../../i18n/LanguageContext';

function LanguageSwitcher() {
  const { language, setLanguage, t } = useLanguage();

  const baseButtonClass = 'px-3 py-1.5 rounded-lg text-xs md:text-sm font-bold transition-all border';
  const activeButtonClass = 'bg-emerald-500 text-slate-950 border-emerald-400 shadow-md';
  const inactiveButtonClass = 'bg-[#0A0F24]/70 text-slate-300 border-slate-700 hover:border-emerald-400/60 hover:text-emerald-300';

  return (
    <div className='mt-5 flex flex-wrap items-center justify-center gap-2 rounded-xl border border-slate-800 bg-[#131A35]/70 px-3 py-2 shadow-lg'>
      <div className='flex items-center gap-2 text-xs md:text-sm text-slate-400 font-semibold mr-1'>
        <Globe2 className='h-4 w-4 text-emerald-400' />
        <span>{t('language.label')}</span>
      </div>

      <button
        type='button'
        onClick={() => setLanguage('vi')}
        className={`${baseButtonClass} ${language === 'vi' ? activeButtonClass : inactiveButtonClass}`}
        aria-pressed={language === 'vi'}
      >
        {t('language.vietnamese')}
      </button>

      <button
        type='button'
        onClick={() => setLanguage('en')}
        className={`${baseButtonClass} ${language === 'en' ? activeButtonClass : inactiveButtonClass}`}
        aria-pressed={language === 'en'}
      >
        {t('language.english')}
      </button>
    </div>
  );
}

export default LanguageSwitcher;
