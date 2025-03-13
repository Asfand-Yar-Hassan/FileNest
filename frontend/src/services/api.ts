import axios from 'axios';

const BASE_URL = 'http://54.162.76.167:8000';

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  login: (username: string, password: string) => 
    api.post('/login', { username, password }),
  
  signup: (username: string, email: string, password: string) => 
    api.post('/signup', { username, email, password }),
  
  logout: () => api.post('/logout'),
};

export const filesAPI = {
  getFiles: () => api.get('/'),
  
  uploadFile: (formData: FormData) => 
    api.post('/upload_file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }),
  
  deleteFile: (fileId: string) => 
    api.delete('/delete_file', { data: { file_id: fileId } }),
};

export default api; 