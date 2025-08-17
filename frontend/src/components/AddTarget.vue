<template>
  <div class="target-creator">
    <div class="compact-form" v-if="!expanded">
      <div class="input-container">
        <input 
          type="text" 
          v-model="targetData.title" 
          placeholder="target title"
          class="rounded-input"
          @keyup.enter="createTarget"
          maxlength="32"
        >
        <div class="divider"></div>
      </div>
      
      <div class="form-group">
        <select v-model="targetData.type" @change="handleTypeChange" class="custom-select">
          <option value="" disabled selected hidden>target type</option>
          <option value="default">default</option>
          <option value="periodic">periodic</option>
          <option value="expirable">expirable</option>
        </select>
        <div class="divider"></div>
      </div>

      <div class="form-group" v-if="showPeriodField">
        <select v-model="targetData.intervalDays" class="custom-select">
          <option v-for="day in 14" :value="day" :key="day">
            every {{ day }} day{{ day > 1 ? 's' : '' }}
          </option>
        </select>
        <div class="divider"></div>
      </div>

      <div class="form-group" v-if="showDeadlineField">
        <input
          type="date"
          v-model="targetData.deadline"
          :min="minDate"
          :max="maxDate"
          class="date-input"
        >
        <div class="divider"></div>
      </div>

      <button class="expand-btn" @click="createTarget">
        <img src="/plus_b.png" alt="Add" class="plus">
      </button>
    </div>
  </div>
</template>

<script>
import api from '@/api.js';
export default {
  data() {
    const today = new Date();
    const sixMonthsLater = new Date();
    sixMonthsLater.setMonth(today.getMonth() + 6);
    
    return {
      expanded: false,
      targetData: {
        title: '',
        type: '',
        intervalDays: '',
        deadline: ''
      },
      minDate: today.toISOString().split('T')[0],
      maxDate: sixMonthsLater.toISOString().split('T')[0]
    }
  },
  computed: {
    showPeriodField() {
      return this.targetData.type === 'periodic';
    },
    showDeadlineField() {
      return this.targetData.type === 'expirable';
    }
  },
  methods: {
    handleTypeChange() {
      this.targetData.intervalDays = '1';
      this.targetData.deadline = '';
    },
    createTarget() {
      if (!this.targetData.title || !this.targetData.type) {
        alert('Please fill all required fields');
        return;
      }
      
      const target = { ...this.targetData };
      
      if (target.type !== 'periodic') delete target.intervalDays;
      if (target.type !== 'expirable') delete target.deadline;

      api.createTarget(this.targetData.title, this.targetData.type, this.targetData.deadline, this.targetData.intervalDays)
      
      console.log('Target created:', target);
      this.$emit('target-created', target);
      
      this.targetData = {
        title: '',
        type: '',
        intervalDays: '',
        deadline: ''
      };
    }
  }
}
</script>

<style scoped>
.target-creator {
  background-color: #161616;
  justify-content: center; 
  display: flex;
}

.compact-form {
  display: flex;
  align-items: center;
  background-color: #1e1e1e;
  border-radius: 20px;
  padding: 8px 20px;
  transition: all 0.2s ease;
  margin-bottom: 40px;
  width: 600px;
  min-width: 500px;
  height: auto;
  min-height: 50px;
  justify-items: center;
  margin-right: 200px;
}

.rounded-input {
  background: transparent;
  border: none;
  color: white;
  font-weight: bold;
  padding: 6px 0;
  outline: none;
  font-size: 14px;
  width: 100%;
}

input::placeholder {
  color: white;
  font-weight: bold;
}

.input-container {
  position: relative;
  margin: 10px 15px;
  width: 60%;
}

.divider {
  height: 2px;
  background-color: #40C9A2;
  margin-top: 4px;
  margin-bottom: 4px;
  opacity: 0.7;
}

.expand-btn {
  background: #1e1e1e;
  border: none;
  width: 40px;
  height: 40px;
  cursor: pointer;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s;
  margin-left: 10px;

  &:hover {
    transform: scale(1.1);
  }
}

.plus {
  width: 40px;
  height: 40px;
}

.custom-select {
  flex-grow: 1;
  background: transparent;
  border: none;
  color: white;
  font-weight: bold;
  padding: 6px 25px 6px 0;
  outline: none;
  font-size: 14px;
  width: 100%;
  background-repeat: no-repeat;
  background-position: right center;  
  background-size: 12px;
  cursor: pointer;
}

.date-input {
  background: transparent;
  border: none;
  color: white;
  font-weight: bold;
  padding: 6px 0;
  outline: none;
  font-size: 14px;
  width: 100%;
  appearance: none;
}

.date-input::-webkit-calendar-picker-indicator {
  color: white;
  cursor: pointer;
}

.date-input::-webkit-datetime-edit-fields-wrapper {
  opacity: 1;
}

.form-group {
  flex-grow: 1;
  position: relative;
  margin: 10px 15px;
  width: auto;
}

input:focus::placeholder {
  color: #1e1e1e
}
</style>