/**
 * @file App.jsx
 * @description Main application component
 */

import React from 'react';
import { BLEProvider } from './bluetooth/context/BLEContext';
import SmartMotorSpike from './components/SmartMotorSpike';

function App() {
  return (
    <BLEProvider>
      <SmartMotorSpike />
    </BLEProvider>
  );
}

export default App;
