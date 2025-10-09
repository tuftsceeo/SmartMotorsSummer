/**
 * @file index.js
 * @description React application entry point
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

// Polyfill Buffer for browser environment
import { Buffer } from 'buffer';
window.Buffer = window.Buffer || Buffer;

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
