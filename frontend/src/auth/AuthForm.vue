<template>
  <form @submit.prevent="handleSubmit" class="auth-form">
    <h2>{{ isLoginMode ? 'Вход' : 'Регистрация' }}</h2>
    
    <div v-if="!isLoginMode" class="form-group">
      <label>Имя</label>
      <input v-model="formData.name" type="text" required>
    </div>

    <div class="form-group">
      <label>Email</label>
      <input v-model="formData.email" type="email" required>
    </div>

    <div class="form-group">
      <label>Пароль</label>
      <input v-model="formData.password" type="password" required minlength="6">
    </div>

    <button type="submit" :disabled="isLoading">
      {{ isLoading ? 'Загрузка...' : isLoginMode ? 'Войти' : 'Зарегистрироваться' }}
    </button>

    <p class="toggle-mode" @click="toggleMode">
      {{ isLoginMode ? 'Нет аккаунта? Создать' : 'Уже есть аккаунт? Войти' }}
    </p>

    <div v-if="error" class="error-message">{{ error }}</div>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'

const { login, register } = useAuthStore()

const isLoginMode = ref(true)
const isLoading = ref(false)
const error = ref('')

const formData = ref({
  name: '',
  email: '',
  password: ''
})

const toggleMode = () => {
  isLoginMode.value = !isLoginMode.value
  error.value = ''
}

const handleSubmit = async () => {
  try {
    isLoading.value = true
    error.value = ''
    
    if (isLoginMode.value) {
      await login(formData.value)
    } else {
      await register(formData.value)
    }
    
    window.location.href = '/'
  } catch (err) {
    error.value = err.message || 'Ошибка авторизации'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.auth-form {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

button {
  width: 100%;
  padding: 0.75rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

button:disabled {
  background-color: #cccccc;
}

.toggle-mode {
  margin-top: 1rem;
  text-align: center;
  color: #42b983;
  cursor: pointer;
}

.error-message {
  margin-top: 1rem;
  color: #ff4444;
  text-align: center;
}
</style>