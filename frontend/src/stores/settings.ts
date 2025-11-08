import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

const SENIOR_MODE_KEY = 'cdhcprs_senior_mode'

export const useSettingsStore = defineStore('settings', () => {
  // 从 localStorage 读取初始值
  const seniorMode = ref<boolean>(
    localStorage.getItem(SENIOR_MODE_KEY) === 'true'
  )

  // 监听变化并保存到 localStorage
  watch(seniorMode, (newValue) => {
    localStorage.setItem(SENIOR_MODE_KEY, String(newValue))
    // 应用或移除老年版样式
    if (newValue) {
      document.documentElement.classList.add('senior-mode')
    } else {
      document.documentElement.classList.remove('senior-mode')
    }
  }, { immediate: true })

  const toggleSeniorMode = () => {
    seniorMode.value = !seniorMode.value
  }

  const setSeniorMode = (value: boolean) => {
    seniorMode.value = value
  }

  return {
    seniorMode,
    toggleSeniorMode,
    setSeniorMode
  }
})
