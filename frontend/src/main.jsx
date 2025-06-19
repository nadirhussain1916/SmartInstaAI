
import { createRoot } from 'react-dom/client';
import { Provider } from 'react-redux';

import './index.scss';

// COMPONENTS
import store from '@store';
import App from '@app/App';

createRoot(document.getElementById('root')).render(
  <Provider store={store}>
    <App />
  </Provider>
);

import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import './index.css';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>
);

