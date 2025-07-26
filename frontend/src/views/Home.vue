<template>
  <div class="sidebar">
    <div class="logo-png">
      <img src="/dark_theme.png" alt="Логотип" class="form-logo">
    </div>
    
      <div class="personal-list">
        <h3>personal</h3>
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

  <div class="main-content">
    <div class="header">

      <div class="header-list">
        <div class="targets"></div>
        <div class="profile"></div>
        <div class="calendar"></div>
      </div>

      <div class="theme"></div>
      <div class="theme">log out</div>
    </div>

    <div class="targets-list">
    </div>

    <div class="create-target">

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

</style>