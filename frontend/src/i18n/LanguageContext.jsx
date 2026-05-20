import { createContext, useContext, useEffect, useMemo, useState } from 'react';

import { translations } from './translations';

const LANGUAGE_STORAGE_KEY = 'vsdat_language';
const DEFAULT_LANGUAGE = 'vi';
const SUPPORTED_LANGUAGES = ['vi', 'en'];

const LanguageContext = createContext(null);

const getInitialLanguage = () => {
  try {
    const savedLanguage = window.localStorage.getItem(LANGUAGE_STORAGE_KEY);
    if (SUPPORTED_LANGUAGES.includes(savedLanguage)) {
      return savedLanguage;
    }
  } catch (error) {
    console.warn('Cannot read language from localStorage:', error);
  }

  return DEFAULT_LANGUAGE;
};

const getNestedValue = (source, key) => {
  return key.split('.').reduce((current, part) => {
    if (current && Object.prototype.hasOwnProperty.call(current, part)) {
      return current[part];
    }

    return undefined;
  }, source);
};

export function LanguageProvider({ children }) {
  const [language, setLanguageState] = useState(getInitialLanguage);

  const setLanguage = (nextLanguage) => {
    if (!SUPPORTED_LANGUAGES.includes(nextLanguage)) {
      return;
    }

    setLanguageState(nextLanguage);

    try {
      window.localStorage.setItem(LANGUAGE_STORAGE_KEY, nextLanguage);
    } catch (error) {
      console.warn('Cannot save language to localStorage:', error);
    }
  };

  useEffect(() => {
    document.documentElement.lang = language;
    document.documentElement.setAttribute('translate', 'no');
    document.documentElement.classList.add('notranslate');
  }, [language]);

  const value = useMemo(() => {
    const t = (key) => {
      const currentLanguageValue = getNestedValue(translations[language], key);
      if (currentLanguageValue !== undefined) {
        return currentLanguageValue;
      }

      const fallbackValue = getNestedValue(translations[DEFAULT_LANGUAGE], key);
      if (fallbackValue !== undefined) {
        return fallbackValue;
      }

      return key;
    };

    return {
      language,
      setLanguage,
      t,
    };
  }, [language]);

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);

  if (!context) {
    throw new Error('useLanguage must be used inside LanguageProvider');
  }

  return context;
}
