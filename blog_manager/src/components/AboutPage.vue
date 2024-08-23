<template>
  <v-container>
    <v-row>
      <v-col>
        <h1 class="text-center">关于本站</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <h2>博客管理</h2>
        <p>博客管理分为嵌入到博客中的管理系统和后台组成</p>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <h2>关于使用</h2>
        <p>管理系统是单机单用户系统，后台API保留了多用户拓展但不提供除单用户之外的授权功能</p>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <h2>隐私政策</h2>
        <p>数据和Cookie政策以具体应用行为为主。</p>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <h2>开源协议</h2>
        <p>MIT， GSE，CC BY-NC-SA 4.0</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'AboutPage'
}
</script>

<style scoped>
h1, h2 {
  margin-bottom: 1rem;
}
p {
  line-height: 1.6;
}
</style>
