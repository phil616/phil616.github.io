import axios from 'axios';

// 创建axios实例
const service = axios.create({
  baseURL: process.env.VUE_APP_API 
});
service.baseURL = process.env.VUE_APP_API;
// 请求拦截器
service.interceptors.request.use(
  config => {
    // 从Cookie中获取token
    const token = getCookie('token'); // 假设getCookie是一个函数，用于从Cookie中获取指定字段的值
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    // 对请求错误做些什么
    return Promise.reject(error);
  }
);

// 响应拦截器
service.interceptors.response.use(
  response => {
    // 对响应数据做点什么
    return response;
  },
  error => {
    // 对响应错误做点什么
    return Promise.reject(error);
  }
);

export default service;

// 假设的getCookie函数
function getCookie(name) {
  return sessionStorage.getItem(name);
}
