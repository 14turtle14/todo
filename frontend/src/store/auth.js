import { defineStore } from 'pinia';
import router from '@/router';
import { jwtDecode } from 'jwt-decode';
import api from '@/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('accessToken') || null,
    user: null     
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },

  actions: {
    setAccessToken(token) {
      this.accessToken = token;
      localStorage.setItem('accessToken', token);
    },

    clearAuthData() {
      this.accessToken = null;
      this.user = null;
      localStorage.removeItem('accessToken');
      router.push('/login');
    },

    async checkTokenExpiration() {
      if (!this.accessToken) return false;

      try {
        const payload = jwtDecode(this.accessToken);
        const isExpired = payload.exp < Date.now() / 1000;

        if (isExpired) {
          return await this.refreshToken();
        }
        return true;
      } catch (error) {
        this.clearAuthData();
        return false;
      }
    },

    async refreshToken() {
      try {
        const response = await api.refreshToken();
        this.setAccessToken(response.data.access_token);
        await this.fetchUser();
        return true;
      } catch (error) {
        this.clearAuthData();
        throw error;
      }
    },

    async fetchUser() {
      try {
        const response = await api.fetchUser();
        this.user = response.data;
      } catch (error) {
        console.error('Failed to fetch user data', error);
        throw error;
      }
    },

    async login(login, password) {
      try {
        const response = await api.login(login, password);
        this.setAccessToken(response.data.access_token);
        await this.fetchUser();
        router.push('/home');
      } catch (error) {
        console.error('Login failed', error);
        throw error;
      }
    },

    async signup(username, email, password) {
      try {
        const response = await api.signup(username, email, password);
        this.setAccessToken(response.data.access_token);
        await this.fetchUser();
        router.push('/home');
      } catch (error) {
        console.error('Login failed', error);
        throw error;
      }
    },
    
    async logout() {
      try {
        await api.logout();
        this.clearAuthData();
        router.push('/login');
      } catch (error) {
        console.error('Logout failed', error);
        throw error;
      }
    }
  }
});