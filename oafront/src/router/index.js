import { createRouter, createWebHashHistory } from 'vue-router'
import login from '@/views/login/login.vue';
import frame from '@/views/main/frame.vue';
import myabsent from '@/views/absent/my.vue';
import subabsent from '@/views/absent/sub.vue';
import { useAuthStore } from '@/stores/auth';
import inform_detail from '@/views/inform/detail.vue';
import inform_publish from '@/views/inform/publish.vue';
import inform_list from '@/views/inform/list.vue';

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'frame',
      component: frame,
      children:[
        {path:'absent/my', name:'myabsent', component: myabsent},
        {path:'absent/sub', name:'subabsent', component: subabsent},
        {path:'absent/publish', name:'inform_publish', component: inform_publish},
        {path:'absent/list', name:'inform_list', component: inform_list},
        {path:'absent/detail/:pk', name:'inform_detail', component: inform_detail},
      ]
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
