<script setup name="subabsent">
    import OAMain from '@/components/OAMain.vue';
    import absentHttp from '@/api/absentHttp';
    import {ref, reactive, onMounted} from 'vue';
    import {ElMessage} from 'element-plus';
    import timeFormatter from '@/utils/timeFormatter';
    import OAPagination from '@/components/OAPagination.vue';
    import OADialog from '@/components/OADialog.vue';

    let absents = ref([])
    let pagination = reactive({
        total: 0,
        page: 1,
    })
    let dialogVisible = ref(false)
    let absentForm = reactive({
        status: 2,
        response_content: ''
    })
    let rules = reactive({
        status:[
            {required: true, message: '请选择处理结果！', trigger: 'change'}
        ],
        response_content:[
            {required: true, message: '请输入理由！', trigger: 'blur'}
        ]
    })
    let absentFormRef = ref()
    let handleIndex = null

    onMounted(async () => {
        try{
            let data = await absentHttp.getSubAbsents()
            // console.log(data);
            pagination.total = data.count
            absents.value = data.results
        }catch(detail){
            ElMessage.error(detail)
        }
    }) 

    const onSubmitAbsent = () => {
        absentFormRef.value.validate(async (valid, fields)=>{
            if(valid){
                try{
                    const absent = absents.value[handleIndex]
                    const data = await absentHttp.handleSubAbsent(absent.id, absentForm.status, absentForm.response_content)
                    // console.log(data);
                    // 替换原来的
                    absents.value.splice(handleIndex, 1, data)
                    ElMessage.success('下属考勤处理成功！')
                    dialogVisible.value = false
                }catch(detail){
                    ElMessage.error(detail)
                }
            }
        })
    }

    const onShowDialog = (index) => {
        handleIndex = index
        absentForm.status = 2
        absentForm.response_content = ''
        dialogVisible.value = true
    }

</script>


<template>
    <OADialog title="处理考勤" v-model="dialogVisible" @submit="onSubmitAbsent">
        <el-form :model="absentForm" :rules="rules" ref="absentFormRef" label-width="100px">
            <el-form-item label="结果" prop="status">
                <el-radio-group v-model="absentForm.status">
                    <el-radio :value="2">通过</el-radio>
                    <el-radio :value="3">拒绝</el-radio>
                </el-radio-group>
            </el-form-item>
            <el-form-item label="理由" prop="response_content">
                <el-input type="textarea" v-model="absentForm.response_content" autocomplete="off" />
            </el-form-item>
        </el-form>
    </OADialog>

    <OAMain title="下属考勤">
        <el-card>
            <el-table :data="absents" style="width: 100%">
                <el-table-column prop="title" label="标题" />
                <el-table-column label="发起者" >
                    <template #default="scope">
                        {{ '[' + scope.row.requester.department.name + ']' + scope.row.requester.realname }}
                    </template>
                </el-table-column>
                <el-table-column prop="absent_type.name" label="类型" />
                <el-table-column prop="request_content" label="原因" />
                <el-table-column label="发起时间">
                    <template #default="scope">
                        {{ timeFormatter.stringFromDateTime(scope.row.create_time) }}
                    </template>
                </el-table-column>
                <el-table-column prop="start_date" label="开始日期" />
                <el-table-column prop="end_date" label="结束日期" />
                <el-table-column prop="responder.realname" label="审核人" />
                <el-table-column prop="response_content" label="反馈意见" />
                <el-table-column label="审核状态">
                    <template #default="scope">
                        <el-tag type="info" v-if="scope.row.status == 1">审核中</el-tag>
                        <el-tag type="success" v-else-if="scope.row.status == 2">已通过</el-tag>
                        <el-tag type="danger" v-else>已拒绝</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="处理">
                    <template #default="scope">
                        <el-button v-if="scope.row.status == 1" @click="onShowDialog(scope.$index)" type="primary" icon="EditPen" />
                        <el-button v-else disabled type="default">已处理</el-button>
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


</style>