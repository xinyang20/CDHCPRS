<template>
  <div class="auth-container">
    <div class="language-switcher-wrapper">
      <LargeFontModeSwitcher />
      <LanguageSwitcher />
    </div>
    <el-card class="auth-card">
      <template #header>
        <div class="card-header">
          <h2>{{ websiteName }}</h2>
          <p>{{ t("auth.login.title") }}</p>
        </div>
      </template>

      <el-form :model="loginForm" :rules="rules" ref="formRef">
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            :placeholder="t('auth.login.username')"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            :placeholder="t('auth.login.password')"
            prefix-icon="Lock"
            size="large"
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="full-width"
            :loading="loading"
            @click="handleLogin"
          >
            {{ t("auth.login.submit") }}
          </el-button>
        </el-form-item>

        <el-form-item>
          <el-button
            size="large"
            class="full-width"
            @click="$router.push('/register')"
          >
            {{ t("auth.login.register") }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";
import { authAPI } from "../api/auth";
import { useUserStore } from "../stores/user";
import api from "../api";
import LanguageSwitcher from "../components/LanguageSwitcher.vue";
import LargeFontModeSwitcher from "../components/LargeFontModeSwitcher.vue";

const { t } = useI18n();
const router = useRouter();
const userStore = useUserStore();

const formRef = ref<FormInstance>();
const loading = ref(false);
const websiteName = ref(t("common.appName"));

const loginForm = reactive({
  username: "",
  password: "",
});

const rules: FormRules = {
  username: [
    {
      required: true,
      message: t("auth.login.usernameRequired"),
      trigger: "blur",
    },
  ],
  password: [
    {
      required: true,
      message: t("auth.login.passwordRequired"),
      trigger: "blur",
    },
  ],
};

const handleLogin = async () => {
  if (!formRef.value) return;

  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true;
      try {
        const res = await authAPI.login(loginForm.username, loginForm.password);
        userStore.setToken(res.data.access_token);

        const userRes = await authAPI.getCurrentUser();
        userStore.setUser(userRes.data);

        ElMessage.success(t("messages.loginSuccess"));
        router.push("/chat");
      } catch (error) {
        console.error("Login failed:", error);
        ElMessage.error(t("messages.loginFailed"));
      } finally {
        loading.value = false;
      }
    }
  });
};

onMounted(async () => {
  try {
    const res = await api.get("/api/public/settings");
    websiteName.value = res.data.website_name || t("common.appName");
  } catch (error) {
    console.error("Failed to fetch site settings:", error);
  }
});
</script>

<style scoped>
.auth-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100vh;
  background: linear-gradient(
    135deg,
    var(--color-primary) 0%,
    var(--color-primaryLight) 100%
  );
  overflow: hidden;
  position: relative;
}

.language-switcher-wrapper {
  position: absolute;
  top: var(--spacing-xl);
  right: var(--spacing-xl);
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
}

.auth-card {
  width: 100%;
  max-width: 420px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0 0 var(--spacing-md) 0;
  color: var(--color-primary);
  font-size: var(--font-size-2xl);
  font-weight: 600;
}

.card-header p {
  margin: 0;
  color: var(--color-textSecondary);
  font-size: var(--font-size-base);
}

.full-width {
  width: 100%;
}

:deep(.el-button) {
  font-weight: 500;
  transition: all var(--transition-base);
}
</style>
