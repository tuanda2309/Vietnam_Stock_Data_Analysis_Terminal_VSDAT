import React from 'react';
import ReactDOM from 'react-dom/client';

import App from './App.jsx';
import ErrorBoundary from './components/layout/ErrorBoundary.jsx';
import { LanguageProvider } from './i18n/LanguageContext.jsx';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <LanguageProvider>
      <ErrorBoundary>
        <App />
      </ErrorBoundary>
    </LanguageProvider>
  </React.StrictMode>,
);
