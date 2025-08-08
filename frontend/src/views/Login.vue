<template>
  <div class="login-container">
    <div class="navigation-list">
      <div class="logo">
        <img src="/dark_theme.png" alt="Logo" class="form-logo">
      </div>
      <div class="close-btn" @click="closeForm">
        <i class="fas fa-times"></i>
      </div>
    </div>

    <form @submit.prevent="login" class="login-form">
      <div class="form-group">
        <input
          type="text"
          id="username"
          v-model="username"
          placeholder="username"
          required
        />
      </div>
      
      <div class="form-group password-group">
        <input
          :type="showPassword ? 'text' : 'password'"
          id="password"
          v-model="password"
          @input="handleInput"
          placeholder="password"
          required
        />
        <i 
          v-if="hasText"
          @click="togglePasswordVisibility"
          class="eye-icon"
          :class="showPassword ? 'fa-regular fa-eye-slash' : 'fa-regular fa-eye'"
        ></i>
      </div>
      
      <button type="submit" class="login-button">log in</button>
    </form>
    
    <div class="signup-link">
      <h6>not a member?</h6>
      <router-link to="/signup">sign up now</router-link>
    </div>
  </div>
</template>

<script>
import api from '@/api.js';
import { useAuthStore } from '@/store/auth.js'

export default {
  data() {
    return {
      username: '',
      password: '',
      showPassword: false,
      hasText: false
    };
  },
  methods: {
    async login() {
      try {
        const authStore = useAuthStore();
        const response = await api.login(this.username, this.password);

        authStore.setAuthData({
          token: response.accessToken,
          user: response.user
        });

        this.$router.push('/home');
      } catch (error) {
        console.error('Login failed:', error);
      }
    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },
    handleInput() {
      this.hasText = this.password.length > 0;
    },
    closeForm() {
      
    }
  }
};
</script>

<style scoped>
.login-container {
  width: 350px;
  height: 450px;
  margin: auto;
  padding: 2rem;
  border-radius: 40px;
  background-color: #161616;
  position: relative;
  transform: translateY(20%);
}

.login-button {
  width: auto;
  padding: 8px 40px;
  background-color: #161616;
  color: #FFFFFF;
  border-radius: 4px;
  font-size: 1cap;
  cursor: pointer;
  font-weight: bold;
  margin-top: 3rem;
  margin-bottom: 2rem;
  border-radius: 50px;
  border: 2px solid #40C9A2;
  background-clip: padding-box;
  display: block;
  margin-left: auto;
  margin-right: auto;
}

.signup-link a {
  color: #40C9A2;
  text-decoration: none;
  font-weight: bold;
  font-size: 1cap;
}

.signup-link {
  text-align: center;
  margin-top: 3.5rem;
  color: #FFFFFF;
}

.form-group {
  position: relative;
  margin: auto;
  padding: 1.3rem;
  border: none;
}

.password-group {
  position: relative;
}

h6 {
  margin-bottom: 0;
}

input {
  width: 95%;
  background-color: #FFFFFF;
  padding: 12px 20px;
  border-radius: 10px;
  font-size: 16px;
  transition: all 0.3s;
  border: none;
  text-align: left;
  font-weight: bold;
  padding-left: 10px;
  padding-right: 40px;
  outline: none;
  color: #40C9A2;
  box-sizing: border-box;
}

input::placeholder {
  color: #40C9A2;
  font-weight: bold;
}

.login-form {
  margin: auto;
  padding-top: 0.95rem;
}

.navigation-list {
  display: flex;
  justify-content: space-between;
  align-items: top;
  margin-bottom: 10px;
}

.close-btn {
  cursor: pointer;
  color: #FFFFFF;
}

.form-logo {
  width: 40px;
  height: 40px;
  display: block;
}

.eye-icon {
  position: absolute;
  right: 40px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  cursor: pointer;
  color: #40C9A2;
}
</style>