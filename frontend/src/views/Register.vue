<template>
  <div class="register-container">
    <el-card class="register-card">
      <template #header>
        <div class="card-header">
          <h2>用户注册</h2>
        </div>
      </template>

      <el-form :model="registerForm" :rules="rules" ref="formRef">
        <el-form-item prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="请输入用户名（3-50个字符）"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码（至少6个字符）"
            prefix-icon="Lock"
            size="large"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            style="width: 100%"
            :loading="loading"
            @click="handleRegister"
          >
            注册
          </el-button>
        </el-form-item>

        <el-form-item>
          <el-button
            size="large"
            style="width: 100%"
            @click="$router.push('/login')"
          >
            返回登录
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";
import { authAPI } from "../api/auth";

const router = useRouter();
const formRef = ref<FormInstance>();
const loading = ref(false);

const registerForm = reactive({
  username: "",
  password: "",
});

const rules: FormRules = {
  username: [
    { required: true, message: "请输入用户名", trigger: "blur" },
    { min: 3, max: 50, message: "用户名长度为3-50个字符", trigger: "blur" },
  ],
  password: [
    { required: true, message: "请输入密码", trigger: "blur" },
    { min: 6, max: 100, message: "密码长度至少6个字符", trigger: "blur" },
  ],
};

const handleRegister = async () => {
  if (!formRef.value) return;

  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true;
      try {
        await authAPI.register(registerForm.username, registerForm.password);
        ElMessage.success("注册成功，请登录");
        router.push("/login");
      } catch (error) {
        console.error("注册失败:", error);
      } finally {
        loading.value = false;
      }
    }
  });
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100vh;
  background: linear-gradient(
    135deg,
    var(--color-primary) 0%,
    var(--color-primaryLight) 100%
  );
}

.register-card {
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

:deep(.el-button) {
  font-weight: 500;
  transition: all var(--transition-base);
}
</style>
