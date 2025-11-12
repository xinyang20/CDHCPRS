<template>
  <div class="chat-layout">
    <BackendStatus />

    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="brand">
          <h2>{{ websiteName }}</h2>
          <p class="brand-subtitle">{{ t("chat.sidebarTagline") }}</p>
        </div>
        <el-button
          type="primary"
          @click="createNewConversation(true)"
          :icon="Plus"
        >
          {{ t("chat.newConversation") }}
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
                >{{ t("common.status.disabled") }}</el-tag
              >
            </div>
            <span class="conversation-time">{{
              formatDate(conv.created_at)
            }}</span>
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

    </aside>

    <main class="main-content">
      <div v-if="!currentConversationId" class="welcome">
        <div class="welcome-card">
          <h1>{{ t("chat.welcomeTitle") }}</h1>
          <p>{{ t("chat.welcomeSubtitle") }}</p>
          <div class="welcome-actions">
            <el-button
              type="primary"
              size="large"
              @click="createNewConversation(true)"
            >
              <el-icon><Plus /></el-icon>
              {{ t("chat.newConversation") }}
            </el-button>
            <el-button size="large" @click="loadConversations">{{
              t("chat.refresh")
            }}</el-button>
          </div>
        </div>
      </div>

      <div v-else class="chat-area">
        <header class="chat-header">
          <div class="chat-title">
            <h1>{{ currentConversation?.title }}</h1>
            <el-tag
              v-if="!currentConversation?.is_active"
              type="warning"
              effect="plain"
            >
              {{ t("common.status.disabled") }}
            </el-tag>
          </div>
        </header>

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

        <footer
          class="input-area"
          :class="{
            'disabled-conversation':
              currentConversation && !currentConversation.is_active,
          }"
        >
          <el-alert
            v-if="currentConversation && !currentConversation.is_active"
            :title="t('chat.conversationDisabled')"
            type="warning"
            :closable="false"
            class="mb-base"
          >
            <template #default>
              <p>{{ t("chat.conversationDisabledDetail") }}</p>
              <el-button
                type="primary"
                size="small"
                :icon="Plus"
                @click="createNewConversation(true)"
                class="mt-sm"
              >
                {{ t("chat.createNewConversation") }}
              </el-button>
            </template>
          </el-alert>

          <el-input
            v-model="inputMessage"
            type="textarea"
            :rows="4"
            :placeholder="t('chat.questionPlaceholder')"
            :disabled="!currentConversation?.is_active || isStreaming"
            @keydown.enter.prevent="sendMessage"
          />
          <div class="input-actions">
            <span class="tip">Enter {{ t("chat.send") }}</span>
            <div class="action-buttons">
              <el-button
                text
                size="small"
                :icon="EditPen"
                @click="openInfoDialog"
                :disabled="!currentConversation?.is_active"
              >
                {{ t("chat.updateInfo") }}
              </el-button>
              <el-button
                type="primary"
                :loading="isStreaming"
                :disabled="
                  !inputMessage.trim() || !currentConversation?.is_active
                "
                @click="sendMessage"
              >
                {{ t("chat.send") }}
              </el-button>
            </div>
          </div>
        </footer>
      </div>
    </main>

    <el-dialog
      v-model="infoDialogVisible"
      :title="t('chat.infoDialogTitle')"
      width="520px"
      destroy-on-close
    >
      <el-form
        ref="infoFormRef"
        :model="infoForm"
        :rules="infoRules"
        label-width="90px"
      >
        <el-form-item :label="t('chat.age')" prop="age">
          <el-input
            v-model="infoForm.age"
            :placeholder="t('chat.age')"
            maxlength="3"
          />
        </el-form-item>
        <el-form-item :label="t('chat.gender')" prop="gender">
          <el-radio-group v-model="infoForm.gender">
            <el-radio label="male">{{ t("chat.genderMale") }}</el-radio>
            <el-radio label="female">{{ t("chat.genderFemale") }}</el-radio>
            <el-radio label="other">{{ t("chat.genderOther") }}</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item :label="t('chat.diseaseHistory')" prop="diseases">
          <el-checkbox-group v-model="infoForm.diseases" class="disease-checkboxes">
            <el-checkbox
              v-for="disease in DISEASES"
              :key="disease.id"
              :label="disease.id"
              border
              class="disease-checkbox-item"
            >
              {{ disease.name }}
            </el-checkbox>
          </el-checkbox-group>
        </el-form-item>

        <el-form-item
          v-if="infoForm.diseases && infoForm.diseases.length > 0"
          :label="t('chat.recentSymptoms')"
          prop="symptoms"
        >
          <div class="symptoms-container">
            <el-tag
              v-for="symptom in availableSymptoms"
              :key="symptom.id"
              :type="infoForm.symptoms?.includes(symptom.name) ? 'primary' : 'info'"
              :effect="infoForm.symptoms?.includes(symptom.name) ? 'dark' : 'plain'"
              @click="toggleSymptom(symptom.name)"
              class="symptom-tag"
            >
              {{ symptom.name }}
            </el-tag>
          </div>
        </el-form-item>

        <el-form-item
          v-if="infoForm.tcmSyndrome"
          :label="t('chat.tcmSyndrome')"
        >
          <el-alert
            :title="infoForm.tcmSyndrome"
            type="success"
            :closable="false"
            show-icon
          >
            <template #default>
              <p style="font-size: 12px; margin: 0;">
                {{ t('chat.tcmSyndromeHint') }}
              </p>
            </template>
          </el-alert>
        </el-form-item>

        <el-form-item :label="t('chat.chiefComplaint')" prop="mainComplaint">
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
          <el-button @click="skipInfoDialog">{{
            t("chat.infoSkip")
          }}</el-button>
          <el-button text type="danger" @click="clearInfoForm">{{
            t("chat.infoClear")
          }}</el-button>
          <el-button type="primary" @click="savePatientInfo">{{
            t("chat.infoSave")
          }}</el-button>
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
} from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";

import api from "../api";
import { chatAPI } from "../api/chat";
import { useUserStore } from "../stores/user";
import BackendStatus from "../components/BackendStatus.vue";
import MarkdownRenderer from "../components/MarkdownRenderer.vue";
import {
  DISEASES,
  getSymptomsByDiseases,
  inferTcmSyndrome,
} from "../constants/medicalData";

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
  diseases: string[];  // 疾病历史（疾病ID列表）
  symptoms: string[];  // 近期症状（症状名称列表）
  tcmSyndrome?: string;  // 前端推断的中医证型
}

const PROFILE_STORAGE_KEY = "cdhcprs_conversation_profiles";

const buildDefaultProfile = (): PatientProfile => ({
  age: "",
  gender: "",
  mainComplaint: "",
  diseases: [],
  symptoms: [],
  tcmSyndrome: undefined,
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

const currentConversation = computed(
  () =>
    conversations.value.find(
      (item) => item.id === currentConversationId.value
    ) || null
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
  return [profile.age, profile.gender, profile.mainComplaint].some(
    (v) => v && v.trim()
  ) || profile.diseases.length > 0 || profile.symptoms.length > 0;
});

// 根据选择的疾病动态过滤症状列表
const availableSymptoms = computed(() => {
  if (infoForm.diseases && infoForm.diseases.length > 0) {
    return getSymptomsByDiseases(infoForm.diseases);
  }
  return [];
});

// 实时推断中医证型
watch(
  () => [infoForm.diseases, infoForm.symptoms],
  () => {
    if (infoForm.diseases && infoForm.symptoms) {
      const syndrome = inferTcmSyndrome(infoForm.diseases, infoForm.symptoms);
      infoForm.tcmSyndrome = syndrome || undefined;
    }
  },
  { deep: true }
);

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

const toggleSymptom = (symptomName: string) => {
  if (!infoForm.symptoms) {
    infoForm.symptoms = [];
  }
  const index = infoForm.symptoms.indexOf(symptomName);
  if (index > -1) {
    infoForm.symptoms.splice(index, 1);
  } else {
    infoForm.symptoms.push(symptomName);
  }
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
      diseases: infoForm.diseases || [],
      symptoms: infoForm.symptoms || [],
      tcmSyndrome: infoForm.tcmSyndrome,
    };
    infoDialogVisible.value = false;
    shouldAttachUserInfo.value = true;
    ElMessage.success(t("chat.infoSaved"));
  });
};

const formatUserInfoForPrompt = (profile: PatientProfile) => {
  const parts: string[] = [];

  // 基本信息
  if (profile.age) {
    parts.push(`${t("chat.age")}: ${profile.age}岁`);
  }
  if (profile.gender) {
    parts.push(`${t("chat.gender")}: ${genderLabel(profile.gender)}`);
  }

  // 疾病历史
  if (profile.diseases && profile.diseases.length > 0) {
    const diseaseNames = profile.diseases
      .map((id) => DISEASES.find((d) => d.id === id)?.name)
      .filter(Boolean)
      .join('、');
    parts.push(`${t("chat.diseaseHistory")}: ${diseaseNames}`);
  }

  // 近期症状
  if (profile.symptoms && profile.symptoms.length > 0) {
    parts.push(`${t("chat.recentSymptoms")}: ${profile.symptoms.join('、')}`);
  }

  // 中医证型（前端推断）
  if (profile.tcmSyndrome) {
    parts.push(`${t("chat.tcmSyndrome")}（初步分析）: ${profile.tcmSyndrome}`);
  }

  // 主诉
  if (profile.mainComplaint) {
    parts.push(`${t("chat.chiefComplaint")}: ${profile.mainComplaint}`);
  }

  return parts.length > 0 ? `\n【患者信息】\n${parts.join("\n")}` : "";
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
    // 确保只加载属于当前对话的消息
    const loadedMessages = res.data.filter(
      (msg: MessageItem) => msg.conversation_id === conversationId
    );
    messages.value = loadedMessages;
    await scrollToBottom();
    if (messages.value.length === 0 && hasPatientInfo.value) {
      shouldAttachUserInfo.value = true;
    }
  } catch (error) {
    console.error("Failed to load messages:", error);
    // 加载失败时清空消息，避免显示错误数据
    messages.value = [];
  }
};

const selectConversation = async (id: number, forceReload = false) => {
  if (currentConversationId.value === id && !forceReload) return;
  currentConversationId.value = id;
  // 先清空消息，防止显示旧数据
  messages.value = [];
  await loadMessages(id);
};

const createNewConversation = async (promptInfo = false) => {
  try {
    const defaultTitle = t("chat.newConversation");
    const res = await chatAPI.createConversation(defaultTitle);
    await loadConversations();
    // 强制重新加载消息，确保不会显示旧数据
    await selectConversation(res.data.id, true);
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
    await ElMessageBox.confirm(
      t("messages.deleteConversationConfirm"),
      t("messages.confirmTitle"),
      {
        confirmButtonText: t("common.actions.confirm"),
        cancelButtonText: t("common.actions.cancel"),
        type: "warning",
      }
    );

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

  if (
    currentConversation.value &&
    currentConversation.value.title === t("chat.newConversation")
  ) {
    const preview = content.trim();
    if (preview) {
      currentConversation.value.title =
        preview.length > 20 ? `${preview.slice(0, 20)}…` : preview;
    }
  }

  await scrollToBottom();

  isStreaming.value = true;
  streamingContent.value = "";

  const existingUserMessages = messages.value.filter(
    (msg) => msg.role === "user"
  ).length;
  const attachInfoNow =
    shouldAttachUserInfo.value ||
    (existingUserMessages === 1 && hasPatientInfo.value);
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

// 定期检查对话状态（检测模型切换）
const checkConversationStatus = async () => {
  if (!currentConversationId.value) return;

  try {
    const res = await chatAPI.getConversations();
    const currentConv = res.data.find(
      (c) => c.id === currentConversationId.value
    );

    if (
      currentConv &&
      !currentConv.is_active &&
      currentConversation.value?.is_active
    ) {
      // 对话被禁用了
      ElMessage.warning({
        message: t("chat.modelUpdatedNotice"),
        duration: 10000,
        showClose: true,
      });
      await loadConversations();
    }
  } catch (error) {
    console.error("Failed to check conversation status:", error);
  }
};

let statusCheckInterval: number | null = null;

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
  statusCheckInterval = window.setInterval(checkConversationStatus, 30000);
});

// 组件卸载时清除定时器
import { onUnmounted } from "vue";
onUnmounted(() => {
  if (statusCheckInterval !== null) {
    clearInterval(statusCheckInterval);
  }
});
</script>

<style scoped>
.chat-layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  flex: 1;
  min-height: 0;
  background: linear-gradient(135deg, var(--color-bgSecondary) 0%, var(--color-bgPrimary) 50%);
  overflow: hidden;
}

.sidebar {
  display: flex;
  flex-direction: column;
  background: var(--color-bgSecondary);
  border-right: 2px solid var(--color-borderPrimary);
  box-shadow: 2px 0 8px rgba(139, 115, 85, 0.1);
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
  position: relative;
}

.conversation-item:hover {
  background: var(--color-bgTertiary);
  border-left: 3px solid var(--color-primaryLight);
  padding-left: calc(var(--spacing-lg) - 3px);
}

.conversation-item.active {
  background: var(--color-primary);
  color: var(--color-white);
  border-left: 3px solid var(--color-primaryDark);
  padding-left: calc(var(--spacing-lg) - 3px);
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

.main-content {
  position: relative;
  background: var(--color-bgPrimary);
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}

.welcome {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(circle at center, var(--color-bgPrimary), var(--color-bgSecondary));
}

.welcome-card {
  background: var(--color-bgSecondary);
  border: 2px solid var(--color-borderPrimary);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-4xl);
  text-align: center;
  max-width: 520px;
  box-shadow: 0 8px 24px rgba(139, 115, 85, 0.15);
  position: relative;
}

.welcome-card::before {
  content: '';
  position: absolute;
  top: -1px;
  left: -1px;
  right: -1px;
  bottom: -1px;
  background: linear-gradient(45deg, var(--color-primaryDark), var(--color-primaryLight));
  border-radius: var(--border-radius-lg);
  opacity: 0.1;
  z-index: -1;
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
  min-height: 0;
}

.chat-header {
  padding: var(--spacing-xl) var(--spacing-2xl) var(--spacing-lg);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid var(--color-borderPrimary);
  background: linear-gradient(to bottom, var(--color-bgPrimary), var(--color-bgSecondary));
  flex-shrink: 0;
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
  font-weight: 600;
}

.message-list {
  flex: 1 1 0;
  overflow-y: auto;
  overflow-x: hidden;
  padding: var(--spacing-xl) var(--spacing-2xl);
  background: var(--color-bgPrimary);
  min-height: 0;
  height: 0;
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
  border: 2px solid var(--color-primaryLight);
  box-shadow: 0 2px 8px rgba(139, 115, 85, 0.2);
}

.message.user .message-avatar {
  background: var(--color-primaryDark);
  border: 2px solid var(--color-primary);
  box-shadow: 0 2px 8px rgba(107, 88, 64, 0.3);
}

.message-content {
  max-width: 70%;
  background: var(--color-bgSecondary);
  border: 1px solid var(--color-borderLight);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-md) var(--spacing-lg);
  box-shadow: 0 2px 12px rgba(139, 115, 85, 0.08);
  position: relative;
  overflow: hidden;
}

.message.user .message-content {
  background: linear-gradient(135deg, var(--color-bgTertiary), var(--color-bgSecondary));
  border: 1px solid var(--color-borderPrimary);
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
  border-top: 2px solid var(--color-borderPrimary);
  background: var(--color-bgSecondary);
  flex-shrink: 0;
  transition: all 0.3s ease;
  position: relative;
}

.input-area::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(to right, var(--color-primaryDark), var(--color-primary), var(--color-primaryDark));
  opacity: 0.3;
}

.input-area.disabled-conversation {
  background: linear-gradient(135deg, var(--color-bgTertiary), var(--color-bgSecondary));
  border-top: 2px solid var(--color-warning);
}

.input-area.disabled-conversation :deep(.el-textarea__inner) {
  background: var(--color-bgPrimary);
  cursor: not-allowed;
  border-color: var(--color-borderSecondary);
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

/* 疾病历史选择器样式 */
.disease-checkboxes {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
  width: 100%;
}

.disease-checkbox-item {
  margin: 0 !important;
  min-width: 140px;
}

.disease-checkbox-item :deep(.el-checkbox__label) {
  font-size: var(--font-size-sm);
}

/* 症状标签容器 */
.symptoms-container {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
  max-height: 200px;
  overflow-y: auto;
  padding: var(--spacing-md);
  background: var(--color-bgPrimary);
  border-radius: var(--border-radius-md);
  border: 2px dashed var(--color-borderSecondary);
  position: relative;
}

.symptoms-container::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--color-bgTertiary), transparent);
  opacity: 0.3;
  border-radius: var(--border-radius-md);
  pointer-events: none;
}

.symptom-tag {
  cursor: pointer;
  user-select: none;
  transition: all var(--transition-fast);
  font-size: var(--font-size-sm);
  border: 1px solid var(--color-borderLight) !important;
}

.symptom-tag:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 6px rgba(139, 115, 85, 0.15);
  border-color: var(--color-primary) !important;
}

.symptom-tag:active {
  transform: translateY(0);
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

/* 大字版模式下扩大侧边栏宽度 */
html.large-font-mode .chat-layout {
  grid-template-columns: 400px 1fr;
}

@media (max-width: 1200px) and (min-width: 961px) {
  html.large-font-mode .chat-layout {
    grid-template-columns: 340px 1fr;
  }
}
</style>
