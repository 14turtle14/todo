import { ref } from 'vue';
import axios from 'axios';

export const useAuthForm = () => {
  const email = ref('');
  const password = ref('');
  const isLoginMode = ref(true);
  const error = ref('');

  const submitForm = async () => {
    try {
      const url = isLoginMode.value ? '/token' : '/register';
      const data = {
        username: email.value,
        password: password.value,
      };
      
      const response = await axios.post('http://localhost:4014' + url, data);
      console.log('Успех!', response.data);
      
      localStorage.setItem('token', response.data.access_token);
      window.location.href = '/profile';
      
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка при авторизации';
    }
  };

  const toggleMode = () => {
    isLoginMode.value = !isLoginMode.value;
    error.value = '';
  };

  return { email, password, isLoginMode, error, submitForm, toggleMode };
};