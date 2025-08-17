import axios from 'axios';
import { useAuthStore } from '@/store/auth.js';

const api = axios.create({
  baseURL: 'http://127.0.0.1:4014',
  withCredentials: true, 
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json'
  }
});

api.interceptors.request.use(async (config) => {
  const authStore = useAuthStore();
  
  if (authStore.accessToken) {
    const isTokenValid = await authStore.checkTokenExpiration();
    
    if (isTokenValid) {
      config.headers.Authorization = `Bearer ${authStore.accessToken}`;
    }
  }
  
  return config;
});

api.interceptors.response.use(
  response => response,
  async (error) => {
    const authStore = useAuthStore();
    
    if (error.response?.status === 401 && !error.config._retry) {
      error.config._retry = true;
      
      try {
        await authStore.refreshToken();
        return api(error.config); 
      } catch (refreshError) {
        authStore.clearAuthData();
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export default {
  login(username, password) {
    return api.post('/auth/login', {username, password}, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
  },

  signup(username, email, password) {
    return api.post('/auth/signup', {username, email, password});
  },
  
  refreshToken() {
    return api.post('/auth/refresh', {}, {
      withCredentials: true 
    });
  },
  
  logout() {
    return api.post('/auth/logout');
  },
  
  fetchUser() {
    return api.get('/users/me');
  },
  
  getTargets() {
    return api.get('/targets');
  },

  createTarget(title, type, deadline, interval_days){
    if (type === 'default'){
      return api.post('/targets/', {title, type})
    } else if (type === 'periodic'){
      return api.post('/targets/', {title, type, interval_days})
    } else {
      return api.post('/targets/', {title, type, deadline})
    }
  }
};