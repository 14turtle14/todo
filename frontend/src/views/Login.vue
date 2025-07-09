<template>
  <div class="login-container">
    <form @submit.prevent="handleSubmit" class="login-form">
      <div class="form-group">
        <input
          type="email"
          id="email"
          v-model="email"
          placeholder="email"
          required
        />
      </div>
      
      <div class="form-group">
        <input
          type="password"
          id="password"
          v-model="password"
          placeholder="password"
          required
        />
      </div>
      
      <button type="submit" class="login-button">log in</button>
      
      <div class="signup-link">
        not a member? 
        <router-link to="/signup">sign up now</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import api from '@/api.js';

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async login() {
      try{
        await api.login(this.username, this.password);
        this.$router.push('/home');
      } catch (error) {
        console.error('Login failed:', error)
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  width: 400px;
  height: 600px;
  margin: auto;
  padding: 2rem;
  border-radius: 50px;
  background-color: #161616;
}

.form-group {
  background-color: #FFFFFF;
  width: 400px;
  height: 50px;
  border-radius: 20px;
  border: 1px;
  border-color: #000000;
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #555;
}

.login-button {
  width: 100%;
  padding: 0.75rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 1rem;
}

.login-button:hover {
  background-color: #45a049;
}

.signup-link {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
}

.signup-link a {
  color: #4CAF50;
  text-decoration: none;
}

.signup-link a:hover {
  text-decoration: underline;
}
</style>
