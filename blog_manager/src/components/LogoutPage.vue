<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card>
          <v-card-title class="headline">登出</v-card-title>
          <v-card-text>
            <p>您将在 {{ countdown }} 秒后自动登出。</p>
            <v-btn color="error" @click="logoutNow">立即登出</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import {logout} from '@/authorize'
export default {
  data() {
    return {
      countdown: 5,
      timer: null
    };
  },
  mounted() {
    this.startCountdown();
  },
  methods: {
    startCountdown() {
      this.timer = setInterval(() => {
        if (this.countdown > 0) {
          this.countdown--;
        } else {
          this.signout();
        }
      }, 1000);
    },
    signout() {
      clearInterval(this.timer);
      logout()
      this.$router.push('/login');
    },
    logoutNow() {
      this.signout();
    }
  },
  beforeDestroy() {
    clearInterval(this.timer);
  }
};
</script>

<style scoped>
/* 你可以在这里添加一些样式 */
</style>
