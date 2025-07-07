import axios from 'axios';
import {useAuthStore} from '@/store/auth.js'

const api = axios.create({
  baseURL: 'http://localhost:4014', 
  withCredentials: false,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json'
  }
});

let authStore;

api.interceptors.request.use(async (config) => {
   if (!authStore) {
    authStore = useAuthStore(); 
  }
  
  if (authStore.token) {
    await authStore.checkTokenExpiration();
    config.headers.Authorization = `Bearer ${authStore.token}`;
  }
  
  return config;
}, (error) => {
  return Promise.reject(error);
});

api.interceptors.response.use(response => response, async (error) => {
  if (error.response?.status === 401) {
    if (!authStore) {
      authStore = useAuthStore();
    }
    authStore.clearAuthData();
  }
  return Promise.reject(error);
});

export default {
  async getTargets() {
    try {
      const response = await api.get('/targets');
      return response.data;
    } catch (error) {
      console.error('Error fetching targets:', error);
      throw error;
    }
  },

  async getUser(userId) {
    try {
      const response = await api.get('/user/{userId}');
      return response.data;
    } catch (error) {
      console.error('Error fetch user:', error);
      throw error;
    }
  },

  async login(username, password) {
    try {
      const response = await api.post('/auth/token', { username, password });
      return response.data;
    } catch (error) {
      console.error('Error logging in:', error);
      throw error;
    }
  },

  async register(username, email, password) {
    try {
      const response = await api.post('/auth/signup', { username, email, password });
      return response.data;
    } catch (error) {
      console.error('Error registering:', error);
      throw error;
    }
  }
};
