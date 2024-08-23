<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <v-app-bar-nav-icon @click="drawerSwitch =!drawerSwitch" />
      <v-spacer />
      <ThemeSwitcher />
    </v-app-bar>
          
    <v-navigation-drawer 
        v-model="drawerSwitch"
        app
        temporary
        clipped
        height="100rm"
      >
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="text-h6">
            文章后台管理
          </v-list-item-title>
          <v-list-item-subtitle>
            博客与文章后台管理
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>
      <v-list-item-content>
          <v-list-item-title>

            <v-btn @click="drawerSwitch = false">
              <v-icon>mdi-arrow-left</v-icon>
              收起
            </v-btn>
            
          </v-list-item-title>
        </v-list-item-content>
      <v-divider></v-divider>

      <v-list
        dense
        nav
      >
        <v-list-item
          v-for="item in items"
          :key="item.title"
          link
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title @click="linkto(item.link)">{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    
    <v-main>
      <router-view />
    </v-main>
      <FooterPage />
  </v-app>
</template>

<script>
import { logout } from './authorize';
import FooterPage from '@/components/FooterPage';
import ThemeSwitcher from '@/components/ThemeSwitcher';
export default {
  name: 'App',

  components: {
    FooterPage,ThemeSwitcher
  },

  data: () => ({
    drawerSwitch: false,
    items: [
      { title: '主页', link: '/', icon:'mdi-home' },
      { title: '博客管理', link: '/blog', icon:'mdi-book-open-page-variant'},
      { title: '文章', link: '/article', icon:'mdi-newspaper' },
      { title: '文件管理', link: '/file', icon:'mdi-tag' },
      { title: '文件提取', link: '/fileextraction', icon:'mdi-file-tree' },
      { title: '系统配置缓存', link: '/cache', icon:'mdi-cached' },
      { title: '登录', link: '/login', icon:'mdi-login' },
      { title: '登出', link: '/logout', icon:'mdi-logout' },
      { title: '关于', link: '/about', icon:'mdi-information' },
    ],
  }),
  methods: {
    linkto(link) {
      this.$router.replace({path: link});
      this.drawerSwitch = false;
    },
    quit() {
      logout();
    }
  }
};
</script>
