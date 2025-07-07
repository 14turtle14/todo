<template>
  <div class="register">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <input v-model="username" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <input v-model="email" type="email" placeholder="Email" required />
      <button type="submit">Register</button>
    </form>
    <p>Already have an account? <router-link to="/token">Login</router-link></p>
  </div>
</template>

<script>
import api from '@/api.js';
import {useAuthStore} from '@/store/auth.js'
export default {
  data() {
    return {
      username: '',
      email: '',
      password: ''
    };
  },
  methods: {
    async register() {
      try {
        const authStore = useAuthStore();
        const response = await api.register(this.username, this.email, this.password);
        
        authStore.setAuthData({
          token: response.accessToken,
          refreshToken: response.refreshToken,
          user: response.user
        });
        
        this.$router.push('/home');
      } catch (error) {
        console.error('Failed Registration:', error);
      }
    }
  }
};
</script>

<style scoped>
.register {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}
</style>
