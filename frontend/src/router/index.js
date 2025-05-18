import { createRouter, createWebHistory } from 'vue-router'
import { setupAuthGuard } from './authGuard'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomePage.vue'),
    meta: { requiresAuth: true }  
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/auth/AuthForm.vue'),
    meta: { guestOnly: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

setupAuthGuard(router)

export default router