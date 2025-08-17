<template>
  <div class="home-container">
    <div class="sidebar">
      <div class="logo-container">
        <img src="/dark_theme.png" alt="Логотип" class="logo">
      </div>
      
      <div class="sidebar-content">
        <div class="menu-section">
          <h3 class="section-title">Targets</h3>
          <div class="section-list">
            <button class="menu-item" @click="">default</button>
            <button class="menu-item" @click="">periodic</button>
            <button class="menu-item" @click="">expirable</button>
          </div>
        </div>
        <TimeDisplay />
      </div>
    </div>

    <div class="main-content">
      <div class="header">
        <div class="header-controls">
          <div class="control-icon">
            <i class="fa-regular fa-circle-dot"></i>
          </div>
          <div class="control-icon">
            <i class="fa-regular fa-circle-user"></i>
          </div>
          <div class="control-icon">
            <i class="fa-regular fa-calendar-days"></i>
          </div>
        </div>
        <div class="right-controls">
          <div class="theme-switcher">
          <i class="fa-regular fa-sun"></i>
          </div>

          <button class="logout-btn" @click="handleLogout">
          <span class="logout-btn-text">log out</span>
          </button>
        </div>
      </div>

      <div class="content-area">
        <TargetList :targets="targets" />
      </div>

      <div class="add-target">
         <AddTarget />
      </div>

    </div>
  </div>
</template>

<script>
import TargetList from '@/components/TargetList.vue';
import TimeDisplay from '@/components/TimeDisplay.vue';
import AddTarget from '@/components/AddTarget.vue';
import { useAuthStore } from '@/store/auth'
import api from '@/api.js'
import { toRaw } from 'vue'

export default { 
  components: {
    TargetList,
    TimeDisplay,
    AddTarget
  },
  data() {
    return {
      targets: []
    };
  },
  async created() {
    try {
      const response = await api.getTargets();
      const plain = toRaw(response.data)
      this.targets = plain
      console.log('Targets data:', this.targets); // Проверяем данные
    } catch (error) {
      console.error('Failed to fetch targets:', error);
    }
  },
  methods: {
    async handleLogout() {
      const authStore = useAuthStore()
      try {
        await authStore.logout()
      } catch (error) {
        console.error('Logout failed:', error);
      }
    }
  }
};
</script>

<style scoped>

.home-container {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: 350px;
  background-color: #191919;
  color: #ffffff;
  display: flex;
  flex-direction: column;
}

.logo-container {
  padding: 14px;
  height: 5vh;
  border-bottom: 1px solid #1e1e1e;
  display: flex;
}

.logo {
  height: 60px;
  width: auto;
  align-self: flex-start;
}

.sidebar-content {
  padding: 16px;
  flex-grow: 1;
}

.menu-section {
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  transform: translateY(50%); 
}

.section-title {
  font-weight: bold;
  text-transform: lowercase;
  color: #40C9A2;
  padding-left: 4px;
  font-size: 1.5rem;
  margin-bottom: 0.75rem;
  align-self: flex-start;
}

.section-list {
  display: flex;
  flex-direction: column;
  gap: 0.25rem; 
}

.menu-item {
  transition: all 0.2s;
  font-weight: bold;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 4px;
  background: none;
  border: none;
  color: #ffffff;
  text-align: left;
  padding: 0.5rem 0.75rem;
  padding-left: 2rem;
  font-size: 1.1rem;
  text-transform: lowercase;
}

.menu-item:hover {
  color: #40C9A2;   
}

.main-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.header {
  height: 5vh;
  background-color: #161616;
  border-bottom: 1px solid #1e1e1e;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  padding: 14px;
  position: relative; 
}

.header-controls {
  display: flex;
  align-items: flex-end;
  position: absolute;
  left: 40%;
  transform: translateX(-28%); 
  gap: 50px;
}

.right-controls {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 100px;
}

.add-target{
  background-color: #161616;
}

.control-icon {
  transition: all 0.2s;
  font-size: 25px;
  color: #FFFFFF;
  cursor: pointer;
  border-radius: 50%;
}

.control-icon:hover{ 
  color: #40C9A2;   
}

.theme-switcher {
  transition: all 0.2s;
  font-size: 25px;
  color: #FFFFFF;
  cursor: pointer;
}

.theme-switcher:hover{
  color: #40C9A2;   
}

.logout-btn {
  align-items: center;
  background: none;
  cursor: pointer;
  font-size: 0.8cap;
  font-weight: bold;
  transition: color 0.2s;
  width: auto;
  padding: 8px 30px;
  color: #FFFFFF;
  border-radius: 50px;
  border: 2px solid #40C9A2;
  background-clip: padding-box;
  display: block;
  margin-right: 20px;

  &:hover {
    border-color: #40C9A286;
  }
}

.logout-btn-text{
  font-size: 1.5cap;
}

.content-area {
  flex-grow: 1;
  padding: 24px;
  background-color: #161616;
  overflow-y: auto;
}
</style>