import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import ErrorBoundary from './ErrorBoundary';
import logger from './utils/logger';

// Ловим глобальные JS ошибки
window.addEventListener("error", (e) => {
  logger.error("📛 JS ошибка:", e.message, e.filename, e.lineno);
});

// Ловим необработанные промисы
window.addEventListener("unhandledrejection", (e) => {
  logger.error("📛 Необработанный Promise:", e.reason);
});

ReactDOM.createRoot(document.getElementById('root')).render(
  <ErrorBoundary>
    <App />
  </ErrorBoundary>
);