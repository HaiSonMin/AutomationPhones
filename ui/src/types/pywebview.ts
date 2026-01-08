// PyWebView Bridge Types
// Python provides these methods via window.pywebview.api

import type { PyWebViewAPI } from './auth';

// Extend Window
declare global {
  interface Window {
    pywebview: {
      auth: PyWebViewAPI;
    };
  }
}

export {};
