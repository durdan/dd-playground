import React from 'react';
import DiagramEditor from './components/DiagramEditor';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Diagram Editor</h1>
      </header>
      <main>
        <DiagramEditor />
      </main>
    </div>
  );
}

export default App;