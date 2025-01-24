import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

const USER_KEY = "OA_USER_KEY"
const TOKEN_KEY = "OA_TOKEN_KEY"

export const PermissionChoice = {
  // 普通员工权限
  Staff: 0b000,
  // 需要董事会权限
  Boarder: 0b001,
  // team Leader权限
  Leader: 0b010,
  // 所有权限
  All: 0b111,
}

export const useAuthStore = defineStore('auth', () => {
  let _user = ref({})
  let _token = ref({})

  function setUserToken(user, token){
    // 保存到对象上 
    _user.value = user
    _token.value = token

    // 存储到浏览器的localStorge中（硬盘本地文件）
    localStorage.setItem(USER_KEY, JSON.stringify(user))
    localStorage.setItem(TOKEN_KEY, token)
  }

  function clearUserToken(){
    _user.value = {}
    _token.value = ""
    localStorage.removeItem(USER_KEY)
    localStorage.removeItem(TOKEN_KEY)
  }

  // 计算属性
  let user = computed(()=>{
    if(Object.keys(_user.value).length == 0){
        let user_str =  localStorage.getItem(USER_KEY)
        if(user_str){
          _user.value = JSON.parse(user_str) 
        }   
    }
    return _user.value
  }) 

  let token = computed(()=>{
    if(Object.keys(_token.value).length == 0){
        let token_str = localStorage.getItem(TOKEN_KEY)
        
        if(token_str){
          _token.value = token_str
        }
    }
    return _token.value
  })

  let is_logined = computed(() => {
    if(Object.keys(user.value).length>0 && token.value){
      return true
    }
    return false
  })

  let own_permissions = computed(() => {
    let _permissions = PermissionChoice.Staff
    if(is_logined.value){
      // 判断是否董事会成员
      if(user.value.department.name == '董事会'){
        _permissions |= PermissionChoice.Boarder
      }
      // 判断是否team leader
      if(user.value.department.leader_id == user.value.uid){
        _permissions |= PermissionChoice.Leader
      }
    }
    return _permissions
  })

  //opt可选值：
  //// 1. |: 或运算
  //// 2. &: 且运算
  function has_permission(permissions, opt='|'){
    let results = permissions.map((permission)=>(permission&own_permissions.value)==permission) 
    if(opt=='|'){
      if(results.indexOf(true)>=0){
        return true
      }else{
        return false
      }
    }else{
      if(results.indexOf(false)>=0){
        return false
      }else{
        return true
      }
    }
  }

  // 让外面访问必须返回
  return { setUserToken, is_logined, clearUserToken, user, token, has_permission }
})
