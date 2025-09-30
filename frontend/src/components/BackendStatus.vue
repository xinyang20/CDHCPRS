<template>
  <div class="backend-status" :class="{ 'status-error': !isHealthy }">
    <el-tooltip
      :content="tooltipContent"
      placement="top"
    >
      <div class="status-indicator">
        <div class="status-dot" :class="statusClass"></div>
        <span class="status-text">{{ statusText }}</span>
      </div>
    </el-tooltip>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import api from "../api";

const isHealthy = ref(true);
const lastCheckTime = ref<Date | null>(null);
const checkInterval = ref<number | null>(null);
const errorMessage = ref("");

// 健康检查间隔（毫秒）
const HEALTH_CHECK_INTERVAL = 30000; // 30秒

// 状态类名
const statusClass = computed(() => {
  return isHealthy.value ? "status-healthy" : "status-unhealthy";
});

// 状态文本
const statusText = computed(() => {
  return isHealthy.value ? "后端正常" : "后端异常";
});

// 提示内容
const tooltipContent = computed(() => {
  if (isHealthy.value) {
    return lastCheckTime.value
      ? `后端服务正常运行\n最后检查: ${lastCheckTime.value.toLocaleTimeString("zh-CN")}`
      : "后端服务正常运行";
  } else {
    return errorMessage.value || "后端服务连接失败，请检查服务是否启动";
  }
});

// 执行健康检查
const checkHealth = async () => {
  try {
    const response = await api.get("/api/health", {
      timeout: 5000, // 5秒超时
    });
    
    if (response.status === 200) {
      isHealthy.value = true;
      errorMessage.value = "";
    } else {
      isHealthy.value = false;
      errorMessage.value = "后端服务响应异常";
    }
  } catch (error: any) {
    isHealthy.value = false;
    if (error.code === "ECONNABORTED") {
      errorMessage.value = "后端服务响应超时";
    } else if (error.response) {
      errorMessage.value = `后端服务错误: ${error.response.status}`;
    } else if (error.request) {
      errorMessage.value = "无法连接到后端服务";
    } else {
      errorMessage.value = "健康检查失败";
    }
  } finally {
    lastCheckTime.value = new Date();
  }
};

// 启动定期健康检查
const startHealthCheck = () => {
  // 立即执行一次检查
  checkHealth();
  
  // 设置定期检查
  checkInterval.value = window.setInterval(() => {
    checkHealth();
  }, HEALTH_CHECK_INTERVAL);
};

// 停止健康检查
const stopHealthCheck = () => {
  if (checkInterval.value !== null) {
    clearInterval(checkInterval.value);
    checkInterval.value = null;
  }
};

// 组件挂载时启动健康检查
onMounted(() => {
  startHealthCheck();
});

// 组件卸载时停止健康检查
onUnmounted(() => {
  stopHealthCheck();
});
</script>

<style scoped>
.backend-status {
  position: fixed;
  bottom: var(--spacing-xl);
  right: var(--spacing-xl);
  z-index: 1000;
  background: var(--color-bgPrimary);
  border-radius: var(--border-radius-full);
  padding: var(--spacing-sm) var(--spacing-base);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all var(--transition-base);
}

.backend-status:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  cursor: pointer;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: var(--border-radius-full);
  position: relative;
  transition: all var(--transition-base);
}

.status-dot::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  border-radius: var(--border-radius-full);
  animation: pulse 2s ease-in-out infinite;
}

.status-healthy {
  background: var(--color-success);
}

.status-healthy::before {
  background: var(--color-success);
}

.status-unhealthy {
  background: var(--color-danger);
}

.status-unhealthy::before {
  background: var(--color-danger);
}

@keyframes pulse {
  0% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    opacity: 0.5;
    transform: translate(-50%, -50%) scale(1.5);
  }
  100% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(2);
  }
}

.status-text {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-textPrimary);
  white-space: nowrap;
}

.status-error .status-text {
  color: var(--color-danger);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .backend-status {
    bottom: var(--spacing-base);
    right: var(--spacing-base);
    padding: var(--spacing-xs) var(--spacing-sm);
  }

  .status-text {
    display: none;
  }

  .status-dot {
    width: 12px;
    height: 12px;
  }
}
</style>

