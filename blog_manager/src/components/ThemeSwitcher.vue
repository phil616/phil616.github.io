<template>
    <div>
  
    <v-btn     
    color="primary"
    dark
     @click="switchTheme">
        <svg-icon type="mdi" :path="path"></svg-icon>
    </v-btn>
  </div>
  </template>
  
  <script>
  import SvgIcon from '@jamescoyle/vue-icon';
  import { mdiThemeLightDark } from '@mdi/js';
  
  export default {
    name: "ThemeSwithcer",
    components: {
      SvgIcon
    },
    data() {
      return {
         path: mdiThemeLightDark,
      }
    },
    methods: {
      switchTheme() {
          this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
          }
      }
  }
  </script>
  