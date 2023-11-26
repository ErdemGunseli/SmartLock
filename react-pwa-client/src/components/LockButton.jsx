import { useState } from "react";

export default function LockButton() {
    const [locked, setLocked] = useState(true);

    function toggleLock() {
        /* Make API call to verify secret key
        
        if (secretKeyCorrect) {
            setLocked(!locked);
        } else {
            alert("Incorrect Secret Key");
        }
        */
        // ToDo: Remove the following:
        setLocked(!locked);
    }

    return (
        <div className="lock-button">
            <h1>{locked ? "Status: Locked" : "Status: Unlocked"}</h1>
            <button onClick={() => toggleLock()}>{locked ? "Unlock Door?" : "Lock Door?"}</button>
        </div>
    );
}



// ToDo: Handle secret key in another file.
/* Once the key is submitted, a request should be made to the server to ensure it is correct.
Subsequent requests should contain the secret key as well.
*/