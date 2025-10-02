<template>
  <div class="language-switcher">
    <el-select
      v-model="selectedLocale"
      size="small"
      class="language-select"
      :teleported="false"
    >
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { availableLocales, setLocale, type AppLocale } from "../i18n";

const { locale } = useI18n();

const options = availableLocales;

const selectedLocale = computed({
  get: () => locale.value as AppLocale,
  set: (value: AppLocale) => {
    setLocale(value);
  },
});
</script>

<style scoped>
.language-switcher {
  position: fixed;
  bottom: var(--spacing-xl);
  left: var(--spacing-xl);
  z-index: 1100;
  background: rgba(255, 255, 255, 0.92);
  border-radius: var(--border-radius-full);
  padding: 4px 12px;
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.12);
  backdrop-filter: blur(12px);
}

.language-select {
  width: 130px;
}

@media (max-width: 768px) {
  .language-switcher {
    bottom: var(--spacing-base);
    left: var(--spacing-base);
  }

  .language-select {
    width: 110px;
  }
}
</style>
