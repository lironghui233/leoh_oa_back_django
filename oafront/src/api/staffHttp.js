import http from './http';

const getAllDepartment = () => {
    const path = "/staff/departments"
    return http.get(path)
}

export default {
    getAllDepartment,
}