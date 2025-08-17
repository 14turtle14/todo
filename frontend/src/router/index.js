import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/store/auth.js';
import Login from '@/views/Login.vue';
import Signup from '@/views/Signup.vue';
import Home from '@/views/Home.vue';
import Profile from '@/views/Profile.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: (to) => {
        const authStore = useAuthStore();
        return authStore.isAuthenticated ? '/home' : '/login';
      }
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: { 
        guestOnly: true,
        title: 'Login' 
      }
    },
    {
      path: '/signup',
      name: 'Signup',
      component: Signup,
      meta: { 
        guestOnly: true,
        title: 'Sign Up' 
      }
    },
    {
      path: '/home',
      name: 'Home',
      component: Home,
      meta: { 
        requiresAuth: true,
        title: 'Home' 
      }
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile,
      meta: { 
        requiresAuth: true,
        title: 'Profile' 
      }
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ]
});

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  

  document.title = to.meta.title || 'To Do';

  if (!to.meta.requiresAuth && !to.meta.guestOnly) {
    return next();
  }

  try {
    if (authStore.isAuthenticated) {
      const isValid = await authStore.checkTokenExpiration();
      
      if (!isValid && to.meta.requiresAuth) {
        return next({ name: 'Login' });
      }
      
      if (isValid && to.meta.guestOnly) {
        return next({ name: 'Home' });
      }
    } else {
      if (to.meta.requiresAuth) {
        return next({ name: 'Login' });
      }
    }

    return next();
  } catch (error) {
    console.error('Router navigation error:', error);
    authStore.clearAuthData();
    return next({ name: 'Login' });
  }
});

export default router;