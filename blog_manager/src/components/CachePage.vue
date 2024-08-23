<template>
  <v-container>
    <v-row>
        <v-col cols="12"><h1> Page</h1></v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>增加KV对</v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="valid" lazy-validation>
              <v-text-field
                v-model="newKey"
                label="Key"
                required
              ></v-text-field>
              <v-text-field
                v-model="newValue"
                label="Value"
                required
              ></v-text-field>
              <v-btn color="success" @click="addKV">增加</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>条件查询KV对</v-card-title>
          <v-card-text>
            <v-text-field
              v-model="searchKey"
              label="Search Key"
            ></v-text-field>
            <v-btn color="primary" @click="searchKV">查询</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>所有的KV对列表</v-card-title>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="kvList"
              :items-per-page="5"
              class="elevation-1"
            >
              <template slot="item.actions" slot-scope="{ item }">
                <v-btn small class="mr-2" @click="editKV(item)">编辑</v-btn>
                <v-btn small @click="deleteKV(item)">删除</v-btn>
              </template>

            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 编辑KV对的对话框 -->
    <v-dialog v-model="editDialog" max-width="500px">
      <v-card>
        <v-card-title>编辑KV对</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="editingItem.key"
            label="Key"
            required
          ></v-text-field>
          <v-text-field
            v-model="editingItem.value"
            label="Value"
            required
          ></v-text-field>
          <v-btn color="success" @click="saveEdit">保存</v-btn>
          <v-btn color="error" @click="editDialog = false">取消</v-btn>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import http from '@/http'
export default {
  data() {
    return {
      valid: true,
      newKey: '',
      newValue: '',
      searchKey: '',
      kvList: [],
      headers: [
        { text: 'Key', value: 'key' },
        { text: 'Value', value: 'value' },
        { text: 'Actions', value: 'actions', sortable: false }
      ],
      editDialog: false,
      editingItem: { key: '', value: '' }
    };
  },
  methods: {
    addKV() {
      if (this.newKey && this.newValue) {
        http.post('/kv/set', { key: this.newKey, value: this.newValue })
        this.kvList.push({ key: this.newKey, value: this.newValue });
        this.newKey = '';
        this.newValue = '';
      }
    },
    searchKV() {
      if (this.searchKey) {
        const result = this.kvList.filter(item => item.key === this.searchKey);
        this.kvList = result;
      } else {

        this.fetchKVList();
      }
    },
    editKV(item) {
      this.editingItem = { ...item };
      this.editDialog = true;
    },
    saveEdit() {
        http.post('/kv/set', { key: this.editingItem.key, value: this.editingItem.value })

        this.fetchKVList();
        this.editDialog = false;
    },
    deleteKV(item) {
        http.get('/kv/remove/'+item.key).then(response => {
            if (response.status == 200)
                this.fetchKVList();
        })

    },
    fetchKVList() {
        http.get('/kv/all').then(response => {
            this.kvList = Object.entries(response.data).map(([key, value]) => ({ key, value }));
        })
        .catch(error => {
        console.log(error);})
    }
  },
  mounted() {
    this.fetchKVList();
  }
};
</script>

<style scoped>
/* 你可以在这里添加一些样式 */
</style>
