import api from './index'

export const chatAPI = {
  // 创建新对话
  createConversation: (title: string) => {
    return api.post('/api/chat/conversations', { title })
  },

  // 获取对话列表
  getConversations: () => {
    return api.get('/api/chat/conversations')
  },

  // 获取对话详情
  getConversation: (id: number) => {
    return api.get(`/api/chat/conversations/${id}`)
  },

  // 获取对话消息
  getMessages: (conversationId: number) => {
    return api.get(`/api/chat/conversations/${conversationId}/messages`)
  },

  // 发送消息（流式响应）
  sendMessage: (conversationId: number, content: string, userInfo?: string) => {
    return fetch(`http://127.0.0.1:8001/api/chat/conversations/${conversationId}/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ content, user_info: userInfo })
    })
  },

  // 删除对话
  deleteConversation: (id: number) => {
    return api.delete(`/api/chat/conversations/${id}`)
  }
}

