<template>
        
<v-container>
  <v-row><!-- CREATE ROW -->
    <v-col cols="12">
        <v-card>
          <v-card-title>Create</v-card-title>
          <v-card-text>
            <v-form ref="form">
              <v-text-field v-model="newKey"   label="Key" required ></v-text-field>
              <v-text-field v-model="newValue" label="Value" required ></v-text-field>
              <v-btn color="success" @click="createItem">Submit</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
  </v-row>
  <v-row><!-- Filter ROW -->
    <v-col cols="12">
        <v-card>
          <v-card-title>Search</v-card-title>
          <v-card-text>
            <v-form ref="form">
              <v-text-field v-model="newKey"   label="Key" required ></v-text-field>
              <v-text-field v-model="newValue" label="Value" required ></v-text-field>
              <v-btn color="primary" @click="filterItems">Filter</v-btn>
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
              :items="kvList"
              :items-per-page="5"
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
          <v-text-field v-model="editingItem.key" label="Key" required ></v-text-field>
          <v-text-field v-model="editingItem.value" label="Value" required ></v-text-field>
          <v-btn color="success" @click="saveEdit">保存</v-btn>
          <v-btn color="error" @click="editDialog = false">取消</v-btn>
        </v-card-text>
      </v-card>
  </v-dialog>
</v-container>
</template>

<script>    
    export default {
        name: 'TemplatePage',
        data() {
            return {
                dialog: false,
                editDialog: false,
                editingItem: { key: '', value: '' },
                kvList: [],
                headers: [
                    { text: 'Key', value: 'key' },
                    { text: 'Value', value: 'value' },
                    { text: 'Actions', value: 'actions', sortable: false }
                ],
            }
        },
        methods: {
            editItem(item){
                item;
            },
            showDialog() {
                this.dialog = true;
            },
            closeDialog() {
                this.dialog = false;
            },
            createItem(){},
        }
    }
</script>