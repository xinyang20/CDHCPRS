import api from './index'

export const authAPI = {
  // 注册
  register: (username: string, password: string) => {
    return api.post('/api/auth/register', { username, password })
  },

  // 登录
  login: (username: string, password: string) => {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)
    
    return api.post('/api/auth/token', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
  },

  // 获取当前用户信息
  getCurrentUser: () => {
    return api.get('/api/auth/users/me')
  },

  // 修改密码
  updatePassword: (password: string) => {
    return api.put('/api/auth/users/me/password', { password })
  }
}

