<template>
  <div class="home-container">
    <div class="sidebar">
      <div class="logo-container">
        <img src="/dark_theme.png" alt="Логотип" class="logo">
      </div>
      
      <div class="sidebar-content">
        <div class="menu-section">
          <h3 class="section-title">library</h3>
          <div class="menu-item">open tasks</div>
          <div class="menu-item">in progress</div>
          <div class="menu-item">finished tasks</div>
        </div>
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
        
        <div class="theme-switcher">
          <i class="fa-regular fa-sun"></i>
        </div>
        
        <button class="logout-btn" @click="handleLogout">
          <span>log out</span>
        </button>
      </div>

      <div class="content-area">
        <TargetList :targets="targets" />
      </div>
    </div>
  </div>
</template>

<script>
import TargetList from '@/components/TargetList.vue';
import api from '@/api.js';
import { useAuthStore } from '@/store/auth.js';

export default {
  components: {
    TargetList
  },
  data() {
    return {
      targets: []
    };
  },
  async created() {
    try {
      this.targets = await api.getTargets();
    } catch (error) {
      console.error('Failed to fetch targets:', error);
    }
  },
  methods: {
    async handleLogout() {
      try {
        const authStore = useAuthStore();
        await authStore.logout();
        this.$router.push('/login');
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
  width: 240px;
  background-color: #191919;
  color: #ffffff;
  display: flex;
  flex-direction: column;
}

.logo-container {
  padding: 14px;
  height: 7vh;
  border-bottom: 1px solid #1e1e1e;
  display: flex;
}

.logo {
  height: 70px;
  width: auto;
  align-self: flex-start;
}

.sidebar-content {
  padding: 16px;
  flex-grow: 1;
}

.menu-section {
  margin-bottom: 32px;
}

.section-title {
  font-size: 12px;
  text-transform: uppercase;
  color: #40C9A2;
  letter-spacing: 1px;
  margin-bottom: 12px;
  padding-left: 8px;
}

.menu-item {
  padding: 10px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-bottom: 4px;
}

.menu-item:hover {
  background-color: #2d2d2d;
  color: #40C9A2;
}

.main-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.header {
  height: 7vh;
  background-color: #161616;
  border-bottom: 1px solid #1e1e1e;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  padding: 14px;
}

.header-controls {
  display: flex;
  gap: 20px;
  align-items: flex-end;
}

.control-icon {
  font-size: 25px;
  color: #FFFFFF;
  cursor: pointer;
  border-radius: 50%;
  transition: all 0.2s;
}
.theme-switcher {
  font-size: 25px;
  color: #FFFFFF;
  cursor: pointer;
}

.logout-btn {
  align-items: center;
  background: none;
  cursor: pointer;
  font-size: 14px;
  transition: color 0.2s;
  width: auto;
  padding: 8px 40px;
  color: #FFFFFF;
  font-weight: bold;
  border-radius: 50px;
  border: 2px solid #40C9A2;
  background-clip: padding-box;
  display: block;
}

.content-area {
  flex-grow: 1;
  padding: 24px;
  background-color: #161616;
  overflow-y: auto;
}
</style>