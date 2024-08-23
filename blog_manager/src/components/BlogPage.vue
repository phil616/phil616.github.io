<template>
        
    <v-container>
      <v-row><!-- CREATE ROW -->
        <v-col cols="12">
            <h3>Blog Manager</h3>
          </v-col>
      </v-row>
      <v-row><!-- Table ROW --> 
        <v-col cols="12">
            <v-card>
              <v-card-title>Table</v-card-title>
              <v-card-text>
                <v-data-table
                  :headers="headers"
                  :items="blogList"
                  :items-per-page="20"
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
            <v-card-title>You are editing "{{ editingItem.title }}"</v-card-title>
            <v-card-text>
              <v-text-field v-model="editingItem.title" label="标题" required ></v-text-field>
              <v-text-field v-model="editingItem.date" label="日期" required ></v-text-field>
              <v-text-field v-model="email" label="邮箱" required ></v-text-field>
              <v-btn color="primary" @click="exportBlog" block class="my-2">导出</v-btn>
              <v-btn color="success" @click="viewBlog" block class="my-2">查看</v-btn>
              <v-btn color="error" @click="deleteBlog" block class="my-2">删除</v-btn>
              <v-btn color="error" @click="editDialog = false" block class="my-2">取消</v-btn>
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
                    editingItem: { date: '', title: '' },
                    email:"",
                    blogList: [],
                    headers: [
                        { text: 'Key', value: 'date' },
                        { text: 'Value', value: 'title' },
                        { text: 'Actions', value: 'actions', sortable: false }
                    ],
                }
            },
            methods: {
                exportBlog(){
                  let filename = this.editingItem.date + '-' + this.editingItem.title + '.md';
                  http.get("/blog/export?filename=" + filename + "&email="+this.email).then(response => {
                    console.log(response);
                    if(response.status === 200)
                  {
                      alert(response.data.message+" ID:"+response.data.bg_id);
                  }
                  })
                },
                viewBlog(){},
                deleteBlog(){
                  alert("Delete is not supported in this view.")
                },
                saveEdit(){},
                editItem(item){
                    this.editingItem = item;
                    this.editDialog = true;
                    this.dialog = true;
                },
                showDialog() {
                    this.dialog = true;
                },
                closeDialog() {
                    this.dialog = false;
                },
                createItem(){},
                fetchBlogList(){
                    http.get("/blog/all").then(response => {
                        let data = response.data;
                        const result = data.map(item => {
                            const parts = item.split('-');
                            if (parts.length < 4) return null; // 过滤掉不符合格式的项
                            const date = parts.slice(0, 3).join('-');
                            const title = parts.slice(3).join('-').replace('.md', '');
                            return { date, title };
                        }).filter(item => item !== null); // 过滤掉null值
                        this.blogList = result;                        
                    })
                },
            },
            mounted() {
                this.fetchBlogList();
            },
        }
    </script>