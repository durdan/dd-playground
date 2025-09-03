import React, { useState } from 'react';
import UserForm from './components/UserForm';
import UserList from './components/UserList';
import './App.css';

function App() {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleUserCreated = () => {
    // Force UserList to refresh
    setRefreshKey(prev => prev + 1);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>User Management</h1>
      </header>
      
      <main className="App-main">
        <div className="container">
          <div className="form-section">
            <UserForm onSuccess={handleUserCreated} />
          </div>
          
          <div className="list-section">
            <UserList key={refreshKey} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;