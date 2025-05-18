<template>
  <form @submit.prevent="$emit('submit', formData)">
    <input v-model="formData.title" placeholder="Название таргета">
    <button type="submit">Создать</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'

const formData = ref({
  title: ''
})
</script>