import React from 'react';
import './styles.css';
import AllCameras from './AllCameras';

function App() {
  return (
    <>
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'}}>
      <h1>Face2Music</h1>
    </div>
    <div className='App'
    style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'}}>
      <AllCameras/>
    </div>
    </>
  );
}

export default App;
