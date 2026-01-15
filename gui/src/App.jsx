import React from 'react';
import StatusBar from './components/StatusBar';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <div className="relative w-screen h-screen overflow-hidden selection:bg-brand-primary/30">
      <StatusBar />
      <Dashboard />
    </div>
  );
}

export default App;
