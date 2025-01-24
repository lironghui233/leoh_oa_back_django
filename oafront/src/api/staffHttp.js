import http from './http';

const getAllDepartment = () => {
    const path = "/staff/departments"
    return http.get(path)
}

const addStaff = (realname, email, password) => {
    const path = "/staff/staff"
    return http.post(path, {realname, email, password})
}

const getStaffList = (page=1, size=10, params) => {
    const path = `/staff/staff`
    params = params?params:{}
    params['page'] = page
    params['size'] = size
    return http.get(path, params)
}

const updateStaffStatus = (staff_id, status) => {
    const path = "/staff/staff/" +staff_id
    return http.put(path, {status})
}

const downloadStaffs = (pks) => {
    const path = "/staff/download" 
    return http.downloadFile(path, {"pks":JSON.stringify(pks)})
}

export default {
    getAllDepartment,
    addStaff,
    getStaffList,
    updateStaffStatus,
    downloadStaffs,
}