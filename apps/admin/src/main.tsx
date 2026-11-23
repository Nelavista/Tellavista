import { applyTheme } from '@nelavista/ui';
import * as React from 'react';
import { createRoot } from 'react-dom/client';

import { App } from './App';
import { initTelemetry } from './lib/telemetry';
import './styles.css';

applyTheme('dark');
document.body.classList.add('nv-admin');
initTelemetry();

const container = document.getElementById('root');
if (!container) throw new Error('#root not found');

createRoot(container).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
