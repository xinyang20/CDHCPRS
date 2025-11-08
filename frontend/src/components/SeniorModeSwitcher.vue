<template>
  <div class="senior-mode-switcher">
    <span class="label">{{ t('seniorMode.label') }}</span>
    <el-switch
      v-model="isSeniorMode"
      size="small"
      :active-text="t('seniorMode.on')"
      :inactive-text="t('seniorMode.off')"
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

const isSeniorMode = computed({
  get: () => settingsStore.seniorMode,
  set: (value: boolean) => settingsStore.setSeniorMode(value)
})
</script>

<style scoped>
.senior-mode-switcher {
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
