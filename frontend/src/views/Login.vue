<template>
  <div class="login-container">
    <div class="navigation-list">
      <div class = "logo">
        <img src="/dark_theme.png" 
        alt="Логотип" 
        class="form-logo">
      </div>
      <div class = "close-btn" @click="closeForm">
        <i class="fas fa-times"></i>
      </div>
    </div>

    <form @submit.prevent="login" class="login-form">
      
      <div class="form-group">
        <input
          type="username"
          id="username"
          v-model="username"
          placeholder="username"
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
    </form>
      <div class="signup-link">
        <h6>not a member?</h6>
        <router-link to="/signup">sign up now</router-link>
      </div>
  </div>
</template>

<script>
import api from '@/api.js';
import {useAuthStore} from '@/store/auth.js'
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
        const authStore = useAuthStore();
        const response = await api.login(this.username, this.password);

        authStore.setAuthData({
          token: response.accessToken,
          user: response.user
        });

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
  border: 2px solid #40C9A2;
  background-clip: padding-box;
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

.navigation-list {
  top: 15px;
  width: 20px;
  height: 20px;
  display: flex;
  color: white;
  transition: all 0.3s ease;
  font-size: 16px;
  border-radius: 50%;
  gap: 300px;
}

.close-btn{
  cursor: pointer;
}
.form-logo{
  position: relative;
  width: 40px;
  height: 40px;
  display: block;
  margin: 0 auto 20px;
}

</style>