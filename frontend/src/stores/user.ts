import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface User {
  id: number
  username: string
  role: string
  is_banned: boolean
  created_at: string
}

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))

  const setUser = (userData: User) => {
    user.value = userData
  }

  const setToken = (newToken: string) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  const isAdmin = () => {
    return user.value?.role === 'admin'
  }

  const isAuthenticated = () => {
    return !!token.value && !!user.value
  }

  return {
    user,
    token,
    setUser,
    setToken,
    logout,
    isAdmin,
    isAuthenticated
  }
})

