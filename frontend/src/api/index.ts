import axios from 'axios'
import { ElMessage } from 'element-plus'

const API_BASE_URL = 'http://127.0.0.1:8001'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 添加 token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response) {
      const message = error.response.data?.detail || '请求失败'
      ElMessage.error(message)
      
      // 401 未授权，跳转登录
      if (error.response.status === 401) {
        localStorage.removeItem('token')
        window.location.href = '/login'
      }
    } else {
      ElMessage.error('网络错误')
    }
    return Promise.reject(error)
  }
)

export default api

