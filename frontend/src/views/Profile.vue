<template>
  <div class="profile-container">
    <BackendStatus />

    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <h2>{{ t('profile.title') }}</h2>
          <el-button @click="$router.back()">{{ t('common.actions.back') }}</el-button>
        </div>
      </template>

      <el-descriptions :column="1" border>
        <el-descriptions-item :label="t('auth.login.username')">
          {{ userStore.user?.username }}
        </el-descriptions-item>
        <el-descriptions-item :label="t('profile.title')">
          {{ userStore.user?.role === 'admin' ? t('profile.roleAdmin') : t('profile.roleUser') }}
        </el-descriptions-item>
        <el-descriptions-item :label="t('profile.registeredAt')">
          {{ formatDate(userStore.user?.created_at) }}
        </el-descriptions-item>
      </el-descriptions>

      <el-divider />

      <h3>{{ t('profile.changePassword') }}</h3>
      <el-form
        :model="passwordForm"
        :rules="rules"
        ref="formRef"
        label-width="120px"
        class="password-form"
      >
        <el-form-item prop="password" :label="t('profile.newPassword')">
          <el-input
            v-model="passwordForm.password"
            type="password"
            :placeholder="t('profile.passwordPlaceholder')"
          />
        </el-form-item>

        <el-form-item prop="confirmPassword" :label="t('profile.confirmPassword')">
          <el-input
            v-model="passwordForm.confirmPassword"
            type="password"
            :placeholder="t('profile.confirmPasswordPlaceholder')"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            @click="handleUpdatePassword"
          >
            {{ t('profile.update') }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { ElMessage } from "element-plus";
import type { FormInstance, FormItemRule, FormRules } from "element-plus";
import { useUserStore } from "../stores/user";
import { authAPI } from "../api/auth";
import BackendStatus from "../components/BackendStatus.vue";

const { t, locale } = useI18n();
const userStore = useUserStore();

const formRef = ref<FormInstance>();
const loading = ref(false);

const passwordForm = reactive({
  password: "",
  confirmPassword: "",
});

const validateConfirmPassword = (_rule: any, value: string, callback: (err?: Error) => void) => {
  if (value !== passwordForm.password) {
    callback(new Error(t("messages.passwordMismatch")));
  } else {
    callback();
  }
};

const rules: FormRules = {
  password: [
    { required: true, message: t("auth.register.passwordRequired"), trigger: "blur" },
    { min: 6, message: t("auth.register.passwordRule"), trigger: "blur" },
  ],
  confirmPassword: [
    { required: true, message: t("profile.confirmPasswordRequired"), trigger: "blur" },
    { validator: validateConfirmPassword, trigger: "blur" },
  ],
};

const toRuleArray = (rules: FormRules[string]): FormItemRule[] => {
  if (!rules) return []
  return Array.isArray(rules) ? [...rules] : [rules]
}

watch(locale, () => {
  toRuleArray(rules.password).forEach((rule, index) => {
    if (index === 0) rule.message = t('auth.register.passwordRequired');
    if (index === 1) rule.message = t('auth.register.passwordRule');
  });
  toRuleArray(rules.confirmPassword).forEach((rule, index) => {
    if (index === 0) rule.message = t('profile.confirmPasswordRequired');
  });
});

const handleUpdatePassword = async () => {
  if (!formRef.value) return;

  await formRef.value.validate(async (valid) => {
    if (!valid) return;
    loading.value = true;
    try {
      await authAPI.updatePassword(passwordForm.password);
      ElMessage.success(t("messages.passwordUpdateSuccess"));
      passwordForm.password = "";
      passwordForm.confirmPassword = "";
      formRef.value?.resetFields();
    } catch (error) {
      console.error("Failed to update password:", error);
      ElMessage.error(t("messages.passwordUpdateFailed"));
    } finally {
      loading.value = false;
    }
  });
};

const formatDate = (value?: string) => {
  if (!value) return "";
  return new Date(value).toLocaleString(locale.value, { hour12: false });
};
</script>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: var(--color-bgSecondary);
  padding: var(--spacing-xl);
}

.profile-card {
  width: 100%;
  max-width: 900px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  color: var(--color-primary);
  font-size: var(--font-size-2xl);
  font-weight: 600;
}

h3 {
  color: var(--color-textPrimary);
  margin-bottom: var(--spacing-lg);
  font-size: var(--font-size-lg);
  font-weight: 600;
}

.password-form {
  max-width: 500px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--color-textSecondary);
}

:deep(.el-descriptions__label) {
  font-weight: 500;
  color: var(--color-textSecondary);
}
</style>
