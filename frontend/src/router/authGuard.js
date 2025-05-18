import { useAuthStore } from '@/stores/authStore'

export function setupAuthGuard(router) {
  router.beforeEach((to) => {
    const authStore = useAuthStore()
    
    if (to.meta.requiresAuth && !authStore.token) {
      return { name: 'Login', query: { redirect: to.fullPath } }
    }
    
    if (to.meta.guestOnly && authStore.token) {
      return { name: 'Home' }
    }
  })
}