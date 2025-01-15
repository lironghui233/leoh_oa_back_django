<script setup name="OAPageHeader">
    import {useRouter} from 'vue-router';
    import {defineProps} from 'vue';

    const router = useRouter()

    const goBack = () => {
        //返回上一个页面
        router.go(-1)
    }

    // 接受父类变量
    let props = defineProps({
        content: ''
    })
</script>


<template>
    <el-page-header @back="goBack" title='返回'>
        <template #content>
            <span class="text-large font-600 mr-3"> {{props.content}} </span>
        </template>
    </el-page-header>
</template>
    
    
<style scoped>
    
</style>