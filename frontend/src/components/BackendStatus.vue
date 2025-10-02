<template>
  <div class="backend-status" :class="{ 'status-error': !isHealthy }">
    <el-tooltip :content="tooltipContent" placement="top">
      <div class="status-indicator">
        <div class="status-dot" :class="statusClass"></div>
        <span class="status-text">{{ statusText }}</span>
      </div>
    </el-tooltip>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";
import { useI18n } from "vue-i18n";
import api from "../api";

const { t, locale } = useI18n();

const isHealthy = ref(true);
const lastCheckTime = ref<Date | null>(null);
const checkInterval = ref<number | null>(null);
const errorMessage = ref("");

const HEALTH_CHECK_INTERVAL = 30000;

const statusClass = computed(() => {
  return isHealthy.value ? "status-healthy" : "status-unhealthy";
});

const statusText = computed(() => {
  return isHealthy.value
    ? t("statusMessages.backendHealthy")
    : t("statusMessages.backendUnhealthy");
});

const tooltipContent = computed(() => {
  if (isHealthy.value) {
    const last = lastCheckTime.value;
    if (last) {
      const time = last.toLocaleTimeString(locale.value);
      return `${t("statusMessages.backendOkDetail")}` + `
${t("statusMessages.lastCheck", { time })}`;
    }
    return t("statusMessages.backendOkDetail");
  }
  return errorMessage.value || t("statusMessages.backendErrorDetail");
});

const checkHealth = async () => {
  try {
    const response = await api.get("/api/health", {
      timeout: 5000,
    });

    if (response.status === 200) {
      isHealthy.value = true;
      errorMessage.value = "";
    } else {
      isHealthy.value = false;
      errorMessage.value = t("statusMessages.backendErrorDetail");
    }
  } catch (error: any) {
    isHealthy.value = false;
    if (error.code === "ECONNABORTED") {
      errorMessage.value = t("statusMessages.backendErrorDetail");
    } else if (error.response) {
      errorMessage.value = `${t("statusMessages.backendErrorDetail")}: ${error.response.status}`;
    } else if (error.request) {
      errorMessage.value = t("statusMessages.backendErrorDetail");
    } else {
      errorMessage.value = t("statusMessages.backendErrorDetail");
    }
  } finally {
    lastCheckTime.value = new Date();
  }
};

const startHealthCheck = () => {
  checkHealth();
  checkInterval.value = window.setInterval(() => {
    checkHealth();
  }, HEALTH_CHECK_INTERVAL);
};

const stopHealthCheck = () => {
  if (checkInterval.value !== null) {
    clearInterval(checkInterval.value);
    checkInterval.value = null;
  }
};

onMounted(() => {
  startHealthCheck();
});

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

@media (max-width: 768px) {
  .backend-status {
    bottom: var(--spacing-base);
    right: var(--spacing-base);
    padding: var(--spacing-xs) var(--spacing-sm);
  }
}
</style>
