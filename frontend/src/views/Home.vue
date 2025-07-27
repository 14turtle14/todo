<template>
  <div class="home-container">
    <div class="sidebar">
      <div class="logo-png">
        <img src="/dark_theme.png" alt="Логотип" class="form-logo">
      </div>
      <div class="sidebar-lists">
        <div class="personal-list">
          <h3>personal</h3>
          <i class="fas fa-sun sun"></i> <!-- Солнце -->
          <i class="fas fa-moon moon"></i> <!-- Месяц -->
          <div class="sidebar-item">notes</div>
          <div class="sidebar-item">planner</div>
        </div>
        <div class="library-list">
          <h3>library</h3>
          <div class="sidebar-item">open tasks</div>
          <div class="sidebar-item">in progress</div>
          <div class="sidebar-item">finished tasks</div>
        </div>
      </div>
    </div>
    <div class="main-content">
      <div class="header">
        <div class="header-list">
          <div class="targets"></div>
          <div class="profile"></div>
          <div class="calendar"></div>
        </div>
        <div class="theme"></div>
        <div class="log-out">log out</div>
      </div>
      <div class="targets-content">
        <h3>targets</h3>
        <div class="targets-list">
        </div>
        <div class="create-target">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TargetList from '@/components/TargetList.vue';
import api from '@/api.js';
export default {
    components:
    {   
        TargetList
    },
    data() {
        return {
            targets: []
        };
    },
    async created() {
        try{
            this.targets = await api.getTargets();
        } catch (error) {
            console.error('Failed to fetch targets:', error)
        }
    }
};
</script>

<style scoped>

.form-logo {
  height: 10vh;
  width: 5vw;
  padding-right: 15rem;
}

.home-container{
  display: flex; 
  width: 100vw;
  height: 100vh;
}

.logo-png{
  width: 20vw;
  height: 10vh;
  background: blue;
}

.header{
  width: 80vw;
  height: 10vh;
  background: yellow;
}

.sidebar-lists{
  background: red;
  height: 90vh;
}

.targets-content{
  background: green;
  height: 90vh;
  
}

</style>