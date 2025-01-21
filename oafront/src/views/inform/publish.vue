<script setup name="informpublish">
    import OAMain from '@/components/OAMain.vue';
    import {ref, reactive, onMounted, onBeforeUnmount, shallowRef} from 'vue';
    import '@wangeditor/editor/dist/css/style.css' // 引入 css
    import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
    import staffHttp from '@/api/staffHttp';
    import {ElMessage} from 'element-plus';
    import {useAuthStore} from '@/stores/auth';
    import informHttp from '@/api/informHttp';

    const authStore = useAuthStore()

    let informForm = reactive({
        title: '',
        content: '', 
        department_ids: []
    })  
    let informFormRef = ref()
    let formLabelWidth = '100px'
    let departments = ref([])

    const rules = reactive({
        title: [{required: true, message: '请输入标题！', trigger:'blur'}],
        content: [{required: true, message: '请输入内容！', trigger:'blur'}],
        department_ids: [{required: true, message: '请选择部门！', trigger:'change'}],
    })

    const onSubmit = () => {
        informFormRef.value.validate(async (valid, fields)=>{
            if(valid){
                // console.log(informForm);
                try{
                    let data = await informHttp.publishInform(informForm)
                    // console.log(data);
                    ElMessage.success('发布成功！')
                    
                }catch(detail){
                    ElMessage.error(detail)
                }
            }
        })
    }

    onMounted(async ()=>{
        try{
            let data = await staffHttp.getAllDepartment()
            departments.value = data.results
        }catch(detail){
            ElMessage.error(detail)
        }
    })

    ///////// wangEditor 相关 /////////
    // 编辑器实例，必须用 shallowRef
    const editorRef = shallowRef()

    const toolbarConfig = {}
    const editorConfig = { 
        placeholder: '请输入内容...',
        MENU_CONF:{
            uploadImage: {
                server: import.meta.env.VITE_BASE_URL +  '/image/upload',  // 这里填服务器上传图片的url
                fieldName: 'image',
                maxFileSize: 0.5 * 1024 * 1024,
                maxNumberOfFiles: 100,
                allowedFileTypes: ['image/*'],
                headers: {
                    Authorization: 'JWT ' + authStore.token,
                },
                timeout: 6 * 1000, // 6秒,
                // 自定义插入图片
                customInsert(res, insertFn) {
                    if(res.errno == 0){
                        // res 即服务端的返回结果
                        // console.log(res);
                        let data = res.data
                        let url = import.meta.env.VITE_BASE_URL + data.url
                        let href = import.meta.env.VITE_BASE_URL + data.href
                        let alt = import.meta.env.VITE_BASE_URL + data.alt
                        // 从 res 中找到 url alt href ，然后插入图片
                        insertFn(url, alt, href)
                    }else{
                        ElMessage.error(res.message)
                    }
                },
                // 单个文件上传失败
                onFailed(file, res) {
                    console.log(`${file.name} 上传失败`, res)
                },
                // 上传错误，或者触发 timeout 超时
                onError(file, err, res) {
                    if(file.size > 0.5 * 1024 * 1024){
                        ElMessage.error('图片文件最大不能超过0.5MB！')
                    }
                    else{
                        ElMessage.error('图片格式不正确！')
                    }
                },
            }
        } 
    }

    // 组件销毁时，也及时销毁编辑器
    onBeforeUnmount(() => {
        const editor = editorRef.value
        if (editor == null) return
        editor.destroy()
    })

    let mode = "default"
    const handleCreated = (editor) => {
        editorRef.value = editor // 记录 editor 实例，重要！
    }
    ///////// wangEditor 相关 /////////

</script>


<template>
    <OAMain title="发布通知">
        <el-card>
            <el-form :model="informForm" :rules="rules" ref="informFormRef">
                <el-form-item label="标题" :label-width="formLabelWidth" prop="title">
                    <el-input v-model="informForm.title" autocomplete="off" />
                </el-form-item>
                <el-form-item label="部门可见" :label-width="formLabelWidth" prop="department_ids">
                    <el-select multiple v-model="informForm.department_ids">
                        <el-option :value="0" label="所有部门"></el-option>
                        <el-option v-for="department in departments" :label="department.name" :value="department.id"
                            :key="department.name" />
                    </el-select>
                </el-form-item>
                <el-form-item label="内容" :label-width="formLabelWidth" prop="content">
                    <div style="border: 1px solid #ccc; width:100%;">
                        <Toolbar style="border-bottom: 1px solid #ccc" :editor="editorRef"
                            :defaultConfig="toolbarConfig" :mode="mode" />
                        <Editor style="height: 500px; overflow-y: hidden;" v-model="informForm.content"
                            :defaultConfig="editorConfig" :mode="mode" @onCreated="handleCreated" />
                    </div>
                </el-form-item>
                <el-form-item>
                    <div style="text-align: right; flex: 1">
                        <el-button type="primary" @click="onSubmit">提交</el-button>
                    </div>
                </el-form-item>
            </el-form>
        </el-card>
    </OAMain>
</template>

    
<style scoped>
    
</style>