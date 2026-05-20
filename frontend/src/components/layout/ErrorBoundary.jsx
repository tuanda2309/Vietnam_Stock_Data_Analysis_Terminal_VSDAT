import React from 'react';

import { translations } from '../../i18n/translations';

const getBoundaryLanguage = () => {
  try {
    const savedLanguage = window.localStorage.getItem('vsdat_language');
    return savedLanguage === 'en' ? 'en' : 'vi';
  } catch {
    return 'vi';
  }
};

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      hasError: false,
    };
  }

  static getDerivedStateFromError() {
    return {
      hasError: true,
    };
  }

  componentDidCatch(error, info) {
    console.error('React display error:', error, info);
  }

  handleReload = () => {
    window.location.reload();
  };

  render() {
    if (!this.state.hasError) {
      return this.props.children;
    }

    const language = getBoundaryLanguage();
    const text = translations[language]?.errors || translations.vi.errors;

    return (
      <div className='notranslate min-h-screen bg-[#0A0F24] text-slate-100 p-6 md:p-10 font-sans flex items-center justify-center' translate='no'>
        <div className='max-w-xl w-full bg-[#131A35] border border-red-500/40 rounded-2xl p-6 md:p-8 shadow-2xl text-center'>
          <h1 className='text-2xl md:text-3xl font-extrabold text-red-300 mb-3'>
            {text.boundaryTitle}
          </h1>
          <p className='text-slate-300 leading-relaxed mb-6'>
            {text.boundaryMessage}
          </p>
          <button
            type='button'
            onClick={this.handleReload}
            className='bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-5 py-3 rounded-lg transition-all active:scale-95'
          >
            {text.reloadPage}
          </button>
        </div>
      </div>
    );
  }
}

export default ErrorBoundary;
