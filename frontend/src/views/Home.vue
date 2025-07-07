<template>
  <div class="home">
    <div class="profile-button">
      <router-link to="/profile">Profile</router-link>
    </div>
    <h2>Targets</h2>
    <TargetList :targets="targets" />
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
.dashboard {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.profile-button {
  margin-bottom: 20px;
}

.targets {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.target {
  margin: 10px;
  padding: 10px;
  border: 1px solid #ccc;
}
</style>
