import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

class Http{
    // 构造函数
    constructor(){
        this.instance = axios.create({
            baseURL: import.meta.env.VITE_BASE_URL,
            timeout: 6000,
        });

        // interceptors：拦截器（发起网络请求前的处理）
        this.instance.interceptors.request.use((config) => {
            const authStore = useAuthStore()
            const token = authStore.token
            
            if(token){
                config.headers.Authorization = "JWT " + token
            }
            return config
        })

        // interceptors：拦截器（发起网络请求后的处理）
        this.instance.interceptors.response.use()
    }

    post(path, data){
        // return this.instance.post(path, data)
        return new Promise(
            // 异步函数
            // async function (resolve, reject) {
            async (resolve, reject) => {
                // await 等待网络请求，挂起线程
                // 如果在某个函数中使用await，那么这个函数就必须定义成async
                try{                    
                    // axios 底层也是用promise对象，在响应的状态码不是200，调用reject，调用reject的结果是外层函数会抛出异常，即下面的代码
                    let result = await this.instance.post(path, data)
                    // 请求成功 (status == 200)
                    resolve(result.data)
                }catch(err){
                    // 请求失败 (status != 200)
                    try{
                        let detail = err.response.data.detail
                        reject(detail)
                    }catch{
                        reject('服务器错误！')
                    }
                }
            }
        )
    }

    get(path, params){
        // return this.instance.get(path, params)
        return new Promise( async (resolve, reject) => {
            try{
                let result = await this.instance.get(path, {params})
                // 请求成功 (status == 200)
                resolve(result.data)
            }catch(err){
                // 请求失败 (status != 200)
                try{
                    let detail = err.response.data.detail
                    reject(detail)
                }catch{
                    reject('服务器错误！')
                }
            }
        })
    }

    put(path, data) {
        // return this.instance.put(path, data)
        return new Promise(
            // 异步函数
            // async function (resolve, reject) {
            async (resolve, reject) => {
                // await 等待网络请求，挂起线程
                // 如果在某个函数中使用await，那么这个函数就必须定义成async
                try{                    
                    // axios 底层也是用promise对象，在响应的状态码不是200，调用reject，调用reject的结果是外层函数会抛出异常，即下面的代码
                    let result = await this.instance.put(path, data)
                    // 请求成功 (status == 200)
                    resolve(result.data)
                }catch(err){
                    // 请求失败 (status != 200)
                    try{
                        let detail = err.response.data.detail
                        reject(detail)
                    }catch{
                        reject('服务器错误！')
                    }
                }
            }
        )
    }

    delete(path){
        // return this.instance.delete(path)
        return new Promise(
            async (resolve, reject) => {
                try{                    
                    let result = await this.instance.delete(path)
                    // 因为服务端的delete方法，只是返回一个状态码，并没有数据，所以直接把result返回即可
                    resolve(result)
                }catch(err){
                    // 请求失败 (status != 200)
                    try{
                        let detail = err.response.data.detail
                        reject(detail)
                    }catch{
                        reject('服务器错误！')
                    }
                }
            }
        )
    }

    downloadFile(path, params){
        // return this.instance.get(path, params)
        return new Promise( async (resolve, reject) => {
            try{
                let result = await this.instance.get(path, {
                    params,
                    responseType:"blob"
                })
                // 请求成功 (status == 200)
                resolve(result.data)
            }catch(err){
                // 请求失败 (status != 200)
                try{
                    let detail = err.response.data.detail
                    reject(detail)
                }catch{
                    reject('服务器错误！')
                }
            }
        })
    }
}

export default new Http()