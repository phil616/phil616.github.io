<template>
        
    <v-container>
      <v-row><!-- CREATE ROW -->
        <v-col cols="12">
            <v-alert type="error" text prominent border="left" v-if="encrypted">
             该文章可能已经被加密，您可以使用对称密码解密，解密前Markdown将不会渲染
            </v-alert>
          </v-col>
          <v-col cols="12">
            <v-text-field label="ID" v-model="id" disabled v-if="!newArticle"></v-text-field>
            <v-text-field label="标题" v-model="title" required></v-text-field>
            <v-row>
                <v-col cols="8">
                    <v-text-field label="tag" v-model="ctag"></v-text-field>
                </v-col>
                <v-col cols="4">
                    <v-btn color="primary" @click="addTag" block>添加</v-btn>
                </v-col>
            </v-row>
            <v-row>
                Tags:
                <v-chip 
                v-for="(tag, index) in tags" 
                :key="index" 
                :label="tag" 
                small class="ml-2"
                @click="removeTag(index)"
                >{{ tag }}</v-chip>
            </v-row>
            <v-row>
                <v-col cols="4"><v-btn block color="primary" @click="saveArticle">缓存</v-btn></v-col>
                <v-col cols="4"><v-btn block color="error" @click="clearArticle">清空缓存</v-btn></v-col>
                <v-col cols="4"><v-btn block color="primary" @click="readArticle">读取缓存</v-btn></v-col>
            </v-row>
          </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
            <v-textarea label="Markdown内容"  auto-grow v-model="markdownText" required></v-textarea>
            
        </v-col>
        <v-col cols="12">
            <v-btn block @click="copyToClipboard">复制到剪贴板</v-btn>
        </v-col>
        <v-col cols="12" v-if="!encrypted">
            <p>渲染区域</p>
            <div v-html="renderedMarkdown" class="markdown-body"></div>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
            <v-btn block color="primary" @click="submitPage">提交/更新</v-btn>
        </v-col>
        <v-col cols="12">
            <v-divider></v-divider>
        </v-col>
        <v-col cols="12">
            <v-text-field label="对称加密密码" v-model="passphrase" type="password"></v-text-field>
        </v-col>
        <v-col cols="12">
            <v-btn block color="success" @click="encryptArticle">加密文章</v-btn>
        </v-col>
        <v-col cols="12">
            <v-btn block color="primary" @click="decrypteArticle">解密文章</v-btn>
        </v-col>
      </v-row>
    </v-container>
</template>
    
    <script>  
    import Markdown from 'markdown-it'
    import http from '@/http'  
        export default {
            name: 'NewArticlePage',
            data() {
                return {
                    id: '',
                    ctag: '',
                    title: '',
                    markdownText: '',
                    passphrase: '',
                    tags: [],
                    encrypted: false,
                    newArticle: true,
                }
            },
            methods: {
                copyToClipboard(){
                const textToCopy = this.markdownText; // 假设你要复制的内容是 markdownText
                const tempInput = document.createElement('textarea');
                tempInput.value = textToCopy;
                document.body.appendChild(tempInput);
                tempInput.select();
                document.execCommand('copy');
                document.body.removeChild(tempInput);
                alert('内容已复制到剪贴板');
                },
                submitPage(){
                    if (this.newArticle){
                        http.post("/article/create",{
                            title:this.title,
                            //tags:this.tags,
                            tags: JSON.stringify(this.tags),
                            content:this.markdownText,
                            decrypted:this.encrypted
                        }).then(response => {
                            if (response.status === 200){
                                alert("文章已提交/更新");
                            }
                        })
                    }else{
                        http.put("/article/update/"+this.id,{
                            title:this.title,
                            //tags:this.tags,
                            tags: JSON.stringify(this.tags),
                            content:this.markdownText,
                            decrypted:this.encrypted
                        }).then(response => {
                            if (response.status === 200){
                                alert("文章已提交/更新");
                            }
                        })
                    }

                },
                encryptArticle(){
                    if(this.passphrase.trim() === "")
                        return;
                    http.post("/symmetric_encrypt",{
                        data:this.markdownText,
                        passphrase:this.passphrase
                    }).then(response => {
                        this.markdownText = response.data;
                        this.encrypted = true;
                    })
                },
                decrypteArticle(){
                    if(this.passphrase.trim() === "")
                        return;
                    http.post("/symmetric_decrypt",{
                        data:this.markdownText,
                        passphrase:this.passphrase
                    }).then(response => {
                        this.markdownText = response.data;
                        this.encrypted = false;
                    })
                },
                removeTag(idx){
                    this.tags.splice(idx,1);
                    console.log(idx);
                },
                saveArticle(){
                    localStorage.setItem('tmpArticle',JSON.stringify(this.markdownText))
                },
                readArticle(){
                    let tmpArticle = localStorage.getItem('tmpArticle');
                    if(tmpArticle !== null){
                        this.markdownText = JSON.parse(tmpArticle);
                    }
                },
                clearArticle(){
                    localStorage.removeItem('tmpArticle');
                },

                addTag(){
                    if(this.ctag.trim() !== ""){
                        this.tags.push(this.ctag.trim());
                        this.ctag = "";
                    }
                },
            },
            computed: {
                renderedMarkdown() {
                    const md = new Markdown();
                    return md.render(String(this.markdownText));
                }
            },
            created(){
                let params = this.$route.query;
                console.log(params);
                if(params.id === undefined){
                    // new article
                    this.newArticle = true;
                    this.title = "";
                    this.tags = [];
                    this.markdownText = "";
                    this.encrypted = false;
                }else{
                    let id = params.id;
                    this.id = id;
                    this.newArticle = false;
                    http.get("/article/get/"+id).then(response => {
                        this.title = response.data.title;
                        this.tags = JSON.parse(response.data.tags.replace(/'/g, '"'));
                        this.markdownText = response.data.content;
                        if (response.data.decrypted){
                            this.encrypted = true;
                        }
                    })
                }
            }
        }
</script>