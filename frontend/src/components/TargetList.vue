<template>
  <div class="targets-container">

    <draggable 
      :list="internalTargets" 
      group="targets" 
      item-key="id"
      class="targets-list"
      @end="onDragEnd"
    >
      <template #item="{ element: target }">
        <div class="target">
          <div class="target-header">
            <span class="target-title">{{ target.title }}</span>
            <span
            v-if="hasTasks(target)"
            class="progress-badge"
            >
              {{ completedTasksCount(target) }}/{{ target.tasks.length }}
            </span>
          </div>

          <div 
            v-if="hasPriorityTasks(target)" 
            class="priority-tasks"
          >
            <div 
              v-for="task in priorityTasks(target)" 
              :key="task.id"
              class="priority-task"
              :class="{ 'completed': task.completed }"
            >
              {{ task.title }}
            </div>
          </div>
        </div>
      </template>
    </draggable>
  </div>
</template>

<script>
import { VueDraggableNext } from 'vue-draggable-next'

export default {
  components: {
    draggable: VueDraggableNext
  },
  props: {
    targets: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      internalTargets: [...this.targets] 
    }
  },
  watch: {
    targets(newVal) {
      this.internalTargets = [...newVal] 
    }
  },
  methods: {
    hasTasks(target) {
      return target.tasks && target.tasks.length > 0
    },
    completedTasksCount(target) {
      return this.hasTasks(target) ? target.tasks.filter(t => t.completed).length : 0
    },
    hasPriorityTasks(target) {
      return this.hasTasks(target) && target.tasks.some(t => t.priority)
    },
    priorityTasks(target) {
      return this.hasTasks(target) ? target.tasks.filter(t => t.priority) : []
    },
    onDragEnd() {
      this.$emit('update:targets', [...this.internalTargets])
    }
  }
}
</script>

<style scoped>
.targets-container {
  padding: 20px;
  min-height: 200px;
}

.empty-state {  
  color: #666;
  text-align: center;
  padding: 40px;
  font-style: italic;
}

.targets-list {
  display: grid;
  gap: 15px;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

.target {
  background: #2a2a2a;
  border-radius: 8px;
  padding: 15px;
  cursor: grab;
  transition: transform 0.2s;
}

.target:active {
  cursor: grabbing;
}

.target:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.target-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.target-title {
  font-weight: bold;
  font-size: 16px;
  color: #fff;
}

.progress-badge {
  background: #40C9A2;
  color: #161616;
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
}

.priority-tasks {
  margin-top: 10px;
  border-top: 1px solid #3a3a3a;
  padding-top: 10px;
}

.priority-task {
  font-size: 14px;
  padding: 5px 0;
  color: #ddd;
  position: relative;
  padding-left: 15px;
}

.priority-task:before {
  content: "•";
  color: #40C9A2;
  position: absolute;
  left: 0;
}

.priority-task.completed {
  text-decoration: line-through;
  color: #777;
}
</style>