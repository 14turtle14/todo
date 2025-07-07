<template>
  <div class="profile">
    <h2>Profile</h2>
    <p>Username: {{ username }}</p>
    <p>Email: {{ email }}</p>
    <router-link to="/home">Back to Dashboard</router-link>
  </div>
</template>

<script>
import api from '@/api.js';
export default {
  data() {
    return {
        username: '',
        email: ''
    };
  },
  async created() {
    try {
        data = await api.getUser(userId)
        this.username = data.username
        this.email = data.email
    } catch (error) {
        console.error('Failed to get user:', error)
    }
  }
};
</script>

<style scoped>
.profile {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}
</style>
