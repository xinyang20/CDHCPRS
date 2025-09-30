<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>{{ websiteName }}</h2>
          <p>用户登录</p>
        </div>
      </template>

      <el-form :model="loginForm" :rules="rules" ref="formRef">
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            size="large"
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            style="width: 100%"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>

        <el-form-item>
          <el-button
            size="large"
            style="width: 100%"
            @click="$router.push('/register')"
          >
            注册账号
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";
import { authAPI } from "../api/auth";
import { useUserStore } from "../stores/user";
import api from "../api";

const router = useRouter();
const userStore = useUserStore();
const formRef = ref<FormInstance>();
const loading = ref(false);
const websiteName = ref("慢性病诊疗方案推荐系统");

const loginForm = reactive({
  username: "",
  password: "",
});

const rules: FormRules = {
  username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }],
};

const handleLogin = async () => {
  if (!formRef.value) return;

  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true;
      try {
        const res = await authAPI.login(loginForm.username, loginForm.password);
        userStore.setToken(res.data.access_token);

        // 获取用户信息
        const userRes = await authAPI.getCurrentUser();
        userStore.setUser(userRes.data);

        ElMessage.success("登录成功");
        router.push("/chat");
      } catch (error) {
        console.error("登录失败:", error);
      } finally {
        loading.value = false;
      }
    }
  });
};

// 获取网站名称
onMounted(async () => {
  try {
    const res = await api.get("/api/public/settings");
    websiteName.value = res.data.website_name;
  } catch (error) {
    console.error("获取网站设置失败:", error);
  }
});
</script>

<style scoped>
.login-container {
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

.login-card {
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

:deep(.el-button) {
  font-weight: 500;
  transition: all var(--transition-base);
}
</style>
