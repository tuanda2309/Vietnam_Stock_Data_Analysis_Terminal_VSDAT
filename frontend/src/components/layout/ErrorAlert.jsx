import { AlertTriangle } from 'lucide-react';

import { translateBackendText } from '../../i18n/backendTextTranslations';
import { useLanguage } from '../../i18n/LanguageContext';

function ErrorAlert({ error }) {
  const { language } = useLanguage();

  if (!error) return null;

  const translatedError = translateBackendText(error, language);

  return (
    <div className='bg-red-950/40 border border-red-900 text-red-200 p-4 rounded-lg mb-6 text-sm font-medium flex items-center gap-3 animate-fadeIn'>
      <AlertTriangle className='h-5 w-5 text-red-400 shrink-0' />
      <span>{translatedError}</span>
    </div>
  );
}

export default ErrorAlert;
