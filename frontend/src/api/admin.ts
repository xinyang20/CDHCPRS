import api from './index'

export const adminAPI = {
  // 用户管理
  getUsers: () => {
    return api.get('/api/admin/users')
  },

  updateUser: (userId: number, data: { is_banned?: boolean }) => {
    return api.put(`/api/admin/users/${userId}`, data)
  },

  deleteUser: (userId: number) => {
    return api.delete(`/api/admin/users/${userId}`)
  },

  // 对话管理
  getAllConversations: () => {
    return api.get('/api/admin/conversations')
  },

  deleteConversation: (conversationId: number) => {
    return api.delete(`/api/admin/conversations/${conversationId}`)
  },

  // 系统设置
  getSettings: () => {
    return api.get('/api/admin/settings')
  },

  updateSettings: (data: any) => {
    return api.put('/api/admin/settings', data)
  },

  testConnection: (data: { llm_provider: string; llm_api_key: string; llm_model_id: string }) => {
    return api.post('/api/admin/settings/test-connection', data)
  }
}

