import axios from 'axios';

class Http{
    // 构造函数
    constructor(){
        this.instance = axios.create({
            baseURL: import.meta.env.VITE_BASE_URL,
            timeout: 6000,
        });
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
                    let detail = err.response.data.detail
                    reject(detail)
                }
            }
        )
    }

    get(path, params){
        return this.instance.get(path, params)
    }
}

export default new Http()