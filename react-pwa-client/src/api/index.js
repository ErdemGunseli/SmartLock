/* This file stores some code used by several routers, and acts as a barrel file 
(a file that exports many modules at once) for the api folder. 
*/
export * from './authApi';
export * from './actionsApi';

export const API_BASE_URL = "http://localhost:8000"
