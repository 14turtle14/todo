<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const currentTime = ref(new Date());

const formatTime = (date) => {
  return date.toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const startMinuteSync = () => {
  let timerId;
  
  const update = () => {
    const now = new Date();
    currentTime.value = now;
    
    const delay = (60 - now.getSeconds()) * 1000;
    
    timerId = setTimeout(() => {
      update();
    }, delay);
  };

  update();

  onUnmounted(() => {
    clearTimeout(timerId);
  });
};

onMounted(startMinuteSync);
</script>

<template>
  <div class="time-display">
    {{ formatTime(currentTime) }}
  </div>
</template>

<style scoped>
.time-display {
  font-size: 1rem;
  font-weight: bold;
  position: fixed;
  bottom: 60px;
  left: 8.5%;
  transform: translateX(-50%);
}
</style>