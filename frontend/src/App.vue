<template>
  <div id="app">
    <GlobalNavbar v-if="shouldShowNav" />
    <main class="main-content">
      <router-view />
    </main>
    <GlobalFooter v-if="shouldShowNav" />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useSettingsStore } from './stores/settings'
import GlobalNavbar from './components/GlobalNavbar.vue'
import GlobalFooter from './components/GlobalFooter.vue'
import api from './api'

const route = useRoute()

// 初始化设置store，确保页面加载时应用正确的大字版样式
const settingsStore = useSettingsStore()

// 从后端获取大字版倍率配置
onMounted(async () => {
  try {
    const res = await api.get('/api/public/settings')
    if (res.data.large_font_scale) {
      settingsStore.setLargeFontScale(res.data.large_font_scale)
    }
  } catch (error) {
    console.error('Failed to fetch large font scale setting:', error)
  }
})

// 监听路由变化，在 /admin 页面禁用大字版
watch(() => route.path, () => {
  const isAdminPage = route.path === '/admin'
  if (isAdminPage) {
    document.documentElement.classList.remove('large-font-mode')
  } else if (settingsStore.largeFontMode) {
    // 重新应用大字版样式
    const baseFontSize = 16
    const scaledSize = baseFontSize * settingsStore.largeFontScale
    document.documentElement.style.setProperty('--large-font-size', `${scaledSize}px`)
    document.documentElement.classList.add('large-font-mode')
  }
}, { immediate: true })

// 所有页面都显示导航栏
const shouldShowNav = computed(() => {
  return true
})
</script>

<style>
#app {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  overflow-x: hidden;
}

/* 首页和关于页可以滚动 */
.main-content:has(.home-page),
.main-content:has(.about-page) {
  overflow-y: auto;
}

/* 其他页面内容应该在容器内自行处理滚动 */
.main-content:not(:has(.home-page)):not(:has(.about-page)) {
  overflow-y: hidden;
}
</style>
