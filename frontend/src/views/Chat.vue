<template>
  <div class="chat-layout">
    <BackendStatus />

    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="brand">
          <h2>{{ websiteName }}</h2>
          <p class="brand-subtitle">{{ t('chat.sidebarTagline') }}</p>
        </div>
        <el-button type="primary" @click="createNewConversation(true)" :icon="Plus">
          {{ t('chat.newConversation') }}
        </el-button>
      </div>

      <el-scrollbar class="conversation-scroll">
        <div
          v-for="conv in conversations"
          :key="conv.id"
          :class="[
            'conversation-item',
            {
              active: currentConversationId === conv.id,
              inactive: !conv.is_active,
            },
          ]"
          @click="selectConversation(conv.id)"
        >
          <div class="conversation-meta">
            <div class="conversation-title">
              <el-icon><ChatDotRound /></el-icon>
              <span class="title-text">{{ conv.title }}</span>
              <el-tag
                v-if="!conv.is_active"
                size="small"
                type="warning"
                effect="plain"
              >{{ t('common.status.disabled') }}</el-tag>
            </div>
            <span class="conversation-time">{{ formatDate(conv.created_at) }}</span>
          </div>
          <div class="conversation-actions" @click.stop>
            <el-tooltip :content="t('common.actions.delete')" placement="top">
              <el-button
                text
                type="danger"
                size="small"
                :icon="Delete"
                @click="deleteConv(conv.id)"
              />
            </el-tooltip>
          </div>
        </div>
      </el-scrollbar>

      <div class="sidebar-footer">
        <el-dropdown trigger="click">
          <span class="user-info">
            <el-avatar size="small" icon="User" />
            <span class="user-name">{{ userStore.user?.username }}</span>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="$router.push('/profile')">
                {{ t('chat.userMenu.profile') }}
              </el-dropdown-item>
              <el-dropdown-item
                v-if="userStore.isAdmin()"
                @click="$router.push('/admin')"
              >
                {{ t('chat.userMenu.admin') }}
              </el-dropdown-item>
              <el-dropdown-item divided @click="handleLogout">
                {{ t('chat.userMenu.logout') }}
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </aside>

    <main class="main-content">
      <div v-if="!currentConversationId" class="welcome">
        <div class="welcome-card">
          <h1>{{ t('chat.welcomeTitle') }}</h1>
          <p>{{ t('chat.welcomeSubtitle') }}</p>
          <div class="welcome-actions">
            <el-button type="primary" size="large" @click="createNewConversation(true)">
              <el-icon><Plus /></el-icon>
              {{ t('chat.newConversation') }}
            </el-button>
            <el-button size="large" @click="loadConversations">{{ t('chat.refresh') }}</el-button>
          </div>
        </div>
      </div>

      <div v-else class="chat-area">
        <header class="chat-header">
          <div class="chat-title">
            <h1>{{ currentConversation?.title }}</h1>
            <el-tag v-if="!currentConversation?.is_active" type="warning" effect="plain">
              {{ t('common.status.disabled') }}
            </el-tag>
          </div>
          <div class="chat-actions">
            <el-button text size="small" :icon="Refresh" @click="refreshConversation">
              {{ t('chat.refresh') }}
            </el-button>
            <el-button text size="small" :icon="User" @click="openInfoDialog">
              {{ t('chat.patientProfile') }}
            </el-button>
          </div>
        </header>

        <section class="patient-info-card">
          <div class="card-header">
            <div>
              <h3>{{ t('chat.patientProfile') }}</h3>
              <p class="card-subtitle">{{ t('chat.patientProfileHint') }}</p>
            </div>
            <el-button type="primary" text :icon="EditPen" @click="openInfoDialog">
              {{ t('chat.updateInfo') }}
            </el-button>
          </div>

          <div v-if="hasPatientInfo" class="info-body">
            <el-descriptions :column="3" border size="small">
              <el-descriptions-item label="{{ t('chat.age') }}">
                {{ currentProfile.age || t('chat.fillInfo') }}
              </el-descriptions-item>
              <el-descriptions-item label="{{ t('chat.gender') }}">
                {{ genderLabel(currentProfile.gender) }}
              </el-descriptions-item>
              <el-descriptions-item label="{{ t('chat.chiefComplaint') }}">
                {{ currentProfile.mainComplaint || t('chat.fillInfo') }}
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <div v-else class="info-empty">
            <el-empty description="{{ t('chat.fillInfo') }}">
              <el-button type="primary" link @click="openInfoDialog">
                {{ t('chat.fillInfo') }}
              </el-button>
            </el-empty>
          </div>
        </section>

        <div class="message-list" ref="messageListRef">
          <div
            v-for="msg in messages"
            :key="msg.id"
            :class="['message', msg.role]"
          >
            <div class="message-avatar">
              <el-icon v-if="msg.role === 'user'"><User /></el-icon>
              <el-icon v-else><ChatDotRound /></el-icon>
            </div>
            <div class="message-content">
              <MarkdownRenderer :content="msg.content" />
              <span class="message-time">{{ formatDate(msg.created_at) }}</span>
            </div>
          </div>

          <div v-if="isStreaming" class="message assistant">
            <div class="message-avatar">
              <el-icon><ChatDotRound /></el-icon>
            </div>
            <div class="message-content streaming">
              <MarkdownRenderer :content="streamingContent" />
              <el-icon class="loading-icon"><Loading /></el-icon>
            </div>
          </div>
        </div>

        <footer class="input-area" :class="{ 'disabled-conversation': currentConversation && !currentConversation.is_active }">
          <el-alert
            v-if="currentConversation && !currentConversation.is_active"
            :title="t('chat.conversationDisabled')"
            type="warning"
            :closable="false"
            class="mb-base"
          >
            <template #default>
              <p>{{ t('chat.conversationDisabledDetail') }}</p>
              <el-button
                type="primary"
                size="small"
                :icon="Plus"
                @click="createNewConversation(true)"
                class="mt-sm"
              >
                {{ t('chat.createNewConversation') }}
              </el-button>
            </template>
          </el-alert>

          <el-input
            v-model="inputMessage"
            type="textarea"
            :rows="4"
            :placeholder="t('chat.questionPlaceholder')"
            :disabled="!currentConversation?.is_active || isStreaming"
            @keydown.enter.ctrl.prevent="sendMessage"
          />
          <div class="input-actions">
            <span class="tip">Ctrl + Enter {{ t('chat.send') }}</span>
            <div class="action-buttons">
              <el-button
                text
                size="small"
                :icon="EditPen"
                @click="openInfoDialog"
                :disabled="!currentConversation?.is_active"
              >
                {{ t('chat.updateInfo') }}
              </el-button>
              <el-button
                type="primary"
                :loading="isStreaming"
                :disabled="!inputMessage.trim() || !currentConversation?.is_active"
                @click="sendMessage"
              >
                {{ t('chat.send') }}
              </el-button>
            </div>
          </div>
        </footer>
      </div>
    </main>

    <el-dialog
      v-model="infoDialogVisible"
      title="{{ t('chat.infoDialogTitle') }}"
      width="520px"
      destroy-on-close
    >
      <el-form ref="infoFormRef" :model="infoForm" :rules="infoRules" label-width="90px">
        <el-form-item label="{{ t('chat.age') }}" prop="age">
          <el-input v-model="infoForm.age" :placeholder="t('chat.age')" maxlength="3" />
        </el-form-item>
        <el-form-item label="{{ t('chat.gender') }}" prop="gender">
          <el-radio-group v-model="infoForm.gender">
            <el-radio label="male">{{ t('chat.genderMale') }}</el-radio>
            <el-radio label="female">{{ t('chat.genderFemale') }}</el-radio>
            <el-radio label="other">{{ t('chat.genderOther') }}</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="{{ t('chat.chiefComplaint') }}" prop="mainComplaint">
          <el-input
            v-model="infoForm.mainComplaint"
            type="textarea"
            :rows="4"
            maxlength="400"
            show-word-limit
            :placeholder="t('chat.chiefComplaintPlaceholder')"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="skipInfoDialog">{{ t('chat.infoSkip') }}</el-button>
          <el-button text type="danger" @click="clearInfoForm">{{ t('chat.infoClear') }}</el-button>
          <el-button type="primary" @click="savePatientInfo">{{ t('chat.infoSave') }}</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>


<script setup lang="ts">
import { computed, nextTick, onMounted, reactive, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import {
  Plus,
  Delete,
  User,
  ChatDotRound,
  Loading,
  EditPen,
  Refresh,
} from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";

import api from "../api";
import { chatAPI } from "../api/chat";
import { useUserStore } from "../stores/user";
import BackendStatus from "../components/BackendStatus.vue";
import MarkdownRenderer from "../components/MarkdownRenderer.vue";

interface ConversationItem {
  id: number;
  title: string;
  user_id: number;
  is_active: boolean;
  created_at: string;
}

interface MessageItem {
  id: number;
  conversation_id: number;
  role: "user" | "assistant";
  content: string;
  created_at: string;
}

interface PatientProfile {
  age: string;
  gender: string;
  mainComplaint: string;
}

const PROFILE_STORAGE_KEY = "cdhcprs_conversation_profiles";

const buildDefaultProfile = (): PatientProfile => ({
  age: "",
  gender: "",
  mainComplaint: "",
});

const router = useRouter();
const userStore = useUserStore();
const { t, locale } = useI18n();

const websiteName = ref(t("common.appName"));
const conversations = ref<ConversationItem[]>([]);
const currentConversationId = ref<number | null>(null);
const messages = ref<MessageItem[]>([]);
const isStreaming = ref(false);
const streamingContent = ref("");
const inputMessage = ref("");
const messageListRef = ref<HTMLElement>();

const conversationProfiles = ref<Record<number, PatientProfile>>({});
const infoDialogVisible = ref(false);
const infoFormRef = ref<FormInstance>();
const infoForm = reactive<PatientProfile>(buildDefaultProfile());
const shouldAttachUserInfo = ref(false);

const infoRules: FormRules = {
  age: [
    {
      validator: (_rule, value, callback) => {
        if (!value) {
          callback();
          return;
        }
        const num = Number(value);
        if (!Number.isInteger(num) || num < 0 || num > 120) {
          callback(new Error(t("chat.ageError")));
          return;
        }
        callback();
      },
      trigger: "blur",
    },
  ],
  mainComplaint: [
    {
      validator: (_rule, value, callback) => {
        if (value && value.length < 4) {
          callback(new Error(t("chat.chiefComplaintError")));
          return;
        }
        callback();
      },
      trigger: "blur",
    },
  ],
};

const currentConversation = computed(() =>
  conversations.value.find((item) => item.id === currentConversationId.value) || null
);

const currentProfile = computed<PatientProfile>(() => {
  const id = currentConversationId.value;
  if (!id) {
    return buildDefaultProfile();
  }
  if (!conversationProfiles.value[id]) {
    conversationProfiles.value[id] = buildDefaultProfile();
  }
  return conversationProfiles.value[id];
});

const hasPatientInfo = computed(() => {
  const profile = currentProfile.value;
  return [profile.age, profile.gender, profile.mainComplaint].some((v) => v && v.trim());
});

const genderLabel = (gender: string) => {
  if (gender === "male") return t("chat.genderMale");
  if (gender === "female") return t("chat.genderFemale");
  if (gender === "other") return t("chat.genderOther");
  return t("chat.fillInfo");
};

const formatDate = (value?: string) => {
  if (!value) return "";
  return new Date(value).toLocaleString(locale.value, {
    hour12: false,
  });
};

const scrollToBottom = async () => {
  await nextTick();
  if (messageListRef.value) {
    messageListRef.value.scrollTop = messageListRef.value.scrollHeight;
  }
};

const persistProfiles = () => {
  localStorage.setItem(
    PROFILE_STORAGE_KEY,
    JSON.stringify(conversationProfiles.value)
  );
};

const restoreProfiles = () => {
  try {
    const raw = localStorage.getItem(PROFILE_STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw) as Record<number, PatientProfile>;
      conversationProfiles.value = parsed;
    }
  } catch (error) {
    console.error("Failed to restore patient profile", error);
  }
};

watch(
  conversationProfiles,
  () => {
    persistProfiles();
  },
  { deep: true }
);

const prepareInfoForm = () => {
  Object.assign(infoForm, buildDefaultProfile(), currentProfile.value);
};

const openInfoDialog = () => {
  if (!currentConversationId.value) {
    ElMessage.warning(t("messages.selectConversationWarning"));
    return;
  }
  prepareInfoForm();
  infoDialogVisible.value = true;
};

const skipInfoDialog = () => {
  infoDialogVisible.value = false;
  if (messages.value.length === 0) {
    shouldAttachUserInfo.value = hasPatientInfo.value;
  }
};

const clearInfoForm = () => {
  Object.assign(infoForm, buildDefaultProfile());
};

const savePatientInfo = async () => {
  if (!currentConversationId.value) {
    ElMessage.warning(t("messages.needSelectConversation"));
    return;
  }
  if (!infoFormRef.value) {
    return;
  }
  await infoFormRef.value.validate(async (valid) => {
    if (!valid) return;
    conversationProfiles.value[currentConversationId.value!] = {
      age: infoForm.age.trim(),
      gender: infoForm.gender,
      mainComplaint: infoForm.mainComplaint.trim(),
    };
    infoDialogVisible.value = false;
    shouldAttachUserInfo.value = true;
    ElMessage.success(t("chat.infoSaved"));
  });
};

const formatUserInfoForPrompt = (profile: PatientProfile) => {
  return [
    `${t('chat.age')}: ${profile.age || t('chat.fillInfo')}`,
    `${t('chat.gender')}: ${genderLabel(profile.gender)}`,
    `${t('chat.chiefComplaint')}: ${profile.mainComplaint || t('chat.fillInfo')}`,
  ].join("\n");
};

const loadConversations = async () => {
  try {
    const res = await chatAPI.getConversations();
    conversations.value = res.data;
  } catch (error) {
    console.error("Failed to load conversations:", error);
  }
};

const loadMessages = async (conversationId: number) => {
  try {
    const res = await chatAPI.getMessages(conversationId);
    messages.value = res.data;
    await scrollToBottom();
    if (messages.value.length === 0 && hasPatientInfo.value) {
      shouldAttachUserInfo.value = true;
    }
  } catch (error) {
    console.error("Failed to load messages:", error);
  }
};

const selectConversation = async (id: number) => {
  if (currentConversationId.value === id) return;
  currentConversationId.value = id;
  await loadMessages(id);
};

const createNewConversation = async (promptInfo = false) => {
  try {
    const defaultTitle = t("chat.newConversation");
    const res = await chatAPI.createConversation(defaultTitle);
    await loadConversations();
    await selectConversation(res.data.id);
    if (promptInfo) {
      await nextTick();
      openInfoDialog();
    }
    ElMessage.success(t("messages.conversationCreated"));
  } catch (error) {
    console.error("Failed to create conversation:", error);
  }
};

const deleteConv = async (id: number) => {
  try {
    await ElMessageBox.confirm(t("messages.deleteConversationConfirm"), t("messages.confirmTitle"), {
      confirmButtonText: t("common.actions.confirm"),
      cancelButtonText: t("common.actions.cancel"),
      type: "warning",
    });

    await chatAPI.deleteConversation(id);
    await loadConversations();

    if (currentConversationId.value === id) {
      currentConversationId.value = null;
      messages.value = [];
    }

    if (conversationProfiles.value[id]) {
      const { [id]: _removed, ...rest } = conversationProfiles.value;
      conversationProfiles.value = rest;
    }

    ElMessage.success(t("messages.deleteSuccess"));
  } catch (error) {
    if (error !== "cancel") {
      console.error("Failed to delete conversation:", error);
    }
  }
};

const refreshConversation = async () => {
  if (!currentConversationId.value) return;
  await loadMessages(currentConversationId.value);
};

const sendMessage = async () => {
  if (!inputMessage.value.trim() || !currentConversationId.value) return;
  if (!currentConversation.value?.is_active) {
    ElMessage.warning(t("chat.conversationDisabled"));
    return;
  }

  const content = inputMessage.value;
  inputMessage.value = "";

  const tempMessage: MessageItem = {
    id: Date.now(),
    conversation_id: currentConversationId.value,
    role: "user",
    content,
    created_at: new Date().toISOString(),
  };
  messages.value.push(tempMessage);

  if (currentConversation.value && currentConversation.value.title === t("chat.newConversation")) {
    const preview = content.trim();
    if (preview) {
      currentConversation.value.title =
        preview.length > 20 ? `${preview.slice(0, 20)}…` : preview;
    }
  }

  await scrollToBottom();

  isStreaming.value = true;
  streamingContent.value = "";

  const existingUserMessages = messages.value.filter((msg) => msg.role === "user").length;
  const attachInfoNow = shouldAttachUserInfo.value || (existingUserMessages === 1 && hasPatientInfo.value);
  const userInfoPayload = attachInfoNow
    ? formatUserInfoForPrompt(currentProfile.value)
    : undefined;

  let sendSuccess = false;

  try {
    const response = await chatAPI.sendMessage(
      currentConversationId.value,
      content,
      userInfoPayload
    );

    if (!response.ok) {
      throw new Error(t("messages.sendFailed"));
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    if (reader) {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        streamingContent.value += chunk;
        await scrollToBottom();
      }

      messages.value.push({
        id: Date.now() + 1,
        conversation_id: currentConversationId.value,
        role: "assistant",
        content: streamingContent.value,
        created_at: new Date().toISOString(),
      });
      sendSuccess = true;
    }
  } catch (error) {
    console.error("Failed to send message:", error);
    ElMessage.error(t("messages.sendFailed"));
    inputMessage.value = content;
    messages.value = messages.value.filter((msg) => msg.id !== tempMessage.id);
  } finally {
    isStreaming.value = false;
    streamingContent.value = "";
    if (attachInfoNow && sendSuccess) {
      shouldAttachUserInfo.value = false;
    }
    await scrollToBottom();
  }
};

const handleLogout = () => {
  userStore.logout();
  router.push("/login");
};

// 定期检查对话状态（检测模型切换）
const checkConversationStatus = async () => {
  if (!currentConversationId.value) return

  try {
    const res = await chatAPI.getConversations()
    const currentConv = res.data.find((c) => c.id === currentConversationId.value)

    if (currentConv && !currentConv.is_active && currentConversation.value?.is_active) {
      // 对话被禁用了
      ElMessage.warning({
        message: t("chat.modelUpdatedNotice"),
        duration: 10000,
        showClose: true,
      })
      await loadConversations()
    }
  } catch (error) {
    console.error("Failed to check conversation status:", error)
  }
}

let statusCheckInterval: number | null = null

onMounted(async () => {
  restoreProfiles();
  if (!userStore.user) {
    try {
      const res = await api.get("/api/auth/users/me");
      userStore.setUser(res.data);
    } catch (error) {
      router.push("/login");
      return;
    }
  }

  try {
    const res = await api.get("/api/public/settings");
    websiteName.value = res.data.website_name;
  } catch (error) {
    console.error("Failed to fetch site settings:", error);
  }

  await loadConversations();

  // 每30秒检查一次对话状态
  statusCheckInterval = window.setInterval(checkConversationStatus, 30000)
});

// 组件卸载时清除定时器
import { onUnmounted } from 'vue'
onUnmounted(() => {
  if (statusCheckInterval !== null) {
    clearInterval(statusCheckInterval)
  }
})
</script>

<style scoped>
.chat-layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  height: 100vh;
  background: linear-gradient(120deg, rgba(240, 160, 75, 0.08), #ffffff 45%);
  overflow: hidden;
}

.sidebar {
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.92);
  border-right: 1px solid var(--color-borderPrimary);
  backdrop-filter: blur(12px);
}

.sidebar-header {
  padding: var(--spacing-xl);
  border-bottom: 1px solid var(--color-borderPrimary);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.brand h2 {
  margin: 0;
  font-size: var(--font-size-xl);
  color: var(--color-primary);
  font-weight: 700;
}

.brand-subtitle {
  margin: 4px 0 0;
  color: var(--color-textTertiary);
  font-size: var(--font-size-sm);
}

.conversation-scroll {
  flex: 1;
}

.conversation-item {
  padding: var(--spacing-md) var(--spacing-lg);
  border-bottom: 1px solid var(--color-borderLight);
  cursor: pointer;
  transition: all var(--transition-base);
}

.conversation-item:hover {
  background: rgba(240, 160, 75, 0.08);
}

.conversation-item.active {
  background: var(--color-primary);
  color: var(--color-white);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.4);
}

.conversation-item.active .conversation-time,
.conversation-item.active .conversation-actions .el-button,
.conversation-item.active .title-text {
  color: var(--color-white);
}

.conversation-item.inactive {
  opacity: 0.65;
}

.conversation-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--spacing-sm);
}

.conversation-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  max-width: 200px;
}

.title-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 600;
}

.conversation-time {
  font-size: var(--font-size-xs);
  color: var(--color-textTertiary);
}

.conversation-actions {
  display: flex;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-sm);
}

.sidebar-footer {
  padding: var(--spacing-lg);
  border-top: 1px solid var(--color-borderPrimary);
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  cursor: pointer;
  color: var(--color-textPrimary);
}

.user-name {
  font-weight: 500;
}

.main-content {
  position: relative;
  background: rgba(255, 255, 255, 0.96);
  display: flex;
  flex-direction: column;
}

.welcome {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.welcome-card {
  background: linear-gradient(135deg, rgba(240, 160, 75, 0.12), rgba(240, 160, 75, 0.22));
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-4xl);
  text-align: center;
  max-width: 520px;
  box-shadow: 0 18px 40px rgba(240, 160, 75, 0.18);
}

.welcome-card h1 {
  margin-bottom: var(--spacing-base);
  color: var(--color-primary);
}

.welcome-card p {
  color: var(--color-textSecondary);
  margin-bottom: var(--spacing-2xl);
}

.welcome-actions {
  display: flex;
  justify-content: center;
  gap: var(--spacing-lg);
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  padding: var(--spacing-xl) var(--spacing-2xl) var(--spacing-lg);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--color-borderPrimary);
  background: rgba(255, 255, 255, 0.95);
}

.chat-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.chat-title h1 {
  margin: 0;
  font-size: var(--font-size-2xl);
  color: var(--color-textPrimary);
}

.chat-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.patient-info-card {
  padding: var(--spacing-xl) var(--spacing-2xl);
  border-bottom: 1px solid var(--color-borderLight);
  background: rgba(255, 255, 255, 0.9);
}

.patient-info-card .card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--spacing-lg);
}

.card-header h3 {
  margin: 0;
  font-size: var(--font-size-lg);
  color: var(--color-textPrimary);
}

.card-subtitle {
  margin: var(--spacing-xs) 0 0;
  color: var(--color-textSecondary);
  font-size: var(--font-size-sm);
}

.info-body {
  margin-top: var(--spacing-lg);
}

.info-empty {
  margin-top: var(--spacing-lg);
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-xl) var(--spacing-2xl);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.95), rgba(245, 229, 204, 0.25));
}

.message {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
  align-items: flex-start;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 44px;
  height: 44px;
  border-radius: var(--border-radius-full);
  background: var(--color-primary);
  color: var(--color-white);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(240, 160, 75, 0.35);
}

.message.user .message-avatar {
  background: #409eff;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.message-content {
  max-width: 70%;
  background: rgba(255, 255, 255, 0.95);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-md) var(--spacing-lg);
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
  position: relative;
  overflow: hidden;
}

.message.user .message-content {
  background: rgba(64, 158, 255, 0.12);
}

.message-time {
  display: block;
  margin-top: var(--spacing-sm);
  font-size: var(--font-size-xs);
  color: var(--color-textTertiary);
}

.message-content.streaming {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.loading-icon {
  animation: rotate 1s linear infinite;
  color: var(--color-primary);
}

.input-area {
  padding: var(--spacing-xl) var(--spacing-2xl);
  border-top: 1px solid var(--color-borderPrimary);
  background: rgba(255, 255, 255, 0.95);
  position: sticky;
  bottom: 0;
  transition: all 0.3s ease;
}

.input-area.disabled-conversation {
  background: rgba(255, 243, 224, 0.95);
  border-top: 2px solid #ffa726;
}

.input-area.disabled-conversation :deep(.el-textarea__inner) {
  background: #f5f5f5;
  cursor: not-allowed;
}

.mt-sm {
  margin-top: var(--spacing-sm);
}

.mb-base {
  margin-bottom: var(--spacing-md);
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: var(--spacing-md);
}

.tip {
  font-size: var(--font-size-xs);
  color: var(--color-textTertiary);
}

.action-buttons {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.dialog-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 1200px) {
  .chat-layout {
    grid-template-columns: 260px 1fr;
  }

  .message-content {
    max-width: 80%;
  }
}

@media (max-width: 960px) {
  .chat-layout {
    grid-template-columns: 1fr;
  }

  .sidebar {
    display: none;
  }

  .main-content {
    height: 100vh;
  }
}
</style>
