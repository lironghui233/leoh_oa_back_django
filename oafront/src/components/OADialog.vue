<script setup>
import {ref, defineModel, defineProps, defineEmits} from 'vue';

// 定义model：父子双向绑定的变量
let dialoVisible = defineModel({required: true})

// 定义属性：接受父类传来的变量
let props = defineProps({
    title:{
        type: String,
        default: ''
    },
    width: {
        type: String,
        default: '500',
    }
})

// 定义事件
let emits = defineEmits(['cancel', 'submit'])

const onCancel = () => {
    dialoVisible.value = false
    emits('cancel')
}

const onSubmit = () => {
    emits('submit')
}
    
</script>


<template>
    <el-dialog v-model="dialoVisible" :title="props.title" :width="props.width">
        <slot></slot>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="onCancel">取消</el-button>
                <el-button type="primary" @click="onSubmit">
                    提交
                </el-button>
            </div>
        </template>
    </el-dialog> 
</template>

    
<style scoped>
    
</style>