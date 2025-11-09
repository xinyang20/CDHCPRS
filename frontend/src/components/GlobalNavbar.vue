<template>
  <header class="global-navbar">
    <div class="navbar-container">
      <div class="navbar-left">
        <router-link to="/" class="brand">
          <img
            v-if="websiteLogo"
            :src="websiteLogo"
            alt="Logo"
            class="brand-logo"
          />
          <span class="brand-name">{{ websiteName }}</span>
        </router-link>
      </div>

      <nav class="navbar-center">
        <el-dropdown @command="handleNavigate">
          <el-button type="text" class="nav-dropdown-button">
            <el-icon><Menu /></el-icon>
            {{ t('common.menu') }}
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="/" :icon="HomeFilled">
                {{ t('home.nav.home') }}
              </el-dropdown-item>
              <el-dropdown-item command="/about" :icon="InfoFilled">
                {{ t('home.nav.about') }}
              </el-dropdown-item>
              <el-dropdown-item
                v-if="userStore.isAuthenticated()"
                command="/chat"
                :icon="ChatDotRound"
              >
                {{ t('chat.title') }}
              </el-dropdown-item>
              <el-dropdown-item
                v-if="userStore.isAuthenticated()"
                command="/profile"
                :icon="User"
              >
                {{ t('profile.title') }}
              </el-dropdown-item>
              <el-dropdown-item
                v-if="userStore.isAdmin()"
                command="/admin"
                :icon="Setting"
                divided
              >
                {{ t('chat.userMenu.admin') }}
              </el-dropdown-item>
              <el-dropdown-item
                v-if="!userStore.isAuthenticated()"
                command="/login"
                :icon="User"
                divided
              >
                {{ t('home.nav.login') }}
              </el-dropdown-item>
              <el-dropdown-item
                v-if="!userStore.isAuthenticated()"
                command="/register"
                :icon="UserFilled"
              >
                {{ t('home.nav.register') }}
              </el-dropdown-item>
              <el-dropdown-item
                v-if="userStore.isAuthenticated()"
                command="logout"
                :icon="SwitchButton"
                divided
              >
                {{ t('common.actions.logout') }}
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </nav>

      <div class="navbar-right">
        <LargeFontModeSwitcher />
        <LanguageSwitcher />
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import {
  Menu,
  ArrowDown,
  HomeFilled,
  InfoFilled,
  ChatDotRound,
  User,
  UserFilled,
  Setting,
  SwitchButton
} from '@element-plus/icons-vue'
import { useUserStore } from '../stores/user'
import LargeFontModeSwitcher from './LargeFontModeSwitcher.vue'
import LanguageSwitcher from './LanguageSwitcher.vue'
import api from '../api'

const { t } = useI18n()
const router = useRouter()
const userStore = useUserStore()

const websiteName = ref('')
const websiteLogo = ref('')

const handleNavigate = (command: string) => {
  if (command === 'logout') {
    userStore.logout()
    router.push('/login')
  } else {
    router.push(command)
  }
}

onMounted(async () => {
  try {
    const res = await api.get('/api/public/settings')
    websiteName.value = res.data.website_name || t('common.appName')
    websiteLogo.value = res.data.website_logo || ''
  } catch (error) {
    console.error('Failed to fetch site settings:', error)
    websiteName.value = t('common.appName')
  }
})
</script>

<style scoped>
.global-navbar {
  background: var(--color-bgPrimary);
  border-bottom: 1px solid var(--color-borderLight);
  padding: var(--spacing-md) 0;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.navbar-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--spacing-lg);
}

.navbar-left {
  flex: 0 0 auto;
}

.brand {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  text-decoration: none;
  color: var(--color-textPrimary);
  font-weight: 600;
  font-size: var(--font-size-lg);
}

.brand-logo {
  height: 32px;
  width: auto;
  object-fit: contain;
}

.brand-name {
  white-space: nowrap;
}

.navbar-center {
  flex: 1 1 auto;
  display: flex;
  justify-content: center;
}

.nav-dropdown-button {
  font-size: var(--font-size-base);
  color: var(--color-textPrimary);
}

.navbar-right {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

@media (max-width: 768px) {
  .brand-name {
    display: none;
  }
}
</style>
