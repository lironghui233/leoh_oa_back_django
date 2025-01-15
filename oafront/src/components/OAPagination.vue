<script setup name="OAPagination">
    import {defineModel, defineProps} from 'vue';

    // 从父类获取变量
    let props = defineProps({
        total:{
            type: Number,
            default: 0
        },
        pageSize: {
            type: Number,
            default: 10,
        }
    })

    // 父类字类 双向绑定的 model 变量
    let page = defineModel({required: true})
</script>


<template>
     <el-pagination background layout="prev, pager, next" :total="props.total" 
            :page-size="props.pageSize" v-model:current-page="page" />   
</template>
    

<style scoped>
    .el-pagination{
        justify-content: center ;
    }
</style>