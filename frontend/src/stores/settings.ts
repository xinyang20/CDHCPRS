import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

const LARGE_FONT_MODE_KEY = 'cdhcprs_large_font_mode'

export const useSettingsStore = defineStore('settings', () => {
  // 从 localStorage 读取初始值
  const largeFontMode = ref<boolean>(
    localStorage.getItem(LARGE_FONT_MODE_KEY) === 'true'
  )

  // 大字版字体放大倍率（默认1.5，从后端获取）
  const largeFontScale = ref<number>(1.5)

  // 应用大字版样式
  const applyLargeFontStyle = () => {
    if (largeFontMode.value) {
      const baseFontSize = 16 // 基础字体大小
      const scaledSize = baseFontSize * largeFontScale.value
      document.documentElement.style.setProperty('--large-font-size', `${scaledSize}px`)
      document.documentElement.classList.add('large-font-mode')
    } else {
      document.documentElement.classList.remove('large-font-mode')
    }
  }

  // 监听变化并保存到 localStorage
  watch(largeFontMode, (newValue) => {
    localStorage.setItem(LARGE_FONT_MODE_KEY, String(newValue))
    applyLargeFontStyle()
  }, { immediate: true })

  // 监听倍率变化
  watch(largeFontScale, () => {
    applyLargeFontStyle()
  })

  const toggleLargeFontMode = () => {
    largeFontMode.value = !largeFontMode.value
  }

  const setLargeFontMode = (value: boolean) => {
    largeFontMode.value = value
  }

  const setLargeFontScale = (scale: number) => {
    largeFontScale.value = scale
  }

  return {
    largeFontMode,
    largeFontScale,
    toggleLargeFontMode,
    setLargeFontMode,
    setLargeFontScale
  }
})
