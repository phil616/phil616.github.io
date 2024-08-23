<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col>
        <h1>您正在分享文件</h1>
        <v-col col="12">文件名</v-col>
        <v-col col="12">{{ fileName }}</v-col>
        <v-col col="12">文件ID</v-col>
        <v-col col="12">{{ fid }}</v-col>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col col="6"  jusify="center">
          <v-text-field type="number" v-model="shareTime" outlined dense></v-text-field>
      </v-col>
      <v-col col="6">
        单位：分钟
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col col="6">
        <v-btn color="primary" block @click="createShare">创建分享码</v-btn>
      </v-col>
    </v-row>
    <v-row v-if="shareCode">
      <v-col col="12"> <p>分享码：{{ shareCode }}</p></v-col>
      <v-col col="12">
        <v-btn block color="primary" @click="copyShareCode">复制分享码</v-btn>
      </v-col>
      <v-col col="12">
        <v-btn block color="success" @click="goExtract">去提取</v-btn>
      </v-col>
    </v-row>
    
  </v-container>
</template>

<script>
import http from '@/http'

export default {
  data() {
    return {
      fid: null,
      fileName: null,
      shareTime: 30,
      shareCode: null
    };
  },
  created() {
    let params = this.$route.query;
    this.fid = params.fid;
    http.get("/file/list").then(response => {
      let filename = response.data.find(item => item.fid === this.fid).filename;
      this.fileName = filename;
    })
  },
  methods: {
    async createShare() {
      http.get(`file/create_share?fid=${this.fid}&exp=${this.shareTime}`).then(
        response => {
          this.shareCode = response.data.extract_code;
        }
      )
    },
    goExtract(){
      window.location.href = `fileextraction?ec=${this.shareCode}`;
    },
    copyShareCode() {
      navigator.clipboard.writeText(this.shareCode).then(() => {
        alert("分享码已复制到剪贴板");
      }).catch((err) => {
        console.error('复制失败: ', err);
      });
    }
  }
};
</script>
