import api from './index'

export const authAPI = {
  register: (username: string, password: string) => {
    return api.post('/api/auth/register', { username, password })
  },

  login: (username: string, password: string) => {
    const params = new URLSearchParams()
    params.set('username', username)
    params.set('password', password)

    return api.post('/api/auth/token', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
  },

  getCurrentUser: () => {
    return api.get('/api/auth/users/me')
  },

  updatePassword: (password: string) => {
    return api.put('/api/auth/users/me/password', { password })
  },
}
