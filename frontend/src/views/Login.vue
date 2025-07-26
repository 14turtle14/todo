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
        <h6>not a member?</h6>
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
  width: 350px;
  height: 450px;
  margin: auto;
  padding: 2rem;
  border-radius: 40px;
  background-color: #161616;
}

.login-button {
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
  border: 2px solid #40C9A286;
  background-clip: padding-box;
}

.login-button:hover {
  background-color: #161616;
}

.signup-link a {
  color: #40C9A2;
  text-decoration: none;
  font-weight: bold;
  font-size: 1cap;
}

.signup-link {
  text-align: center;
  margin-top: 1.5rem;
  color: #FFFFFF;
}

.form-group{
  margin: auto;
  padding: 1.3rem;
  border: none;
}

h6 {
  margin-bottom: 0;
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

.login-form {
  margin: auto;
  padding-top: 3rem;
}
</style>
