import { defineStore } from 'pinia';
import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: (() => {
      try {
        const userData = localStorage.getItem('user');
        return userData && userData !== 'undefined' 
          ? JSON.parse(userData) 
          : null;
      } catch (e) {
        console.error('Failed to parse user data:', e);
        return null;
      }
    }),
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user
  },

  actions: {
    setAuthData({ token, user }) {
      this.token = token;
      this.user = user;
      
      localStorage.setItem('jwt', token);
      localStorage.setItem('user', user);

      return { token, user };
    },

    clearAuthData() {
      this.token = null;
      this.user = null;
      
      localStorage.removeItem('jwt');
      localStorage.removeItem('user');
      
      const router = useRouter();
      router.push('/login');
    },

    async checkTokenExpiration() {
      if (!this.token) return false;

      try {
        const payload = JSON.parse(atob(this.token.split('.')[1]));
        const isExpired = payload.exp < Date.now() / 1000;
        
        if (isExpired) {
          try {
            await this.refreshToken();
            return true;
          } catch {
            return false;
          }
        }
        return true;
      } catch (error) {
        this.clearAuthData();
        return false;
      }
    },

    async refreshToken() {
      if (!this.refreshToken) {
        throw new Error('No refresh token available');
      }

      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/refresh`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) throw new Error('Refresh failed');

        const data = await response.json();
        this.setAuthData({
          token: data.accessToken,
          user: this.user
        });
        
        return data.accessToken;
      } catch (error) {
        this.clearAuthData();
        throw error;
      }
    }
  }
});