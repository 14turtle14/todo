import { defineStore } from 'pinia';
import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('jwt') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
    user: JSON.parse(localStorage.getItem('user')) || null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user
  },

  actions: {
    setAuthData({ token, refreshToken, user }) {
      this.token = token;
      this.refreshToken = refreshToken;
      this.user = user;
      
      localStorage.setItem('jwt', token);
      localStorage.setItem('refreshToken', refreshToken);
      localStorage.setItem('user', JSON.stringify(user));

      return { token, user };
    },

    clearAuthData() {
      this.token = null;
      this.refreshToken = null;
      this.user = null;
      
      localStorage.removeItem('jwt');
      localStorage.removeItem('refreshToken');
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
          },
          body: JSON.stringify({ refreshToken: this.refreshToken })
        });

        if (!response.ok) throw new Error('Refresh failed');

        const data = await response.json();
        this.setAuthData({
          token: data.accessToken,
          refreshToken: data.refreshToken,
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