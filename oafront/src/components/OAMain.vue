<script setup name="OAMain">
import OAPageHeader from '@/components/OAPageHeader.vue';
import {defineProps} from 'vue';

//从父组件接受参数
let props = defineProps({
    title: '',
})
    
</script>

<template>
    <el-space direction="vertical" fill :size="23" style="width:100%">
        <OAPageHeader :content="props.title"></OAPageHeader>    
        <slot></slot>
    </el-space>
</template>
    
<style scoped>
    .el-space :deep(.el-space__item){
        width: 100%;
    }
</style>