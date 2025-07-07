<template>
  <div class="target-list">
    <div v-for="target in targets" :key="target.id" class="target">
      {{ target.name }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'TargetList',
  props: {
    targets: {
      type: Array,
      required: true
    }
  }
};
</script>

<style scoped>
.target-list {
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
