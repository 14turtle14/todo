<template>
  <div class="register-container">

    <div class="navigation-list">

      <div class = "back-btn" @click="goBack">
        <router-link to="/login">
          <i class="fas fa-arrow-left"></i>
        </router-link>
      </div>
      <div class = "close-btn" @click="closeForm">
        <i class="fas fa-times"></i>
      </div>
    </div>

    <form @submit.prevent="register" class="signup-form">

      <div class="form-group">
        <input 
          type="username"
          v-model="username" 
          placeholder="username" 
          required 
        />
      </div>
      
      <div class="form-group">
        <input 
          type="email"
          v-model="email" 
          placeholder="email" 
          required 
        />
      </div>

      <div class="form-group">
        <input 
          type="password"
          v-model="password" 
          placeholder="password" 
          required 
        />
      </div>

      <button type="submit" class="register-button">sign up</button>
    </form>
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

.form-group{
  margin: auto;
  padding: 1.3rem;
  border: none;
}

input {
    width: auto;
    background-color: #FFFFFF;
    padding: 12px 80px;
    border-radius: 10px;
    font-size: 16px;
    transition: all 0.3s;
    border: none;
    text-align: left;
    font-weight: bold;
    padding-left: 10px;
    outline: none;
    color: #40C9A2;

    &::placeholder {
      color: #40C9A2;
      font-weight: bold;
    }
}

.register-container {
  width: 350px;
  height: 450px;
  margin: auto;
  padding: 2rem;
  border-radius: 40px;
  background-color: #161616;
}

.register-button{
  width: auto;
  padding: 8px 40px;
  background-color: #161616;
  color: white;
  border-radius: 4px;
  font-size: 1cap;
  cursor: pointer;
  font-weight: bold;
  margin-top: 3rem;
  margin-bottom: 2rem;
  border-radius: 50px;
  border: 2px solid #40C9A2;
  background-clip: padding-box;
}

.signup-form{
  margin: auto;
  padding-top: 2rem;
}

.navigation-list {
  top: 15px;
  width: 20px;
  height: 20px;
  display: flex;
  cursor: pointer;
  color: white;
  transition: all 0.3s ease;
  font-size: 16px;
  border-radius: 50%;
  gap: 326px;
}

.fas {
  color: white;
}

</style>
