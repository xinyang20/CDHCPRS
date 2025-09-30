<template>
  <div class="profile-container">
    <!-- 后端状态指示器 -->
    <BackendStatus />

    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <h2>个人信息</h2>
          <el-button @click="$router.back()">返回</el-button>
        </div>
      </template>

      <el-descriptions :column="1" border>
        <el-descriptions-item label="用户名">
          {{ userStore.user?.username }}
        </el-descriptions-item>
        <el-descriptions-item label="角色">
          {{ userStore.user?.role === "admin" ? "管理员" : "普通用户" }}
        </el-descriptions-item>
        <el-descriptions-item label="注册时间">
          {{ formatDate(userStore.user?.created_at) }}
        </el-descriptions-item>
      </el-descriptions>

      <el-divider />

      <h3>修改密码</h3>
      <el-form
        :model="passwordForm"
        :rules="rules"
        ref="formRef"
        label-width="100px"
        style="max-width: 500px"
      >
        <el-form-item label="新密码" prop="password">
          <el-input
            v-model="passwordForm.password"
            type="password"
            placeholder="请输入新密码（至少6个字符）"
          />
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="passwordForm.confirmPassword"
            type="password"
            placeholder="请再次输入新密码"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            @click="handleUpdatePassword"
          >
            修改密码
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { ElMessage } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";
import { useUserStore } from "../stores/user";
import { authAPI } from "../api/auth";
import BackendStatus from "../components/BackendStatus.vue";

const userStore = useUserStore();
const formRef = ref<FormInstance>();
const loading = ref(false);

const passwordForm = reactive({
  password: "",
  confirmPassword: "",
});

const validateConfirmPassword = (rule: any, value: any, callback: any) => {
  if (value !== passwordForm.password) {
    callback(new Error("两次输入的密码不一致"));
  } else {
    callback();
  }
};

const rules: FormRules = {
  password: [
    { required: true, message: "请输入新密码", trigger: "blur" },
    { min: 6, max: 100, message: "密码长度至少6个字符", trigger: "blur" },
  ],
  confirmPassword: [
    { required: true, message: "请再次输入新密码", trigger: "blur" },
    { validator: validateConfirmPassword, trigger: "blur" },
  ],
};

const handleUpdatePassword = async () => {
  if (!formRef.value) return;

  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true;
      try {
        await authAPI.updatePassword(passwordForm.password);
        ElMessage.success("密码修改成功");
        passwordForm.password = "";
        passwordForm.confirmPassword = "";
        formRef.value?.resetFields();
      } catch (error) {
        console.error("修改密码失败:", error);
      } finally {
        loading.value = false;
      }
    }
  });
};

const formatDate = (dateStr?: string) => {
  if (!dateStr) return "";
  return new Date(dateStr).toLocaleString("zh-CN");
};
</script>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  height: 100vh;
  background: var(--color-bgSecondary);
  padding: var(--spacing-xl);
  overflow-y: auto;
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

/* 确保表单项对齐 */
:deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--color-textSecondary);
}

:deep(.el-descriptions__label) {
  font-weight: 500;
  color: var(--color-textSecondary);
}
</style>
