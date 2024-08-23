<template>
  <v-container>
    <v-row>
      <v-col>
        <v-file-input
          label="文件上传"
          @change="handleFileUpload"
        ></v-file-input>
        <v-btn color="primary" @click="uploadFile">上传</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-text-field
          label="文件查询"
          v-model="searchQuery"
          @input="searchFiles"
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-list>
            <v-list-item v-for="file in filteredFiles" :key="file.fid" :class="{ 'v-list-item-background': true }">
            <v-list-item-content>
                <v-list-item-title>{{ file.filename }}</v-list-item-title>
                <v-list-item-subtitle>{{ file.mimetype }}</v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
                <v-col>
                    <v-btn @click="downloadFile(file.fid)">下载</v-btn>
                </v-col>
                <v-col>
                    <v-btn @click="deleteFile(file.fid)">删除</v-btn>
                </v-col>
                <v-col>
                    <v-btn @click="shareFile(file.fid)">分享</v-btn>
                </v-col>
            </v-list-item-action>
            </v-list-item>
        </v-list>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import http from '@/http';

export default {
  data() {
    return {
      files: [],
      searchQuery: '',
      uploadedFile: null,
    };
  },
  computed: {
    filteredFiles() {
      return this.files.filter(file =>
        file.filename.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {
    handleFileUpload(file) {
      this.uploadedFile = file;
    },
    async uploadFile() {
      if (this.uploadedFile) {
        const formData = new FormData();
        formData.append('file', this.uploadedFile);

        try {
          const response = await http.post('/file/upload', formData);
          console.log('文件上传成功', response.data);
          this.fetchFiles();
          this.uploadedFile = null;
        } catch (error) {
          console.error('文件上传失败', error);
        }
      }
    },
    async fetchFiles() {
      try {
        const response = await http.get('/file/list');
        this.files = response.data;
      } catch (error) {
        console.error('获取文件列表失败', error);
      }
    },
    searchFiles() {
      // 查询逻辑在 computed 属性中处理
    },
    async downloadFile(fileId) {
        window.open(`${http.baseURL}/file/download/${fileId}`);
        if(fileId){
            return;
        }
        // unreachable code
        try {
            const response = await http.get(`/file/download/${fileId}`, { responseType: 'blob' });
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', response.headers['content-disposition'].split('=')[1]); // 设置下载文件的名称
            document.body.appendChild(link);
            link.click();
        } catch (error) {
            console.error('文件下载失败', error);
        }
    },
    async deleteFile(fileId) {
      try {
        await http.delete(`/file/delete/${fileId}`);
        this.fetchFiles();
      } catch (error) {
        console.error('文件删除失败', error);
      }
    },
    shareFile(fileId) {
        console.log('分享文件', fileId);
        const fid = fileId;
        this.$router.push("/fileshare?fid=" + fid);
    }
  },
  created() {
    this.fetchFiles();
  },
};
</script>


<style scoped>
.v-list-item-background {
  background-color: #f0f0f0; /* 你可以根据需要更改背景颜色 */
}
</style>