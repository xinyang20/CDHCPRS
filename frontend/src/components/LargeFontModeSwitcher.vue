<template>
  <div class="large-font-mode-switcher">
    <span class="label">{{ t('largeFontMode.label') }}</span>
    <el-switch
      v-model="isLargeFontMode"
      size="small"
      :active-text="t('largeFontMode.on')"
      :inactive-text="t('largeFontMode.off')"
      inline-prompt
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useSettingsStore } from '../stores/settings'

const { t } = useI18n()
const settingsStore = useSettingsStore()

const isLargeFontMode = computed({
  get: () => settingsStore.largeFontMode,
  set: (value: boolean) => settingsStore.setLargeFontMode(value)
})
</script>

<style scoped>
.large-font-mode-switcher {
  display: flex;
  align-items: center;
  gap: 12px;
}

.label {
  font-size: var(--font-size-sm);
  color: var(--color-textPrimary);
  white-space: nowrap;
}
</style>
