import { createRouter, createWebHashHistory } from 'vue-router'
import login from '@/views/login/login.vue';
import frame from '@/views/main/frame.vue';
import { useAuthStore } from '@/stores/auth';

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'frame',
      component: frame,
    },
    {
      path: '/login',
      name: 'login',
      component: login,
    },
  ],
})

router.beforeEach((to, from)=>{
  // 判断用户是否登录，如果没有登录，并且访问的页面不是登录页面，那么跳转到登陆页面
  const authStore = useAuthStore()
  if(!authStore.is_logined && to.name!='login'){
    return {name:'login'}
  }
})

export default router
