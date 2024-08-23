import Vue from 'vue';
import Router from 'vue-router';

import Login from '@/components/LoginPage.vue'
import Home from '@/components/HomePage.vue'
import File from '@/components/FilePage.vue'
import FileShare from '@/components/FileSharePage.vue'
import Cache from '@/components/CachePage.vue'
import Logout from '@/components/LogoutPage.vue'
import NotFound from '@/components/NotFoundPage.vue'
import FileExtraction from '@/components/FileExtraction.vue'
import { checkAuthorizaion } from '@/authorize';
Vue.use(Router);

const router = new Router({
  mode: 'history',
  base: process.env.VUE_APP_BASE_URL,

  routes: [
    {
        path: "/",
        name: "Index",
        redirect: "/home",
    },
    {
        path: "/home",
        name: "Home",
        component: Home,
    },
    {
        path:"/login",
        name: "Login",
        component: Login
    },
    {
        path:"/article",
        name: "Article",
        meta: { requiresAuth: true },
        component: () => import('@/components/ArticlePage.vue')
    },
    {
        path:"/new-article",
        name: "NewArticle",
        meta: { requiresAuth: true },
        component: () => import('@/components/NewArticlePage.vue')
    },
    {
       path: "/blog",
       name: "Blog",
       meta: { requiresAuth: true },
       component: () => import('@/components/BlogPage.vue')
    },
    {
        path:"/about",
        name: "About",
        component: () => import('@/components/AboutPage.vue')
    },
    {
        path:"/file",
        name: "File",
        meta: { requiresAuth: true },
        component: File
    },
    {
        path:"/fileshare",
        name: "FileShare",
        meta: { requiresAuth: true },
        component: FileShare
    },
    {
        path:"/fileextraction",
        name: "FileExtraction",
        component:FileExtraction
    },
    {
        path:"/cache",
        name: "Cache",
        meta: { requiresAuth: true },
        component: Cache
    },
    {
        path:"/logout",
        name: "Logout",
        component: Logout
    },
    {
      path: '*',
      component: NotFound
    }

  ]
});


router.push = new Proxy(router.push, {
  apply(target, thisArg, args) {
    return target.apply(thisArg, args).catch(error => {
      if (error.name === 'NavigationDuplicated') {
        console.log('重复导航到当前位置:', args[0].path);
      } else {
        throw error;
      }
    });
  }
});

router.beforeEach((to, from, next) => {
  from;
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const isAuthenticated = checkAuthorizaion()

  if (requiresAuth && !isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } });
  } else {
    next()
  }
  
})
// 全局后置钩子

router.afterEach((to, from) => {
    to;
    from;
});
export default router;