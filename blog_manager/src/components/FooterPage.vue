
<template>
    <v-footer app>
      <v-container flex>
        <v-row justify="center">
          <v-col class="text-center">
            <p>&copy; {{ new Date().getFullYear() }} Blog Mananger Powered by Vue.js<br>
            phil616 All Rights Reserved</p>
          </v-col>
        </v-row>
      </v-container>
    </v-footer>
</template>

<script>
export default {
  name: 'FooterPage',
};
</script>

<style scoped>
/* 你可以在这里添加自定义样式 */
</style>
