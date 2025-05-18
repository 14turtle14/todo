<template>
  <div v-if="isOpen" class="modal">
    <slot></slot>
  </div>
</template>

<script setup>
defineProps({
  isOpen: Boolean
})
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>