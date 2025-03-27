import React, { useEffect } from 'react';
import './App.css';
import axios from 'axios';

import CardsPage from './pages/CardsPage';

function App() {
  useEffect(() => {
    axios.post('/api/ping', {
        timestamp: new Date().toISOString(),
    });
  }, []);
  return <CardsPage />;
}

export default App; 