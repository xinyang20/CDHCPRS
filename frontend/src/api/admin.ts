import api from './index'

export interface AdminUser {
  id: number
  username: string
  role: string
  is_banned: boolean
  created_at: string
}

export interface ConversationSummary {
  id: number
  title: string
  user_id: number
  is_active: boolean
  created_at: string
}

export interface ConversationMessage {
  id: number
  conversation_id: number
  role: "user" | "assistant"
  content: string
  created_at: string
}

export interface AdminSettingsResponse {
  website_name: string
  website_logo: string
  system_prompt: string
  llm_provider: string
  llm_base_url: string
  llm_api_key: string
  llm_model_id: string
  llm_model_name: string
  large_font_scale: number
  suggested_questions_enabled: string
  suggested_questions_provider: string
  suggested_questions_base_url: string
  suggested_questions_api_key: string
  suggested_questions_model_id: string
  suggested_questions_system_prompt: string
  suggested_questions_count: string
  suggested_questions_max_rounds: string
  suggested_questions_template_questions: string
}

export interface AdminSettingsUpdatePayload {
  website_name?: string
  website_logo?: string
  system_prompt?: string
  llm_provider?: string
  llm_base_url?: string
  llm_api_key?: string
  llm_model_id?: string
  llm_model_name?: string
  large_font_scale?: number
  suggested_questions_enabled?: string
  suggested_questions_provider?: string
  suggested_questions_base_url?: string
  suggested_questions_api_key?: string
  suggested_questions_model_id?: string
  suggested_questions_system_prompt?: string
  suggested_questions_count?: string
  suggested_questions_max_rounds?: string
  suggested_questions_template_questions?: string
}

export interface TestConnectionPayload {
  llm_provider: string
  llm_api_key: string
  llm_model_id?: string
  llm_model_name?: string
  llm_base_url?: string
}

export interface TestConnectionResult {
  success: boolean
  message: string
}

export interface LLMModelOption {
  id: string
  name?: string | null
  owned_by?: string | null
}

export interface ModelListResponse {
  models: LLMModelOption[]
}

export interface LogoUploadResponse {
  logo_url: string
}

export const adminAPI = {
  getUsers: () => api.get<AdminUser[]>('/api/admin/users'),

  updateUser: (userId: number, data: { is_banned?: boolean }) => {
    return api.put<AdminUser>(`/api/admin/users/${userId}`, data)
  },

  deleteUser: (userId: number) => api.delete(`/api/admin/users/${userId}`),

  getAllConversations: () => api.get<ConversationSummary[]>('/api/admin/conversations'),

  deleteConversation: (conversationId: number) => {
    return api.delete(`/api/admin/conversations/${conversationId}`)
  },

  getConversationMessages: (conversationId: number) => {
    return api.get<ConversationMessage[]>(`/api/admin/conversations/${conversationId}/messages`)
  },

  getSettings: () => api.get<AdminSettingsResponse>('/api/admin/settings'),

  updateSettings: (data: AdminSettingsUpdatePayload) => {
    return api.put<AdminSettingsResponse>('/api/admin/settings', data)
  },

  testConnection: (data: TestConnectionPayload) => {
    return api.post<TestConnectionResult>('/api/admin/settings/test-connection', data)
  },

  fetchModels: (data: { llm_provider: string; llm_api_key: string; llm_base_url?: string }) => {
    return api.post<ModelListResponse>('/api/admin/settings/models', data)
  },

  uploadLogo: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post<LogoUploadResponse>('/api/admin/settings/upload-logo', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
}
