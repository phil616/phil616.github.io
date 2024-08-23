<template>
        <div>
  <v-container>
    <v-row>
      <v-col>
        <h1 class="text-center">博客和文章的管理后台</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6" lg="4">
        <v-card>
          <v-card-title>博客管理</v-card-title>
          <v-card-text>
            管理Github博客<br>
            1. 文章查询-0%<br>
            2. 文章发布-0%<br>
            3. 文章列表<br>
            4. 文章删除<br>
            5. 文章导出-0%<br>
          </v-card-text>
          
        </v-card>
      </v-col>
      <v-col cols="12" md="6" lg="4">
        <v-card>
          <v-card-title>文章管理</v-card-title>
          <v-card-text>
            管理本地文章<br>
            1. 文章的增删改查<br>
            2. 文章加密<br>
            3. 文章导出<br>
            4. 文章发表形式渲染-0%<br>
          </v-card-text>
          
        </v-card>
      </v-col>
      <v-col cols="12" md="6" lg="4">
        <v-card>
          <v-card-title>文件管理和分享</v-card-title>
          <v-card-text>
            管理本地文件<br>
            1. 文件上传、下载<br>
            2. 文件共享<br>
            3. 文件打包迁移-50%未测试<br>
            4. 文件同步-0%<br>
            5. 文件加密-0%<br>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6" lg="4">
        <v-card>
          <v-card-title>缓存配置管理</v-card-title>
          <v-card-text>对缓存的CURD</v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
  </div>

</template>

<script>
export default {
   components:{
},
  name: 'HomePage',
};
</script>

<style scoped>
/* 添加一些自定义样式 */
</style>
