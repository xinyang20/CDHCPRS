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
import { computed, onMounted } from 'vue'
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

// 决定是否显示导航栏（只在特定页面显示）
const shouldShowNav = computed(() => {
  const showNavPages = ['/', '/about', '/login', '/register']
  return showNavPages.includes(route.path)
})
</script>

<style>
#app {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>
