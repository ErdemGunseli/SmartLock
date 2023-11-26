import api from "../api/index.js";
import { authenticate } from '../api';


export default function KeyField({ state, setState }) {


    function handleSubmit() {
        const authenticated = authenticate(state.accessKey);
        console.log("AUTHENTICATED IS: ")
        console.log(authenticated)
        setState({...state, keyCorrect: authenticated});
    }

    return (
        <div className="key-field">
            <input type="password" placeholder={"Access Key"} value={state.accessKey}
            onChange={(event) => setState({...state, accessKey: event.target.value})}/>

            {/* The button should call the function that sends the secret key to the server for verification, 
            but for testing purposes, just setting the key to be true. */}
            <button onClick={handleSubmit}>Continue</button>
        </div>
    );
}