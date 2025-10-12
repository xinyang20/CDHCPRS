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
  position: static;
  background: transparent;
  padding: 0;
  box-shadow: none;
  backdrop-filter: none;
}

.language-select {
  width: 110px;
}
</style>
