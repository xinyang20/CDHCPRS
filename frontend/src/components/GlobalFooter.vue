<template>
  <footer class="global-footer">
    <div class="footer-container">
      <div class="footer-content">
        <p class="footer-text">
          © {{ currentYear }} {{ websiteName }}. All rights reserved.
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '../api'

const { t } = useI18n()

const websiteName = ref('')
const currentYear = computed(() => new Date().getFullYear())

onMounted(async () => {
  try {
    const res = await api.get('/api/public/settings')
    websiteName.value = res.data.website_name || t('common.appName')
  } catch (error) {
    console.error('Failed to fetch site settings:', error)
    websiteName.value = t('common.appName')
  }
})
</script>

<style scoped>
.global-footer {
  background: var(--color-bgSecondary);
  border-top: 1px solid var(--color-borderLight);
  padding: 0;
  margin-top: auto;
}

.footer-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0;
}

.footer-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.footer-text {
  color: var(--color-textSecondary);
  font-size: var(--font-size-sm);
  margin: 0;
}

.footer-links {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.footer-link {
  color: var(--color-textTertiary);
  text-decoration: none;
  font-size: var(--font-size-sm);
  transition: color var(--transition-fast);
}

.footer-link:hover {
  color: var(--color-primary);
}

.footer-separator {
  color: var(--color-textTertiary);
}
</style>
