import { defineStore } from 'pinia'
import authApi from '@/auth/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null
  }),
  actions: {
    async login(credentials) {
      const response = await authApi.login(credentials)
      this.setAuthData(response.data)
    },
    async register(userData) {
      const response = await authApi.register(userData)
      this.setAuthData(response.data)
    },
    setAuthData({ user, token }) {
      this.user = user
      this.token = token
      localStorage.setItem('token', token)
    },
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    }
  }
})