<template>
  <div class="chat-layout">
    <!-- 后端状态指示器 -->
    <BackendStatus />

    <!-- 侧边栏 -->
    <div class="sidebar">
      <div class="sidebar-header">
        <h2>{{ websiteName }}</h2>
        <el-button type="primary" @click="createNewConversation" :icon="Plus">
          新建对话
        </el-button>
      </div>

      <div class="conversation-list">
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
          <div class="conversation-title">
            <el-icon><ChatDotRound /></el-icon>
            <span>{{ conv.title }}</span>
          </div>
          <div class="conversation-actions">
            <el-button
              type="danger"
              size="small"
              :icon="Delete"
              circle
              @click.stop="deleteConv(conv.id)"
            />
          </div>
        </div>
      </div>

      <div class="sidebar-footer">
        <el-dropdown>
          <span class="user-info">
            <el-icon><User /></el-icon>
            {{ userStore.user?.username }}
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="$router.push('/profile')">
                个人信息
              </el-dropdown-item>
              <el-dropdown-item
                v-if="userStore.isAdmin()"
                @click="$router.push('/admin')"
              >
                管理后台
              </el-dropdown-item>
              <el-dropdown-item divided @click="handleLogout">
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="main-content">
      <div v-if="!currentConversationId" class="welcome">
        <h1>欢迎使用慢性病诊疗方案推荐系统</h1>
        <p>请选择或创建一个对话开始咨询</p>
      </div>

      <div v-else class="chat-area">
        <!-- 消息列表 -->
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
            </div>
          </div>

          <!-- 流式响应中的消息 -->
          <div v-if="isStreaming" class="message assistant">
            <div class="message-avatar">
              <el-icon><ChatDotRound /></el-icon>
            </div>
            <div class="message-content">
              <MarkdownRenderer :content="streamingContent" />
              <el-icon class="loading-icon"><Loading /></el-icon>
            </div>
          </div>
        </div>

        <!-- 输入区域 -->
        <div class="input-area">
          <el-alert
            v-if="currentConversation && !currentConversation.is_active"
            title="此对话已被禁用（管理员已更换模型配置），请创建新对话"
            type="warning"
            :closable="false"
            style="margin-bottom: 10px"
          />

          <el-input
            v-model="inputMessage"
            type="textarea"
            :rows="3"
            placeholder="请输入您的问题..."
            :disabled="!currentConversation?.is_active || isStreaming"
            @keydown.enter.ctrl="sendMessage"
          />
          <div class="input-actions">
            <span class="tip">Ctrl + Enter 发送</span>
            <el-button
              type="primary"
              :loading="isStreaming"
              :disabled="
                !inputMessage.trim() || !currentConversation?.is_active
              "
              @click="sendMessage"
            >
              发送
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, computed } from "vue";
import { useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";
import {
  Plus,
  Delete,
  User,
  ChatDotRound,
  Loading,
} from "@element-plus/icons-vue";
import { useUserStore } from "../stores/user";
import { chatAPI } from "../api/chat";
import api from "../api";
import MarkdownRenderer from "../components/MarkdownRenderer.vue";
import BackendStatus from "../components/BackendStatus.vue";

const router = useRouter();
const userStore = useUserStore();

const websiteName = ref("慢性病诊疗方案推荐系统");
const conversations = ref<any[]>([]);
const currentConversationId = ref<number | null>(null);
const messages = ref<any[]>([]);
const inputMessage = ref("");
const isStreaming = ref(false);
const streamingContent = ref("");
const messageListRef = ref<HTMLElement>();

const currentConversation = computed(() => {
  return conversations.value.find((c) => c.id === currentConversationId.value);
});

// 加载对话列表
const loadConversations = async () => {
  try {
    const res = await chatAPI.getConversations();
    conversations.value = res.data;
  } catch (error) {
    console.error("加载对话列表失败:", error);
  }
};

// 创建新对话
const createNewConversation = async () => {
  try {
    const res = await chatAPI.createConversation("新对话");
    await loadConversations();
    selectConversation(res.data.id);
    ElMessage.success("创建成功");
  } catch (error) {
    console.error("创建对话失败:", error);
  }
};

// 选择对话
const selectConversation = async (id: number) => {
  currentConversationId.value = id;
  await loadMessages(id);
};

// 加载消息
const loadMessages = async (conversationId: number) => {
  try {
    const res = await chatAPI.getMessages(conversationId);
    messages.value = res.data;
    await nextTick();
    scrollToBottom();
  } catch (error) {
    console.error("加载消息失败:", error);
  }
};

// 发送消息
const sendMessage = async () => {
  if (!inputMessage.value.trim() || !currentConversationId.value) return;
  if (!currentConversation.value?.is_active) {
    ElMessage.warning("此对话已被禁用，请创建新对话");
    return;
  }

  const content = inputMessage.value;
  inputMessage.value = "";

  // 添加用户消息到列表
  messages.value.push({
    id: Date.now(),
    role: "user",
    content: content,
    created_at: new Date().toISOString(),
  });

  await nextTick();
  scrollToBottom();

  // 发送流式请求
  isStreaming.value = true;
  streamingContent.value = "";

  try {
    const response = await chatAPI.sendMessage(
      currentConversationId.value,
      content
    );

    if (!response.ok) {
      throw new Error("发送失败");
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    if (reader) {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        streamingContent.value += chunk;

        await nextTick();
        scrollToBottom();
      }

      // 流式响应完成，添加到消息列表
      messages.value.push({
        id: Date.now(),
        role: "assistant",
        content: streamingContent.value,
        created_at: new Date().toISOString(),
      });
    }
  } catch (error) {
    console.error("发送消息失败:", error);
    ElMessage.error("发送失败，请重试");
  } finally {
    isStreaming.value = false;
    streamingContent.value = "";
  }
};

// 删除对话
const deleteConv = async (id: number) => {
  try {
    await ElMessageBox.confirm("确定要删除这个对话吗？", "提示", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });

    await chatAPI.deleteConversation(id);
    await loadConversations();

    if (currentConversationId.value === id) {
      currentConversationId.value = null;
      messages.value = [];
    }

    ElMessage.success("删除成功");
  } catch (error) {
    if (error !== "cancel") {
      console.error("删除对话失败:", error);
    }
  }
};

// 退出登录
const handleLogout = () => {
  userStore.logout();
  router.push("/login");
};

// 滚动到底部
const scrollToBottom = () => {
  if (messageListRef.value) {
    messageListRef.value.scrollTop = messageListRef.value.scrollHeight;
  }
};

// 初始化
onMounted(async () => {
  // 获取用户信息
  if (!userStore.user) {
    try {
      const res = await api.get("/api/auth/users/me");
      userStore.setUser(res.data);
    } catch (error) {
      router.push("/login");
      return;
    }
  }

  // 获取网站名称
  try {
    const res = await api.get("/api/public/settings");
    websiteName.value = res.data.website_name;
  } catch (error) {
    console.error("获取网站设置失败:", error);
  }

  // 加载对话列表
  await loadConversations();
});
</script>

<style scoped>
.chat-layout {
  display: flex;
  height: 100vh;
  background: var(--color-bgSecondary);
  overflow: hidden;
}

.sidebar {
  width: 280px;
  background: var(--color-bgPrimary);
  border-right: 1px solid var(--color-borderPrimary);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar-header {
  padding: var(--spacing-xl);
  border-bottom: 1px solid var(--color-borderPrimary);
}

.sidebar-header h2 {
  margin: 0 0 var(--spacing-base) 0;
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-primary);
}

.conversation-list {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-md);
}

.conversation-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-sm);
  border-radius: var(--border-radius-base);
  cursor: pointer;
  transition: all var(--transition-base);
}

.conversation-item:hover {
  background: var(--color-bgSecondary);
}

.conversation-item.active {
  background: var(--color-primary);
  color: var(--color-white);
}

.conversation-item.inactive {
  opacity: 0.5;
}

.conversation-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  flex: 1;
  overflow: hidden;
}

.conversation-title span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.conversation-actions {
  opacity: 0;
  transition: opacity var(--transition-base);
}

.conversation-item:hover .conversation-actions {
  opacity: 1;
}

.sidebar-footer {
  padding: var(--spacing-base);
  border-top: 1px solid var(--color-borderPrimary);
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  cursor: pointer;
  padding: var(--spacing-sm);
  border-radius: var(--border-radius-sm);
  transition: background var(--transition-base);
  color: var(--color-textPrimary);
  font-weight: 500;
}

.user-info:hover {
  background: var(--color-bgSecondary);
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--color-bgPrimary);
  overflow: hidden;
}

.welcome {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: var(--color-textTertiary);
}

.welcome h1 {
  font-size: var(--font-size-3xl);
  font-weight: 600;
  color: var(--color-textSecondary);
  margin-bottom: var(--spacing-base);
}

.welcome p {
  font-size: var(--font-size-lg);
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-xl);
}

.message {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: var(--border-radius-full);
  background: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-white);
  flex-shrink: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.message.user .message-avatar {
  background: #409eff;
}

.message-content {
  max-width: 70%;
  padding: var(--spacing-md) var(--spacing-base);
  border-radius: var(--border-radius-base);
  background: var(--color-bgSecondary);
  position: relative;
  line-height: 1.6;
}

.message.user .message-content {
  background: #e3f2fd;
}

.loading-icon {
  margin-left: var(--spacing-sm);
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.input-area {
  padding: var(--spacing-xl);
  border-top: 1px solid var(--color-borderPrimary);
  background: var(--color-bgPrimary);
  flex-shrink: 0;
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

:deep(.el-button) {
  font-weight: 500;
  transition: all var(--transition-base);
}

:deep(.el-textarea__inner) {
  font-family: var(--font-family-base);
}
</style>
