/* The only auth endpoint accessible on the client-side will be the login endpoint. 
The other endpoints will be accessible on the server-side, 
or through SwaggerUI when connected to the same network as the server. 
*/
import axios from 'axios';
import { API_BASE_URL } from './index';

export const authenticate = async (accessKey) => {
    try {
        // Sending a POST request to the authentication endpoint with the user data and returning the response:
        const response = await axios.post(`${API_BASE_URL}/auth/token`, {
            // The OAuth2PasswordRequestForm expects a username, but the server doesn't need it:
            username: "null",
            password: accessKey,
        });
        return { data: response.data };

    } catch (error) {
        /* Catching any errors and returning the error message,
        because React cannot display the fallback UI for errors thrown in async functions. 
        It is also necessary to check for the error message manually in the calling component.
        Using optional chining since error.response and error.response.data may be undefined:
        */
        return { error: error.response?.data?.detail || "An error occurred" };
    }
};

