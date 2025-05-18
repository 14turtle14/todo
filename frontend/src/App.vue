<template>
  <div class="app-container">
    <header class="app-header">
      <nav class="main-nav">
        <router-link to="/" class="logo">MyTargetApp</router-link>
        <div class="nav-right">
          <button @click="showTargetModal = true" class="create-target-btn">
            <i class="fas fa-plus"></i> Создать таргет
          </button>
          <div class="user-profile" @click="toggleProfileDropdown">
            <img :src="user.avatar" alt="Profile" class="profile-avatar">
            <span class="profile-name">{{ user.name }}</span>
            <i class="fas fa-chevron-down"></i>
            
            <div v-if="isProfileDropdownOpen" class="profile-dropdown">
              <router-link to="/profile" class="dropdown-item">
                <i class="fas fa-user"></i> Профиль
              </router-link>
              <button @click="logout" class="dropdown-item">
                <i class="fas fa-sign-out-alt"></i> Выйти
              </button>
            </div>
          </div>
        </div>
      </nav>
    </header>

    <main class="app-main">
      <router-view />
    </main>

    <modal v-if="showTargetModal" @close="showTargetModal = false">
      <h3>Создать новый таргет</h3>
      <target-form @submit="handleTargetCreate" />
    </modal>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'
import Modal from '@/components/Modal.vue'
import TargetForm from '@/components/TargetForm.vue'

const authStore = useAuthStore()
const router = useRouter()

const user = ref({})

const isProfileDropdownOpen = ref(false)
const showTargetModal = ref(false)

const toggleProfileDropdown = () => {
  isProfileDropdownOpen.value = !isProfileDropdownOpen.value
}

const logout = () => {
  authStore.logout()
  router.push('/login')
}

const handleTargetCreate = (targetData) => {
  console.log('Создаем таргет:', targetData)
  showTargetModal.value = false
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: linear-gradient(135deg, #6e8efb, #a777e3);
  color: white;
  padding: 0 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.main-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
  max-width: 1200px;
  margin: 0 auto;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  text-decoration: none;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.create-target-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background-color 0.3s;
}

.create-target-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.user-profile {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 30px;
  transition: background-color 0.3s;
}

.user-profile:hover {
  background: rgba(255, 255, 255, 0.1);
}

.profile-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
}

.profile-name {
  font-weight: 500;
}

.profile-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 0.5rem 0;
  min-width: 180px;
  z-index: 100;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  width: 100%;
  text-align: left;
  background: none;
  border: none;
  color: #333;
  cursor: pointer;
  transition: background-color 0.2s;
}

.dropdown-item:hover {
  background: #f5f5f5;
}

.app-main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}
</style>