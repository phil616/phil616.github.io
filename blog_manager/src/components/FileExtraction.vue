<template>
  <v-container>
    <v-row>
        <v-col cols="12" sm="12" md="12">
          <h3 class="text-center">文件提取</h3>
        </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-text-field
          v-model="extractionCode"
          label="提取码"
          outlined
          clearable
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-btn color="primary" @click="extractFile" block>提取文件</v-btn>
      </v-col>
      <v-col cols="12" sm="8" md="6">
        <v-btn @click="copyLink" block>复制提取链接</v-btn>
      </v-col>
    </v-row>
    <v-row justify="center" v-if="errorMessage">
      <v-col cols="12" sm="8" md="6">
        <v-alert type="error">{{ errorMessage }}</v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import http from '@/http'
export default {
  data() {
    return {
      fullLink: '',
      extractionCode: '',
      errorMessage: ''
    };
  },
  methods: {
    copyLink(){
      const textToCopy = this.fullLink; 
                const tempInput = document.createElement('textarea');
                tempInput.value = textToCopy;
                document.body.appendChild(tempInput);
                tempInput.select();
                document.execCommand('copy');
                document.body.removeChild(tempInput);
                alert('内容已复制到剪贴板');
    },
    async extractFile() {
      try {
        http.get("/share/exact?exact_code="+this.extractionCode).then(response => {
            if(response.status === 200)
            window.location.href = http.baseURL+"/share/exact?exact_code="+this.extractionCode;
            else if(response.status === 404)
            this.errorMessage = '提取码过期或无效';
        })
        .catch(error => {
            this.errorMessage = error;
        })

      } catch (error) {
        this.errorMessage = '提取码过期或无效';
      }
    }
  },
  created(){
    let params = this.$route.query;
    if(params.ec != null){
      this.extractionCode = params.ec
    }
    const fullURL = window.location.href;
    this.fullLink = fullURL;
  }
};
</script>

<style scoped>

</style>
