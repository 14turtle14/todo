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

    <form @submit.prevent="handleSubmit" class="signup-form">
      <div class="form-group">
        <input 
          type="text"
          id="username"
          v-model="username" 
          placeholder="username" 
          required 
        />
      </div>
      
      <div class="form-group">
        <input 
          type="text"
          id="email"
          v-model="email" 
          placeholder="email" 
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

      <button type="submit" class="register-button">sign up</button>
    </form>
  </div>
</template>

<script>
import { useAuthStore } from '@/store/auth'

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      showPassword: false,
      hasText: false
    };
  },
  methods: {
    async handleSubmit() {
      const authStore = useAuthStore()
      await authStore.signup(
        this.username, 
        this.email, 
        this.password
      )
    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },
    handleInput() {
      this.hasText = this.password.length > 0;
    },
    goBack(){
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
.register-container {
  width: 350px;
  height: 450px;
  margin: auto;
  padding: 2rem;
  border-radius: 40px;
  background-color: #161616;
  position: relative;
  transform: translateY(20%);
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
  transition: all 0.2s;
  border-radius: 50px;
  border: 2px solid #40C9A2;
  background-clip: padding-box;
  display: block;
  margin-left: auto;
  transition: all 0.2s;
  margin-right: auto;

  &:hover {
    border-color: #40C9A286;
  }
}

.form-group{
  position: relative;
  margin: auto;
  padding: 1.3rem;
  border: none;
}

input {
    width: 95%;
    background-color: #FFFFFF;
    padding: 12px 80px;
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

    &::placeholder {
      color: #40C9A2;
      font-weight: bold;
    }
}

.signup-form{
  margin: auto;
  padding-top: 2rem;
}

.navigation-list {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.close-btn {
  cursor: pointer;
  color: white;
}

input:focus::placeholder {
  color: white;
}

.back-btn a{
  cursor: pointer;
  color: white;
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
