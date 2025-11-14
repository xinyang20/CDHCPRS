import api, { API_BASE_URL } from './index'

const buildUrl = (path: string) => `${API_BASE_URL}${path}`

export const chatAPI = {
  createConversation: (title: string) => {
    return api.post('/api/chat/conversations', { title })
  },

  getConversations: () => {
    return api.get('/api/chat/conversations')
  },

  getConversation: (id: number) => {
    return api.get(`/api/chat/conversations/${id}`)
  },

  getMessages: (conversationId: number) => {
    return api.get(`/api/chat/conversations/${conversationId}/messages`)
  },

  sendMessage: (conversationId: number, content: string, userInfo?: string) => {
    return fetch(buildUrl(`/api/chat/conversations/${conversationId}/messages`), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('token') ?? ''}`,
      },
      body: JSON.stringify({ content, user_info: userInfo }),
    })
  },

  deleteConversation: (id: number) => {
    return api.delete(`/api/chat/conversations/${id}`)
  },

  getSuggestedQuestions: (conversationId: number) => {
    return api.get(`/api/chat/conversations/${conversationId}/suggested-questions`)
  },
}
