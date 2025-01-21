<script setup name="informdetail">
    import {ref, reactive, onMounted} from 'vue';
    import OAMain from '@/components/OAMain.vue';
    import OADialog from '@/components/OADialog.vue';
    import OAPagination from '@/components/OAPagination.vue';
    import timeFormatter from '@/utils/timeFormatter';
    import {useAuthStore} from '@/stores/auth';
    import informHttp from '@/api/informHttp';
    import {ElMessage} from 'element-plus';
    import { useRoute } from 'vue-router';
     
    const route = useRoute()

    let inform = reactive({
        title: "",
        content: "",
        create_time: "",
        author: {
            realname: "",
            department: {
                name: "",
            }
        }
    })

    onMounted(async ()=>{
        const pk = route.params.pk
        try{
            let data = await informHttp.getInformDetail(pk)
            Object.assign(inform, data)             
        }catch(detail){
            ElMessage.error(detail)
        }
        // 阅读通知
        await informHttp.readInform(pk)
    })

</script>


<template>
    <OAMain title="通知详情">
        <el-card>
            <template #header>
                <div style="text-align: center;">
                    <h2 style="padding-bottom: 20px;">{{ inform.title }}</h2>
                    <div>
                        <span style="margin-right: 20px;">作者：{{ inform.author.realname }}</span>
                        <span>发布时间：{{ timeFormatter.stringFromDateTime(inform.create_time) }}</span>
                    </div>
                </div>
            </template>
            <template #default>
                <div v-html="inform.content" class="content"></div>
            </template>
            <template #footer>
                阅读量：{{ inform.read_count }}
            </template>
        </el-card>
    </OAMain>
</template>

    
<style scoped>
    /* .content ::v-deep(img){ */
    .content :deep(img){
        max-width: 100%;
    }
</style>