import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// You can add interceptors for request/response logging or error handling here
// apiClient.interceptors.request.use(request => {
//   console.log('Starting Request', request);
//   return request;
// });

// apiClient.interceptors.response.use(response => {
//   console.log('Response:', response);
//   return response;
// }, error => {
//   console.error('Response Error:', error.response || error.message);
//   return Promise.reject(error);
// });

export default apiClient;
