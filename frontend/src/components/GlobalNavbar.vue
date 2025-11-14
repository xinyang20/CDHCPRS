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
        <router-link to="/" class="nav-link">{{ t('home.nav.home') }}</router-link>
        <router-link to="/about" class="nav-link">{{ t('home.nav.about') }}</router-link>
        <router-link v-if="userStore.isAuthenticated()" to="/chat" class="nav-link">
          {{ t('chat.title') }}
        </router-link>
        <el-dropdown v-if="userStore.isAdmin()" trigger="hover" @command="handleAdminCommand" class="admin-dropdown">
          <span class="nav-link admin-link">
            {{ t('chat.userMenu.admin') }}
            <el-icon class="el-icon--right"><arrow-down /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="users">
                <el-icon><User /></el-icon>
                {{ t('admin.menu.users') }}
              </el-dropdown-item>
              <el-dropdown-item command="conversations">
                <el-icon><ChatDotRound /></el-icon>
                {{ t('admin.menu.conversations') }}
              </el-dropdown-item>
              <el-dropdown-item command="settings">
                <el-icon><Setting /></el-icon>
                {{ t('admin.menu.settings') }}
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </nav>

      <div class="navbar-right">
        <LargeFontModeSwitcher />
        <LanguageSwitcher />

        <router-link v-if="!userStore.isAuthenticated()" to="/login" class="login-button">
          {{ t('home.nav.login') }}
        </router-link>

        <el-dropdown v-if="userStore.isAuthenticated()" @command="handleCommand" trigger="click">
          <div class="user-avatar">
            <el-avatar :size="36" :style="{ background: 'var(--color-primary)' }">
              {{ userStore.user?.username?.charAt(0).toUpperCase() || 'U' }}
            </el-avatar>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item disabled>
                <div class="user-info">
                  <strong>{{ userStore.user?.username }}</strong>
                  <span class="user-role">{{ userStore.isAdmin() ? t('profile.roleAdmin') : t('profile.roleUser') }}</span>
                </div>
              </el-dropdown-item>
              <el-dropdown-item divided command="logout">
                <el-icon><SwitchButton /></el-icon>
                {{ t('common.actions.logout') }}
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ElMessageBox } from 'element-plus'
import { SwitchButton, ArrowDown, User, ChatDotRound, Setting } from '@element-plus/icons-vue'
import { useUserStore } from '../stores/user'
import LargeFontModeSwitcher from './LargeFontModeSwitcher.vue'
import LanguageSwitcher from './LanguageSwitcher.vue'
import api from '../api'

const { t } = useI18n()
const router = useRouter()
const userStore = useUserStore()

const websiteName = ref('')
const websiteLogo = ref('')

const handleAdminCommand = (command: string) => {
  router.push({ path: '/admin', query: { tab: command } })
}

const handleCommand = async (command: string) => {
  if (command === 'logout') {
    await handleLogout()
  }
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm(
      t('messages.logoutConfirm'),
      t('messages.confirmTitle'),
      {
        confirmButtonText: t('common.actions.confirm'),
        cancelButtonText: t('common.actions.cancel'),
        type: 'warning',
      }
    )
    userStore.logout()
    router.push('/login')
  } catch {
    // 用户取消登出
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
  gap: var(--spacing-lg);
  flex-wrap: wrap;
}

.nav-link {
  color: var(--color-textSecondary);
  text-decoration: none;
  font-size: var(--font-size-base);
  transition: color var(--transition-fast);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-sm);
}

.nav-link:hover {
  color: var(--color-primary);
  background: var(--color-bgSecondary);
}

.nav-link.router-link-active {
  color: var(--color-primary);
  font-weight: 600;
}

.navbar-right {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.login-button {
  padding: var(--spacing-sm) var(--spacing-lg);
  background: var(--color-primary);
  color: white;
  text-decoration: none;
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-base);
  transition: all var(--transition-fast);
}

.login-button:hover {
  background: var(--color-primaryDark);
  transform: translateY(-1px);
}

.user-avatar {
  cursor: pointer;
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  flex-direction: column;
  padding: var(--spacing-xs) 0;
}

.user-info strong {
  color: var(--color-textPrimary);
  font-size: var(--font-size-base);
}

.user-role {
  color: var(--color-textSecondary);
  font-size: var(--font-size-sm);
  margin-top: var(--spacing-xs);
}

.admin-dropdown {
  display: inline-flex;
  align-items: center;
}

.admin-link {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  cursor: pointer;
}

@media (max-width: 768px) {
  .brand-name {
    display: none;
  }

  .navbar-center {
    display: none;
  }
}
</style>
