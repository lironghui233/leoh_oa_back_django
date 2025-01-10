<script setup name="login">
    import login_img from '@/assets/image/login.png';    
    import { reactive } from 'vue';
    import { useAuthStore } from '@/stores/auth';
    import { useRouter } from 'vue-router';
    import authHttp from '@/api/authHttp';
    import {ElMessage} from 'element-plus';

    const authStore = useAuthStore()
    const router = useRouter()

    let form = reactive({
        email: '',
        password: ''
    })

    const onSubmit = async () => {
        let pwdRgx = /^[0-9a-zA-Z_-]{6,20}/
        let emailRgx = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9])+/
        if(!emailRgx.test(form.email)){
            // alert('邮箱格式不满足！')
            ElMessage.info('邮箱格式不满足！')
            return
        }
        if(!pwdRgx.test(form.password)){
            // alert('密码格式不满足！')
            ElMessage.info('密码格式不满足！')
            return
        }

        // 1. 直接使用 axios
        // axios.post("http://127.0.0.1:8000/auth/login",{
        //     email: form.email,
        //     password: form.password,
        // })
        // // promise
        // .then(function(response){
        //     // 处理成功情况
        //     console.log(response);
        //     let data = response.data
        //     let token = data.token
        //     let user = data.user
        //     // 保存信息
        //     authStore.setUserToken(user, token)
        //     // 跳转页面
        //     router.push({name:"frame"})
        // })
        // .catch(function(error){
        //     // 处理错误情况    
        //     let detail = error.response.data.detail
        //     alert(detail)
        // })
        // .finally(function(){
        //     // 总是会执行
        // });

        // 2. 封装一层 axios
        // authHttp.login(form.email, form.password)
        // // promise
        // .then(function(response){
        //     // 处理成功情况
        //     // console.log(response);
        //     let data = response.data
        //     let token = data.token
        //     let user = data.user
        //     // 保存信息
        //     authStore.setUserToken(user, token)
        //     // 跳转页面
        //     router.push({name:"frame"})
        // })
        // .catch(function(error){
        //     // 处理错误情况    
        //     let detail = error.response.data.detail
        //     alert(detail)
        // })
        // .finally(function(){
        //     // 总是会执行
        // });

        // 3. 基于 Promises 实现的语法糖, 使代码看起像同步调用 (实际仍是异步调用，只是写法上更加简洁和易于理解。)
        try{
            let data = await authHttp.login(form.email, form.password)
            let token = data.token
            let user = data.user
            // 保存信息
            authStore.setUserToken(user, token)
            // 跳转页面
            router.push({name:"frame"})
        }catch(detail){
            // alert(detail)
            ElMessage.error(detail)
        }
    }
</script>


<template>
    <div class="dowebok">
        <div class="container-login100">
            <div class="wrap-login100">
                <div class="login100-pic js-tilt" data-tilt>
                    <img :src="login_img" alt="IMG" />
                </div>

                <div class="login100-form validate-form">
                    <span class="login100-form-title"> 员工登陆 </span>

                    <div class="wrap-input100 validate-input">
                        <input class="input100" type="text" name="email" placeholder="邮箱" v-model="form.email"/>
                        <span class="focus-input100"></span>
                        <span class="symbol-input100">
                            <i class="iconfont icon-fa-envelope" aria-hidden="true"></i>
                        </span>
                    </div>

                    <div class="wrap-input100 validate-input">
                        <input class="input100" type="password" name="password" placeholder="密码" v-model="form.password"/>
                        <span class="focus-input100"></span>
                        <span class="symbol-input100">
                            <i class="iconfont icon-fa-lock" aria-hidden="true"></i>
                        </span>
                    </div>

                    <div class="container-login100-form-btn">
                        <button class="login100-form-btn" @click="onSubmit">
                            登陆
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

    
<style scoped src="@/assets/css/login.css"></style>
<style scoped src="@/assets/iconfont/iconfont.css"></style>