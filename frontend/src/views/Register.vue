<template>
  <div class="auth-container">
    <el-card class="auth-card">
      <template #header>
        <div class="card-header">
          <h2>{{ t("auth.register.title") }}</h2>
        </div>
      </template>

      <el-form :model="registerForm" :rules="rules" ref="formRef">
        <el-form-item prop="username">
          <el-input
            v-model="registerForm.username"
            :placeholder="t('auth.register.username')"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            :placeholder="t('auth.register.password')"
            prefix-icon="Lock"
            size="large"
            @keyup.enter="handleRegister"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="full-width"
            :loading="loading"
            @click="handleRegister"
          >
            {{ t("auth.register.submit") }}
          </el-button>
        </el-form-item>

        <el-form-item>
          <el-button
            size="large"
            class="full-width"
            @click="$router.push('/login')"
          >
            {{ t("auth.register.back") }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import type { FormInstance, FormItemRule, FormRules } from "element-plus";
import { authAPI } from "../api/auth";

const { t, locale } = useI18n();
const router = useRouter();

const formRef = ref<FormInstance>();
const loading = ref(false);

const registerForm = reactive({
  username: "",
  password: "",
});

const rules: FormRules = {
  username: [
    {
      required: true,
      message: t("auth.register.usernameRequired"),
      trigger: "blur",
    },
    {
      min: 3,
      max: 50,
      message: t("auth.register.usernameRule"),
      trigger: "blur",
    },
  ],
  password: [
    {
      required: true,
      message: t("auth.register.passwordRequired"),
      trigger: "blur",
    },
    { min: 6, message: t("auth.register.passwordRule"), trigger: "blur" },
  ],
};

const toRuleArray = (rules: FormRules[string]): FormItemRule[] => {
  if (!rules) return [];
  return Array.isArray(rules) ? [...rules] : [rules];
};

watch(locale, () => {
  toRuleArray(rules.username).forEach((rule, index) => {
    if (index === 0) rule.message = t("auth.register.usernameRequired");
    if (index === 1) rule.message = t("auth.register.usernameRule");
  });
  toRuleArray(rules.password).forEach((rule, index) => {
    if (index === 0) rule.message = t("auth.register.passwordRequired");
    if (index === 1) rule.message = t("auth.register.passwordRule");
  });
});

const handleRegister = async () => {
  if (!formRef.value) return;

  await formRef.value.validate(async (valid) => {
    if (!valid) return;
    loading.value = true;
    try {
      await authAPI.register(registerForm.username, registerForm.password);
      ElMessage.success(t("messages.registerSuccess"));
      router.push("/login");
    } catch (error) {
      console.error("Registration failed:", error);
      ElMessage.error(t("messages.registerFailed"));
    } finally {
      loading.value = false;
    }
  });
};
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
  margin: 0;
  color: var(--color-primary);
  font-size: var(--font-size-2xl);
  font-weight: 600;
}

.full-width {
  width: 100%;
}

:deep(.el-button) {
  font-weight: 500;
  transition: all var(--transition-base);
}
</style>
