import { applyTheme } from '@nelavista/ui';
import * as React from 'react';
import { createRoot } from 'react-dom/client';

import { App } from './App';
import './styles.css';

applyTheme('ink');
document.body.classList.add('nv-admin');

const container = document.getElementById('root');
if (!container) throw new Error('#root not found');

createRoot(container).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
