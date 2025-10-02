<template>
  <router-view />
  <LanguageSwitcher />
</template>

<script setup lang="ts">
import LanguageSwitcher from "./components/LanguageSwitcher.vue";
</script>

<style>
#app {
  width: 100%;
  height: 100vh;
}
</style>
