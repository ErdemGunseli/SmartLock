import './App.css';
import KeyField from './components/KeyField';
import LockButton from './components/LockButton';


import { createContext, useState } from 'react';




/* To start the app:
  cd react-pwa-client
  npm start
*/


export default function App() {

  // Creating an object with identifier 'state' to avoid passing many props to children:
  const [state, setState] = useState({
    accessKey: "",
    keyCorrect: false
  });

  return (
    <div className="App">
      {/* If the secret key is correct, showing the lock/unlock button: */}
      {state.keyCorrect ? 
      <>
        <LockButton  />
      </>:
      <>
        <h1>Enter Access Key</h1>
        <KeyField state={state} setState={setState} />
      </>}
    </div>
  );
}

