<template>
    <v-container  fluid>
      <v-row align="center" justify="center">
        <v-col cols="12" sm="8" md="6">
          <v-card class="elevation-12">
            <v-toolbar color="primary" dark>
              <v-toolbar-title>404 - Page Not Found</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12">
                    <h2 class="headline mb-3">Oops! The page you're looking for could not be found.</h2>
                    <p>The requested URL <strong>{{ $route.path }}</strong> was not found on this server.</p>
                    <p>Here are some suggestions:</p>
                    <ul>
                      <li>Double-check the URL for typos.</li>
                      <li>Go back to the previous page.</li>
                      <li>Visit our <a href="/">homepage</a> to navigate to the desired page.</li>
                    </ul>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" text @click="goBack">Go Back</v-btn>
              <v-btn color="primary" text to="/">Go to Homepage</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  export default {
    methods: {
      goBack() {
        this.$router.go(-1);
      }
    }
  };
  </script>