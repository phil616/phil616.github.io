<template>
  <v-container fluid>
    <v-snackbar v-model="snackbar" :timeout="timeout">
      {{ message }}
      <template v-slot:action="{ attrs }">
        <v-btn color="pink" text v-bind="attrs" @click="snackbar = false">
          关闭
        </v-btn>
      </template>
    </v-snackbar>
    <v-row justify="center" style="margin-top: 1%;">
      <v-alert type="warning" text prominent border="left" v-if="loggedIn">
      该网站已经登录，可以通过重新登陆来更新用户信息
      </v-alert>
    </v-row>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>登录</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form ref="form" v-model="valid" lazy-validation>
              <v-text-field
                v-model="email"
                :rules="emailRules"
                label="邮箱"
                required
                prepend-icon="mdi-email"
              ></v-text-field>
              <v-text-field
                v-model="password"
                :rules="passwordRules"
                label="密码"
                required
                prepend-icon="mdi-lock"
                type="password"
              ></v-text-field>
              <v-checkbox
                v-model="rememberMe"
                label="记住我"
              ></v-checkbox>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn text color="primary" @click="register">用户注册</v-btn>
            <v-spacer></v-spacer>
            <v-btn text color="primary" @click="forgotPassword">忘记密码</v-btn>
            <v-spacer></v-spacer>
            <v-btn color="primary" :disabled="!valid" @click="submit">登录</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      
    </v-row>

  </v-container>
</template>
<script>
import Cookies from 'js-cookie';
import http from '@/http'
import { checkAuthorizaion } from '@/authorize';
export default {
  data: () => ({
    loggedIn: false,
    snackbar: false,
    message: '',
    timeout: 5000,
    valid: true,
    email: '',
    emailRules: [
      v => !!v || '邮箱是必填项',
      v => /.+@.+\..+/.test(v) || '邮箱格式不正确',
    ],
    password: '',
    passwordRules: [
      v => !!v || '密码是必填项',
      v => (v && v.length >= 6) || '密码至少6个字符',
    ],
    rememberMe: false,
  }),
  methods: {
    submit() {
      if (this.$refs.form.validate()) {
        http.post('/login/user',{ username: this.email, password: this.password },
          { headers: { 'Content-Type': 'application/json' } }
        ).then(response => {
          if (response.status == 200) {
            let token = response.data.token;
            Cookies.set('token',token)
            this.$router.push(this.$route.query.redirect || '/')
          } else {
            this.showSnackbar("登录失败"+response.status+" "+response.data);
          }
        }).catch(error => { 
          this.showSnackbar("登录失败"+error); 
        });
        if (this.rememberMe) {
          localStorage.setItem('email', this.email);
          localStorage.setItem('password', this.password);
        }
      }
    },
    showSnackbar(message = 'Login error', timeout = 5000) {
      this.message = message;
      this.timeout = timeout;
      this.snackbar = true;
    },
    register() {
      this.showSnackbar("应用不支持注册");
    },
    forgotPassword() {
      // 跳转到忘记密码页面
      this.showSnackbar("应用不支持忘记密码");
    },
    autoFillCredentials() {
      const storedEmail = localStorage.getItem('email');
      const storedPassword = localStorage.getItem('password');

      if (storedEmail && storedPassword) {
        this.email = storedEmail;
        this.password = storedPassword;
        this.rememberMe = true;
      }
    },
  },
  mounted() {
    this.autoFillCredentials();
    if (checkAuthorizaion()){
      this.loggedIn = true;
    }
  },
};
</script>
