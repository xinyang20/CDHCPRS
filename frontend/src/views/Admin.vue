<template>
  <div class="admin-container">
    <BackendStatus />

    <div class="admin-layout">
      <div class="admin-header-section">
        <h2>{{ t("admin.title") }}</h2>
        <p class="header-subtitle">{{ t("admin.subtitle") }}</p>
      </div>

      <el-tabs v-model="activeMenu" class="admin-tabs" @tab-click="handleTabClick">
        <el-tab-pane name="users">
          <template #label>
            <span class="tab-label">
              <el-icon><User /></el-icon>
              {{ t("admin.menu.users") }}
            </span>
          </template>
        </el-tab-pane>
        <el-tab-pane name="conversations">
          <template #label>
            <span class="tab-label">
              <el-icon><ChatDotRound /></el-icon>
              {{ t("admin.menu.conversations") }}
            </span>
          </template>
        </el-tab-pane>
        <el-tab-pane name="settings">
          <template #label>
            <span class="tab-label">
              <el-icon><Setting /></el-icon>
              {{ t("admin.menu.settings") }}
            </span>
          </template>
        </el-tab-pane>
      </el-tabs>

      <div class="admin-main">
          <section v-if="activeMenu === 'users'" class="panel">
            <header class="panel-header">
              <div>
                <h3>{{ t("admin.users.title") }}</h3>
                <p>{{ t("admin.users.description") }}</p>
              </div>
              <el-button :loading="loadingUsers" @click="loadUsers">
                <el-icon><Refresh /></el-icon>
                {{ t("common.actions.refresh") }}
              </el-button>
            </header>

            <el-table
              :data="users"
              border
              stripe
              class="shadow-table"
              v-loading="loadingUsers"
            >
              <el-table-column
                prop="id"
                :label="t('admin.users.id')"
                width="80"
                align="center"
              />
              <el-table-column
                prop="username"
                :label="t('admin.users.username')"
                min-width="160"
              />
              <el-table-column
                :label="t('admin.users.role')"
                width="120"
                align="center"
              >
                <template #default="{ row }">
                  <el-tag :type="row.role === 'admin' ? 'danger' : 'primary'">
                    {{
                      row.role === "admin"
                        ? t("profile.roleAdmin")
                        : t("profile.roleUser")
                    }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column
                :label="t('admin.users.status')"
                width="120"
                align="center"
              >
                <template #default="{ row }">
                  <el-tag :type="row.is_banned ? 'danger' : 'success'">
                    {{
                      row.is_banned
                        ? t("common.status.banned")
                        : t("common.status.active")
                    }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column
                prop="created_at"
                :label="t('admin.users.createdAt')"
                min-width="200"
              >
                <template #default="{ row }">
                  {{ formatDate(row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column
                :label="t('common.actions.edit')"
                width="240"
                align="center"
              >
                <template #default="{ row }">
                  <el-button
                    v-if="!row.is_banned"
                    type="warning"
                    size="small"
                    @click="banUser(row.id)"
                  >
                    {{ t("admin.users.ban") }}
                  </el-button>
                  <el-button
                    v-else
                    type="success"
                    size="small"
                    @click="unbanUser(row.id)"
                  >
                    {{ t("admin.users.unban") }}
                  </el-button>
                  <el-button
                    type="danger"
                    size="small"
                    @click="deleteUser(row.id)"
                  >
                    {{ t("admin.users.delete") }}
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </section>

          <section v-else-if="activeMenu === 'conversations'" class="panel">
            <header class="panel-header">
              <div>
                <h3>{{ t("admin.conversations.title") }}</h3>
                <p>{{ t("admin.conversations.description") }}</p>
              </div>
              <el-button
                :loading="loadingConversations"
                @click="loadConversations"
              >
                <el-icon><Refresh /></el-icon>
                {{ t("common.actions.refresh") }}
              </el-button>
            </header>

            <el-table
              :data="conversations"
              border
              stripe
              class="shadow-table"
              v-loading="loadingConversations"
            >
              <el-table-column
                prop="id"
                :label="t('admin.users.id')"
                width="80"
                align="center"
              />
              <el-table-column
                prop="title"
                :label="t('admin.conversations.title')"
                min-width="240"
              />
              <el-table-column
                prop="user_id"
                :label="t('admin.conversations.userId')"
                width="120"
                align="center"
              />
              <el-table-column
                :label="t('admin.conversations.status')"
                width="140"
                align="center"
              >
                <template #default="{ row }">
                  <el-tag :type="row.is_active ? 'success' : 'info'">
                    {{
                      row.is_active
                        ? t("common.status.active")
                        : t("common.status.disabled")
                    }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column
                prop="created_at"
                :label="t('admin.conversations.createdAt')"
                min-width="200"
              >
                <template #default="{ row }">
                  {{ formatDate(row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column
                :label="t('common.actions.view')"
                width="220"
                align="center"
              >
                <template #default="{ row }">
                  <el-button size="small" @click="viewConversation(row)">
                    {{ t("admin.conversations.view") }}
                  </el-button>
                  <el-button
                    type="danger"
                    size="small"
                    @click="deleteConversation(row.id)"
                  >
                    {{ t("admin.conversations.delete") }}
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </section>

          <section v-else class="panel">
            <header class="panel-header">
              <div>
                <h3>{{ t("admin.settings.title") }}</h3>
                <p>{{ t("admin.settings.description") }}</p>
              </div>
            </header>

            <el-card class="settings-card" shadow="hover">
              <el-form
                ref="settingsFormRef"
                :model="settingsForm"
                :rules="settingsRules"
                label-width="140px"
                class="settings-form"
              >
                <el-divider content-position="left">{{
                  t("admin.settings.basic")
                }}</el-divider>

                <el-form-item
                  prop="website_name"
                  :label="t('admin.settings.websiteName')"
                >
                  <el-input
                    v-model="settingsForm.website_name"
                    :placeholder="t('admin.settings.websiteNamePlaceholder')"
                  />
                </el-form-item>

                <el-form-item
                  prop="website_logo"
                  :label="t('admin.settings.websiteLogo')"
                >
                  <div class="logo-upload-container">
                    <div class="logo-preview" v-if="settingsForm.website_logo">
                      <img :src="settingsForm.website_logo" alt="Logo" />
                    </div>
                    <el-upload
                      :auto-upload="false"
                      :show-file-list="false"
                      :on-change="handleLogoChange"
                      accept="image/png,image/jpeg,image/jpg,image/gif,image/svg+xml,image/webp"
                    >
                      <el-button type="primary" :loading="uploadingLogo">
                        <el-icon><Upload /></el-icon>
                        {{
                          uploadingLogo
                            ? t("admin.settings.uploading")
                            : t("admin.settings.uploadLogo")
                        }}
                      </el-button>
                    </el-upload>
                    <el-text size="small" type="info">{{
                      t("admin.settings.logoTips")
                    }}</el-text>
                  </div>
                </el-form-item>

                <el-form-item
                  prop="system_prompt"
                  :label="t('admin.settings.systemPrompt')"
                >
                  <el-input
                    v-model="settingsForm.system_prompt"
                    type="textarea"
                    :rows="4"
                    :placeholder="t('admin.settings.systemPromptPlaceholder')"
                  />
                </el-form-item>

                <el-form-item
                  prop="large_font_scale"
                  :label="t('admin.settings.largeFontScale')"
                >
                  <el-input-number
                    v-model="settingsForm.large_font_scale"
                    :min="1.2"
                    :max="3.0"
                    :step="0.1"
                    :precision="1"
                    :placeholder="t('admin.settings.largeFontScalePlaceholder')"
                  />
                  <el-text size="small" type="info" style="margin-left: 12px">{{
                    t("admin.settings.largeFontScaleTips")
                  }}</el-text>
                </el-form-item>

                <el-divider content-position="left">{{
                  t("admin.settings.llm")
                }}</el-divider>

                <el-alert
                  :title="t('admin.settings.warning')"
                  type="warning"
                  effect="light"
                  show-icon
                  class="mb-lg"
                />

                <el-row :gutter="24" class="llm-grid">
                  <el-col :xs="24" :md="12">
                    <el-form-item
                      prop="llm_provider"
                      :label="t('admin.settings.provider')"
                    >
                      <el-select
                        v-model="settingsForm.llm_provider"
                        @change="handleProviderChange"
                        class="full-width"
                        placeholder="{{ t('admin.settings.providerPlaceholder') }}"
                      >
                        <el-option label="DeepSeek" value="deepseek" />
                        <el-option label="Qwen" value="qwen" />
                        <el-option label="OpenAI" value="openai" />
                        <el-option label="OpenAIful" value="openaiful" />
                        <el-option label="Dify" value="dify" />
                      </el-select>
                    </el-form-item>
                  </el-col>

                  <el-col :xs="24" :md="12">
                    <el-form-item
                      prop="llm_base_url"
                      :label="t('admin.settings.baseUrl')"
                      :required="isBaseUrlRequired"
                    >
                      <el-input
                        v-model="settingsForm.llm_base_url"
                        :placeholder="baseUrlPlaceholder"
                        clearable
                      />
                    </el-form-item>
                  </el-col>

                  <el-col :xs="24" :md="12">
                    <el-form-item
                      prop="llm_api_key"
                      :label="t('admin.settings.apiKey')"
                    >
                      <el-input
                        v-model="settingsForm.llm_api_key"
                        type="password"
                        show-password
                        :placeholder="t('admin.settings.apiKeyPlaceholder')"
                      />
                    </el-form-item>
                  </el-col>

                  <el-col :xs="24" :md="12">
                    <el-form-item label=" ">
                      <div class="inline-actions">
                        <el-button
                          plain
                          :loading="fetchingModels"
                          :disabled="!canFetchModels"
                          @click="handleFetchModels"
                        >
                          <el-icon><Search /></el-icon>
                          {{ t("common.actions.fetchModels") }}
                        </el-button>
                        <el-button
                          plain
                          :loading="testingConnection"
                          @click="handleTestConnection"
                        >
                          <el-icon><Link /></el-icon>
                          {{ t("common.actions.test") }}
                        </el-button>
                      </div>
                    </el-form-item>
                  </el-col>

                  <el-col :xs="24" :md="12">
                    <el-form-item
                      prop="llm_model_id"
                      :label="t('admin.settings.modelId')"
                    >
                      <el-select
                        v-model="settingsForm.llm_model_id"
                        filterable
                        allow-create
                        default-first-option
                        class="full-width"
                        @change="handleModelChange"
                        :placeholder="t('admin.settings.modelPlaceholder')"
                      >
                        <el-option
                          v-for="option in modelOptions"
                          :key="option.id"
                          :label="option.name ?? option.id"
                          :value="option.id"
                        />
                      </el-select>
                    </el-form-item>
                  </el-col>

                  <el-col :xs="24" :md="12">
                    <el-form-item
                      prop="llm_model_name"
                      :label="t('admin.settings.modelName')"
                    >
                      <el-input
                        v-model="settingsForm.llm_model_name"
                        :placeholder="t('admin.settings.modelNamePlaceholder')"
                      />
                    </el-form-item>
                  </el-col>
                </el-row>

                <div class="form-actions">
                  <el-button
                    type="primary"
                    :loading="savingSettings"
                    @click="handleSaveSettings"
                  >
                    <el-icon><Check /></el-icon>
                    {{ t("common.actions.save") }}
                  </el-button>
                </div>
              </el-form>
            </el-card>
          </section>
        </div>
      </div>

      <el-dialog
        v-model="conversationDialogVisible"
      width="720px"
      :title="
        t('admin.conversations.dialogTitle', {
          title: selectedConversationTitle,
        })
      "
    >
      <el-empty
        v-if="conversationMessages.length === 0"
        :description="t('admin.conversations.empty')"
      />
      <el-timeline v-else class="conversation-timeline">
        <el-timeline-item
          v-for="message in conversationMessages"
          :key="message.id"
          :timestamp="formatDate(message.created_at)"
          :color="message.role === 'assistant' ? '#f0a04b' : '#409EFF'"
        >
          <div class="message-bubble" :class="message.role">
            <h4>
              <el-icon v-if="message.role === 'assistant'"
                ><Promotion
              /></el-icon>
              <el-icon v-else><User /></el-icon>
              <span>{{
                message.role === "assistant"
                  ? t("chat.assistantLabel")
                  : t("chat.userLabel")
              }}</span>
            </h4>
            <MarkdownRenderer
              v-if="message.role === 'assistant'"
              :content="message.content"
            />
            <p v-else class="plain-text">{{ message.content }}</p>
          </div>
        </el-timeline-item>
      </el-timeline>
      <template #footer>
        <el-button @click="conversationDialogVisible = false">{{
          t("common.actions.close")
        }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, onMounted, reactive, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import {
  ChatDotRound,
  Link,
  Check,
  Promotion,
  Refresh,
  Search,
  Setting,
  User,
  Upload,
} from "@element-plus/icons-vue";
import {
  ElMessage,
  ElMessageBox,
  type FormInstance,
  type FormItemRule,
  type FormRules,
  type UploadFile,
} from "element-plus";

import BackendStatus from "../components/BackendStatus.vue";
import MarkdownRenderer from "../components/MarkdownRenderer.vue";
import {
  adminAPI,
  type AdminSettingsResponse,
  type AdminSettingsUpdatePayload,
  type AdminUser,
  type ConversationMessage,
  type ConversationSummary,
  type LLMModelOption,
} from "../api/admin";
import { useUserStore } from "../stores/user";

const router = useRouter();
const { t, locale } = useI18n();
const userStore = useUserStore();

const activeMenu = ref<"users" | "conversations" | "settings">("users");
const loadingUsers = ref(false);
const loadingConversations = ref(false);
const savingSettings = ref(false);
const testingConnection = ref(false);
const fetchingModels = ref(false);
const uploadingLogo = ref(false);

const users = ref<AdminUser[]>([]);
const conversations = ref<ConversationSummary[]>([]);
const modelOptions = ref<LLMModelOption[]>([]);

const conversationDialogVisible = ref(false);
const conversationMessages = ref<ConversationMessage[]>([]);
const selectedConversationTitle = ref("");

const settingsForm = reactive<
  AdminSettingsUpdatePayload & {
    llm_provider: string;
    llm_model_id: string;
    llm_model_name: string;
  }
>({
  website_name: "",
  website_logo: "",
  system_prompt: "",
  large_font_scale: 1.5,
  llm_provider: "deepseek",
  llm_base_url: "",
  llm_api_key: "",
  llm_model_id: "",
  llm_model_name: "",
});

const settingsFormRef = ref<FormInstance>();
let previousProvider = settingsForm.llm_provider;

const providerDefaults: Record<string, string> = {
  deepseek: "https://api.deepseek.com/v1",
  openai: "https://api.openai.com/v1",
  qwen: "https://dashscope.aliyuncs.com/compatible-mode/v1",
};

const isBaseUrlRequired = computed(
  () => settingsForm.llm_provider === "openaiful" || settingsForm.llm_provider === "dify"
);

const baseUrlPlaceholder = computed(() => {
  if (settingsForm.llm_provider === "openaiful" || settingsForm.llm_provider === "dify") {
    return t("admin.settings.baseUrlRequiredPlaceholder");
  }
  const preset =
    providerDefaults[
      settingsForm.llm_provider as keyof typeof providerDefaults
    ];
  return preset ?? t("admin.settings.baseUrlPlaceholder");
});

const canFetchModels = computed(() => {
  if (!settingsForm.llm_provider || !settingsForm.llm_api_key?.trim()) {
    return false;
  }
  if (settingsForm.llm_provider === "openaiful" || settingsForm.llm_provider === "dify") {
    return Boolean(settingsForm.llm_base_url?.trim());
  }
  return true;
});

const settingsRules: FormRules = {
  website_name: [
    {
      required: true,
      message: t("admin.settings.websiteNameRequired"),
      trigger: "blur",
    },
  ],
  system_prompt: [
    {
      required: true,
      message: t("admin.settings.systemPromptRequired"),
      trigger: "blur",
    },
  ],
  llm_provider: [
    {
      required: true,
      message: t("admin.settings.providerRequired"),
      trigger: "change",
    },
  ],
  llm_api_key: [
    {
      required: true,
      message: t("admin.settings.apiKeyRequired"),
      trigger: "blur",
    },
  ],
  llm_model_id: [
    {
      validator: (_, value, callback) => {
        if (
          (value && value.trim().length > 0) ||
          (settingsForm.llm_model_name &&
            settingsForm.llm_model_name.trim().length > 0)
        ) {
          callback();
        } else {
          callback(new Error(t("admin.settings.modelRequired")));
        }
      },
      trigger: "blur",
    },
  ],
  llm_base_url: [],
};

const setRuleMessage = (rules: FormRules[string], message: string) => {
  if (!rules) return;
  const normalized: FormItemRule[] = Array.isArray(rules)
    ? [...rules]
    : [rules];
  normalized.forEach((rule) => {
    if (rule && typeof rule === "object" && "message" in rule) {
      (rule as FormItemRule).message = message;
    }
  });
};

watch(isBaseUrlRequired, (required) => {
  if (required) {
    settingsRules.llm_base_url = [
      {
        required: true,
        message: t("admin.settings.baseUrlRequired"),
        trigger: "blur",
      },
    ] as FormItemRule[];
  } else {
    settingsRules.llm_base_url = [] as FormItemRule[];
  }
});

watch(locale, () => {
  setRuleMessage(
    settingsRules.website_name,
    t("admin.settings.websiteNameRequired")
  );
  setRuleMessage(
    settingsRules.system_prompt,
    t("admin.settings.systemPromptRequired")
  );
  setRuleMessage(
    settingsRules.llm_provider,
    t("admin.settings.providerRequired")
  );
  setRuleMessage(settingsRules.llm_api_key, t("admin.settings.apiKeyRequired"));
  setRuleMessage(
    settingsRules.llm_base_url,
    t("admin.settings.baseUrlRequired")
  );
});

const formatDate = (value?: string) => {
  if (!value) return "";
  return new Date(value).toLocaleString(locale.value, { hour12: false });
};

const handleMenuSelect = (key: string) => {
  activeMenu.value = key as typeof activeMenu.value;
};

const handleTabClick = () => {
  // Tab切换由v-model自动处理
};

const loadUsers = async () => {
  loadingUsers.value = true;
  try {
    const { data } = await adminAPI.getUsers();
    users.value = data;
  } catch (error) {
    console.error("Failed to fetch users", error);
    ElMessage.error(t("messages.requestFailed"));
  } finally {
    loadingUsers.value = false;
  }
};

const loadConversations = async () => {
  loadingConversations.value = true;
  try {
    const { data } = await adminAPI.getAllConversations();
    conversations.value = data;
  } catch (error) {
    console.error("Failed to fetch conversations", error);
    ElMessage.error(t("messages.requestFailed"));
  } finally {
    loadingConversations.value = false;
  }
};

const loadSettings = async () => {
  try {
    const { data } = await adminAPI.getSettings();
    applySettingsResponse(data);
  } catch (error) {
    console.error("Failed to fetch settings", error);
    ElMessage.error(t("messages.requestFailed"));
  }
};

const applySettingsResponse = (settings: AdminSettingsResponse) => {
  Object.assign(settingsForm, settings);
  previousProvider = settingsForm.llm_provider ?? "deepseek";
  if (!settingsForm.llm_model_id && settingsForm.llm_model_name) {
    settingsForm.llm_model_id = settingsForm.llm_model_name;
  }
};

const banUser = async (userId: number) => {
  try {
    await adminAPI.updateUser(userId, { is_banned: true });
    ElMessage.success(t("admin.users.banSuccess"));
    await loadUsers();
  } catch (error) {
    console.error("Failed to ban user", error);
  }
};

const unbanUser = async (userId: number) => {
  try {
    await adminAPI.updateUser(userId, { is_banned: false });
    ElMessage.success(t("admin.users.unbanSuccess"));
    await loadUsers();
  } catch (error) {
    console.error("Failed to unban user", error);
  }
};

const deleteUser = async (userId: number) => {
  try {
    await ElMessageBox.confirm(
      t("admin.users.deleteConfirm"),
      t("messages.confirmTitle"),
      {
        confirmButtonText: t("common.actions.confirm"),
        cancelButtonText: t("common.actions.cancel"),
        type: "warning",
      }
    );
    await adminAPI.deleteUser(userId);
    ElMessage.success(t("messages.deleteSuccess"));
    await loadUsers();
  } catch (error) {
    if (error !== "cancel") {
      console.error("Failed to delete user", error);
    }
  }
};

const viewConversation = async (conversation: ConversationSummary) => {
  try {
    const { data } = await adminAPI.getConversationMessages(conversation.id);
    conversationMessages.value = data;
    selectedConversationTitle.value = conversation.title;
    conversationDialogVisible.value = true;
    await nextTick();
  } catch (error) {
    console.error("Failed to load conversation messages", error);
    ElMessage.error(t("messages.requestFailed"));
  }
};

const deleteConversation = async (conversationId: number) => {
  try {
    await ElMessageBox.confirm(
      t("admin.conversations.deleteConfirm"),
      t("messages.confirmTitle"),
      {
        confirmButtonText: t("common.actions.confirm"),
        cancelButtonText: t("common.actions.cancel"),
        type: "warning",
      }
    );
    await adminAPI.deleteConversation(conversationId);
    ElMessage.success(t("messages.deleteSuccess"));
    await loadConversations();
  } catch (error) {
    if (error !== "cancel") {
      console.error("Failed to delete conversation", error);
    }
  }
};

const handleProviderChange = async (provider: string) => {
  modelOptions.value = [];

  if (provider !== previousProvider) {
    const preset = providerDefaults[provider as keyof typeof providerDefaults];
    if (
      preset &&
      (!settingsForm.llm_base_url ||
        settingsForm.llm_base_url ===
          providerDefaults[previousProvider as keyof typeof providerDefaults])
    ) {
      settingsForm.llm_base_url = preset;
    }

    if (provider === "openaiful") {
      settingsForm.llm_base_url = settingsForm.llm_base_url || "";
    }
  }

  previousProvider = provider;
};

const handleModelChange = (modelId: string) => {
  const target = modelOptions.value.find((item) => item.id === modelId);
  settingsForm.llm_model_name = target?.name ?? modelId;
};

const handleLogoChange = async (uploadFile: UploadFile) => {
  if (!uploadFile.raw) return;

  const file = uploadFile.raw;
  const allowedTypes = [
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/gif",
    "image/svg+xml",
    "image/webp",
  ];

  if (!allowedTypes.includes(file.type)) {
    ElMessage.error(t("admin.settings.logoTypeError"));
    return;
  }

  if (file.size > 2 * 1024 * 1024) {
    ElMessage.error(t("admin.settings.logoSizeError"));
    return;
  }

  uploadingLogo.value = true;
  try {
    const { data } = await adminAPI.uploadLogo(file);
    settingsForm.website_logo = data.logo_url;
    ElMessage.success(t("admin.settings.logoUploadSuccess"));
  } catch (error) {
    console.error("Failed to upload logo", error);
    ElMessage.error(t("messages.requestFailed"));
  } finally {
    uploadingLogo.value = false;
  }
};

const handleFetchModels = async () => {
  if (!canFetchModels.value) return;
  fetchingModels.value = true;
  try {
    const requestPayload = {
      llm_provider: settingsForm.llm_provider,
      llm_api_key: settingsForm.llm_api_key ?? "",
      llm_base_url: settingsForm.llm_base_url ?? undefined,
    };
    const { data } = await adminAPI.fetchModels(requestPayload);
    modelOptions.value = data.models;
    const [firstModel] = data.models;
    if (firstModel) {
      settingsForm.llm_model_id = firstModel.id;
      settingsForm.llm_model_name = firstModel.name ?? firstModel.id;
    }
    ElMessage.success(t("messages.fetchModelsSuccess"));
  } catch (error) {
    console.error("Failed to fetch models", error);
    ElMessage.error(t("messages.fetchModelsFail"));
  } finally {
    fetchingModels.value = false;
  }
};

const handleTestConnection = async () => {
  if (!settingsForm.llm_api_key?.trim()) {
    ElMessage.warning(t("admin.settings.apiKeyRequired"));
    return;
  }
  if (isBaseUrlRequired.value && !settingsForm.llm_base_url?.trim()) {
    ElMessage.warning(t("admin.settings.baseUrlRequired"));
    return;
  }

  testingConnection.value = true;
  try {
    const trimmedModelId = (settingsForm.llm_model_id ?? "").trim();
    const trimmedModelName = (settingsForm.llm_model_name ?? "").trim();
    const trimmedBaseUrl = (settingsForm.llm_base_url ?? "").trim();

    const payload = {
      llm_provider: settingsForm.llm_provider,
      llm_api_key: settingsForm.llm_api_key ?? "",
      llm_model_id: trimmedModelId || undefined,
      llm_model_name: trimmedModelName || undefined,
      llm_base_url: trimmedBaseUrl || undefined,
    };
    const { data } = await adminAPI.testConnection(payload);
    if (data.success) {
      ElMessage.success(data.message);
    } else {
      ElMessage.error(data.message);
    }
  } catch (error) {
    console.error("Failed to test connection", error);
  } finally {
    testingConnection.value = false;
  }
};

const handleSaveSettings = async () => {
  if (!settingsFormRef.value) {
    await submitSettings();
    return;
  }
  await settingsFormRef.value.validate(async (valid) => {
    if (!valid) return;
    await submitSettings();
  });
};

const submitSettings = async () => {
  if (!settingsForm.llm_model_id && !settingsForm.llm_model_name) {
    ElMessage.warning(t("admin.settings.modelRequired"));
    return;
  }

  savingSettings.value = true;
  try {
    const payload: AdminSettingsUpdatePayload = {
      website_name: settingsForm.website_name,
      website_logo: settingsForm.website_logo,
      system_prompt: settingsForm.system_prompt,
      large_font_scale: settingsForm.large_font_scale,
      llm_provider: settingsForm.llm_provider,
      llm_base_url: settingsForm.llm_base_url,
      llm_api_key: settingsForm.llm_api_key,
      llm_model_id: settingsForm.llm_model_id,
      llm_model_name: settingsForm.llm_model_name,
    };
    const { data } = await adminAPI.updateSettings(payload);
    applySettingsResponse(data);
    ElMessage.success(t("messages.settingsSaved"));
  } catch (error) {
    console.error("Failed to save settings", error);
  } finally {
    savingSettings.value = false;
  }
};

onMounted(async () => {
  if (!userStore.isAdmin()) {
    router.replace("/chat");
    return;
  }

  await Promise.all([loadUsers(), loadConversations(), loadSettings()]);
});
</script>

<style scoped>
.admin-container {
  height: 100%;
  background: linear-gradient(120deg, rgba(240, 160, 75, 0.08), #ffffff 45%);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.admin-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.admin-header-section {
  background: var(--color-bgPrimary);
  padding: var(--spacing-xl) var(--spacing-2xl);
  border-bottom: 1px solid var(--color-borderLight);
  flex-shrink: 0;
}

.admin-header-section h2 {
  margin: 0;
  color: var(--color-primaryDark);
  font-size: var(--font-size-3xl);
  font-weight: 700;
}

.header-subtitle {
  margin: var(--spacing-xs) 0 0;
  color: var(--color-textSecondary);
}

.admin-tabs {
  flex-shrink: 0;
  padding: 0 var(--spacing-2xl);
  background: var(--color-bgPrimary);
}

.tab-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.admin-main {
  padding: var(--spacing-2xl);
  background: transparent;
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
}

.panel {
  background: rgba(255, 255, 255, 0.96);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-2xl);
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
}

.panel-header h3 {
  margin: 0;
  font-size: var(--font-size-2xl);
  color: var(--color-textPrimary);
}

.panel-header p {
  margin: var(--spacing-xs) 0 0;
  color: var(--color-textSecondary);
}

.shadow-table {
  border-radius: var(--border-radius-base);
  overflow: hidden;
}

.settings-card {
  border-radius: var(--border-radius-lg);
}

.settings-form {
  margin-top: var(--spacing-lg);
}

.logo-upload-container {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.logo-preview {
  width: 120px;
  height: 60px;
  border: 1px dashed var(--color-borderSecondary);
  border-radius: var(--border-radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: var(--color-bgSecondary);
}

.logo-preview img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.llm-grid {
  margin-bottom: var(--spacing-xl);
}

.full-width {
  width: 100%;
}

.inline-actions {
  display: flex;
  gap: var(--spacing-sm);
  justify-content: flex-start;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: var(--spacing-xl);
}

.conversation-timeline {
  max-height: 480px;
  overflow-y: auto;
}

.message-bubble {
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
}

.message-bubble.assistant {
  border-left: 4px solid var(--color-primary);
}

.message-bubble.user {
  border-left: 4px solid #409eff;
}

.message-bubble h4 {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-sm);
  font-size: var(--font-size-base);
  color: var(--color-textSecondary);
}

.message-bubble .plain-text {
  margin: 0;
  white-space: pre-wrap;
  color: var(--color-textPrimary);
  line-height: 1.6;
}

:deep(.el-form-item__label) {
  font-weight: 600;
  color: var(--color-textSecondary);
}

:deep(.el-dialog__body) {
  max-height: 60vh;
  overflow-y: auto;
}

@media (max-width: 960px) {
  .admin-header-section {
    padding: var(--spacing-lg);
  }

  .admin-tabs {
    padding: 0 var(--spacing-lg);
  }

  .admin-main {
    padding: var(--spacing-lg);
  }

  .panel {
    padding: var(--spacing-lg);
  }
}
</style>
