import axios from 'axios'
import { ElMessage } from 'element-plus'
import { i18n } from '../i18n'

const DEFAULT_API_BASE_URL = 'http://127.0.0.1:8001'

const getBaseUrl = () => {
  const envUrl = (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? ''
  const raw = envUrl.trim()
  const base = raw.length > 0 ? raw : DEFAULT_API_BASE_URL
  return base.replace(/\/$/, '')
}

export const API_BASE_URL = getBaseUrl()

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error),
)

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const message = error.response.data?.detail || i18n.global.t('messages.requestFailed')
      ElMessage.error(message)

      if (error.response.status === 401) {
        localStorage.removeItem('token')
        window.location.href = '/login'
      }
    } else {
      ElMessage.error(i18n.global.t('messages.networkError'))
    }
    return Promise.reject(error)
  },
)

export default api
