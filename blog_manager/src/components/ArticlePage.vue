<template>
        
    <v-container>
      <v-row><!-- CREATE ROW -->
        <v-col cols="12">
            <v-btn to="/new-article" class="primary"> 新增文章 </v-btn>
        </v-col>
      </v-row>
      <v-row><!-- Filter ROW -->
        <v-col cols="12">
            <v-card>
              <v-card-title>筛选</v-card-title>
              <v-card-text>
                <v-form ref="form">
                  <v-text-field v-model="searchName" label="标题包含"></v-text-field>
                  <v-text-field v-model="searchTag" label="标签包含"></v-text-field>
                  <v-row>
                    <v-col cols="6"> <v-btn color="primary" block @click="filterItems">筛选</v-btn></v-col>
                    <v-col cols="6"> <v-btn color="error" block @click="resetFilter">重置</v-btn></v-col>
                  </v-row>
                 
                 
                </v-form>
              </v-card-text>
            </v-card>
          </v-col>
      </v-row>
      <v-row><!-- Table ROW --> 
        <v-col cols="12">
            <v-card>
              <v-card-title>Table</v-card-title>
              <v-card-text>
                <v-data-table
                  :headers="headers"
                  :items="articleList"
                  :items-per-page="10"
                  class="elevation-1"
                >
                  <template slot="item.actions" slot-scope="{ item }">
                    <v-btn small class="mr-2" @click="editItem(item)">编辑</v-btn>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
          </v-col>
      </v-row>
      <v-dialog v-model="dialog" max-width="500px">  <!-- Modify Dialog -->
        <v-card>
            <v-card-title>Edit</v-card-title>
            <v-card-text>
              <v-text-field v-model="editingItem.id" label="ID" disabled></v-text-field>
              <v-text-field v-model="editingItem.title" label="标题" disabled ></v-text-field>

              <v-row>
              <v-col col="12">
                <v-btn color="success" @click="saveEdit(editingItem.id)">编辑</v-btn>
              </v-col>
              </v-row>
              <v-row>
              <v-col col="12">
                <v-btn color="error" @click="dialog=!dialog">取消</v-btn>
              </v-col>
              </v-row>
              <v-row>
              <v-col col="12">
                <v-text-field v-model="exportEmail" label="导出到邮箱"></v-text-field>
              </v-col>
              </v-row>
              <v-row>
              <v-col col="12">
                <v-btn color="primary" @click="exportArticle">导出</v-btn>
              </v-col>
              </v-row>
            </v-card-text>
          </v-card>
      </v-dialog>
    </v-container>
    </template>
    
    <script>    
    import http from '@/http'
        export default {
            name: 'TemplatePage',
            data() {
                return {
                    dialog: false,
                    editDialog: false,
                    editingItem: { id: '', title: '', tags: [], decrypted: '' },
                    articleList: [],
                    searchName: "",
                    searchTag: "",
                    exportEmail: "",
                    headers: [
                        { text: '编号', value: 'id' },
                        { text: '标题', value: 'title' },
                        { text: '标签', value: 'tags' },
                        { text: '是否加密', value: 'decrypted' },
                        { text: 'Actions', value: 'actions', sortable: false }
                    ],
                }
            },
            methods: {
                filterItems(){
                     // 获取搜索条件
                    const searchName = this.searchName.toLowerCase();
                    const searchTag = this.searchTag.toLowerCase();

                    // 根据搜索条件筛选文章列表
                    this.articleList = this.articleList.filter(item => {
                        const nameMatch = item.title.toLowerCase().includes(searchName);
                        const tagMatch = item.tags.some(tag => tag.toLowerCase().includes(searchTag));

                        // 返回满足所有条件的文章
                        return nameMatch && tagMatch;
                    });
                },
                resetFilter(){
                    this.searchName = "";
                    this.searchTag = "";
                    this.fetchAllArticle();
                },
                saveEdit(id){
                    this.$router.push("/new-article?id="+id);
                },
                editItem(item){
                    this.editingItem = item;
                    this.editDialog = true;
                    this.dialog = true;
                    item;
                },
                showDialog() {
                    this.dialog = true;
                },
                closeDialog() {
                    this.dialog = false;
                },
                exportArticle(){
                  http.get("/article/migrate?email="+this.exportEmail+"&id="+this.editingItem.id)
                   .then(response => {
                        console.log(response.data);
                        if(response.status === 200){
                          alert("导出成功 "+"ID:"+response.data.bg_id)
                        }
                    }).catch(error => {error})
                },
                createItem(){},
                fetchAllArticle(){
                    http.get("/article/all").then(response => {
                        this.articleList = response.data;
                        this.articleList.forEach(item => {
                            item.decrypted = item.decrypted ? "是" : "否";
                            if(item.tags.length > 0){
                                item.tags = JSON.parse(item.tags.replace(/'/g, '"'));
                            }else{
                                item.tags = [];
                            }
                        });
                    }).catch(error => {error})
                },
            },
            created() {
                this.fetchAllArticle();
            },
        }
    </script>