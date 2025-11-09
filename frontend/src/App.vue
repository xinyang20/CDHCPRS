<template>
  <router-view />
</template>

<script setup lang="ts">
import { useSettingsStore } from './stores/settings'

// 初始化设置store，确保页面加载时应用正确的老年版样式
// Store的watch会自动应用样式
useSettingsStore()
</script>

<style>
#app {
  width: 100%;
  height: 100vh;
}
</style>
