import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/store/auth.js'
import Login from '@/views/Login.vue';
import Register from '@/views/Register.vue';
import Home from '@/views/Home.vue';
import Profile from '@/views/Profile.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
  {
    path: '/',
    redirect: (to) => {
      const authStore = useAuthStore;
      return authStore.isAuthenticated ? '/home' : '/login';
  }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { guestOnly: true }
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Register,
    meta: { guestOnly: true }
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    //meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    //meta: { requiresAuth: true }
  }
]
});

router.beforeEach(async (to) => {
  const authStore = useAuthStore();
  
  if (to.name === 'Login') return true;

  try {
    const isValid = await authStore.checkTokenExpiration();
    
    if (to.meta.requiresAuth && !isValid) {
      return { name: 'Login' };
    }
    
    if (to.meta.guestOnly && isValid) {
      return { name: 'Home' };
    }
    
    return true;
  } catch (error) {
    authStore.clearAuthData();
    return { name: 'Login' };
  }
});


export default router;
