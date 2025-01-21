<script setup name="informlist">
    import {ref, reactive, onMounted} from 'vue';
    import OAMain from '@/components/OAMain.vue';
    import OADialog from '@/components/OADialog.vue';
    import OAPagination from '@/components/OAPagination.vue';
    import timeFormatter from '@/utils/timeFormatter';
    import {useAuthStore} from '@/stores/auth';
    import informHttp from '@/api/informHttp';
    import {ElMessage} from 'element-plus';

    const authStore= useAuthStore()

    let informs = ref([])
    let pagination = reactive({
        page: 1,
        total: 0
    })
    let dialogVisible = ref(false)
    let handleIndex = 0

    const onShowDialog = (index) => {
        handleIndex = index
        dialogVisible.value = true
    }

    const onDeleteInform = async () => {
        try{
            let inform = informs.value[handleIndex]
            await informHttp.deleteInform(inform.id)
            informs.value.splice(handleIndex, 1)
            ElMessage.success("通知删除成功！")
            dialogVisible.value = false
        }catch(detail){
            ElMessage.error(detail)
        }
    }

    onMounted(async ()=>{
        try{
            let data = await informHttp.getInformList(1)
            // data = {count: , next: , previous: , results:[]}
            pagination.total = data.total
            informs.value = data.results
        }catch(detail){
            ElMessage.error(detail)
        }
    })

</script>


<template>
    <OADialog v-model="dialogVisible" title="提示" @submit="onDeleteInform"> 
        <span>您确定要删除这个通知吗？</span>
    </OADialog>
    <OAMain title="通知列表">
        <el-card>
            <el-table :data="informs" style="width: 100%">
                <el-table-column label="标题">
                    <template #default="scope">
                        <el-badge v-if="scope.row.reads.length==0" is-dot class="item">
                            <RouterLink :to="{name: 'inform_detail', params: {pk: scope.row.id}}">
                                {{ scope.row.title }}
                            </RouterLink>
                        </el-badge>
                        <RouterLink v-else :to="{name: 'inform_detail', params: {pk: scope.row.id}}">
                                {{ scope.row.title }}
                            </RouterLink>
                    </template>
                </el-table-column>
                <el-table-column label="发布者" >
                    <template #default="scope">
                        {{ '[' + scope.row.author.department.name + ']' + scope.row.author.realname }}
                    </template>
                </el-table-column>
                <el-table-column label="发布时间">
                    <template #default="scope">
                        {{ timeFormatter.stringFromDateTime(scope.row.create_time) }}
                    </template>
                </el-table-column>
                <el-table-column label="部门可见">
                    <template #default="scope">
                        <el-tag v-if="scope.row.public" type="success">公开</el-tag>
                        <el-tag v-else v-for="department in scope.row.departments" :key="department.name" type="info">{{ department.name }}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button v-if="scope.row.author.uid == authStore.user.uid" @click="onShowDialog(scope.$index)" type="danger" icon="Delete" />
                        <el-button v-else disabled type="default">无</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <template #footer>
                <OAPagination v-model="pagination.page" :total="pagination.total"></OAPagination>
            </template>
        </el-card>
    </OAMain>
</template>

    
<style scoped>
    .el-tag{
        margin-right: 3px;
    }
    .el-badge{
        margin-right: 5px;
        margin-top: 5px;
    } 
</style>