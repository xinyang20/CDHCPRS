<template>
  <div class="admin-container">
    <!-- 后端状态指示器 -->
    <BackendStatus />

    <el-container>
      <el-header>
        <div class="header-content">
          <h2>管理员后台</h2>
          <el-button @click="$router.push('/chat')">返回对话</el-button>
        </div>
      </el-header>

      <el-container>
        <el-aside width="200px">
          <el-menu :default-active="activeMenu" @select="handleMenuSelect">
            <el-menu-item index="users">
              <el-icon><User /></el-icon>
              <span>用户管理</span>
            </el-menu-item>
            <el-menu-item index="conversations">
              <el-icon><ChatDotRound /></el-icon>
              <span>对话管理</span>
            </el-menu-item>
            <el-menu-item index="settings">
              <el-icon><Setting /></el-icon>
              <span>系统设置</span>
            </el-menu-item>
          </el-menu>
        </el-aside>

        <el-main>
          <!-- 用户管理 -->
          <div v-if="activeMenu === 'users'">
            <h3>用户管理</h3>
            <el-table :data="users" border>
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="username" label="用户名" />
              <el-table-column prop="role" label="角色" width="100">
                <template #default="{ row }">
                  <el-tag :type="row.role === 'admin' ? 'danger' : 'primary'">
                    {{ row.role === "admin" ? "管理员" : "普通用户" }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="is_banned" label="状态" width="100">
                <template #default="{ row }">
                  <el-tag :type="row.is_banned ? 'danger' : 'success'">
                    {{ row.is_banned ? "已封禁" : "正常" }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="created_at" label="注册时间" width="180">
                <template #default="{ row }">
                  {{ formatDate(row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200">
                <template #default="{ row }">
                  <el-button
                    v-if="!row.is_banned"
                    type="warning"
                    size="small"
                    @click="banUser(row.id)"
                  >
                    封禁
                  </el-button>
                  <el-button
                    v-else
                    type="success"
                    size="small"
                    @click="unbanUser(row.id)"
                  >
                    解封
                  </el-button>
                  <el-button
                    type="danger"
                    size="small"
                    @click="deleteUser(row.id)"
                  >
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>

          <!-- 对话管理 -->
          <div v-if="activeMenu === 'conversations'">
            <h3>对话管理</h3>
            <el-table :data="conversations" border>
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="title" label="标题" />
              <el-table-column prop="user_id" label="用户ID" width="100" />
              <el-table-column prop="is_active" label="状态" width="100">
                <template #default="{ row }">
                  <el-tag :type="row.is_active ? 'success' : 'info'">
                    {{ row.is_active ? "活跃" : "已禁用" }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="created_at" label="创建时间" width="180">
                <template #default="{ row }">
                  {{ formatDate(row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="100">
                <template #default="{ row }">
                  <el-button
                    type="danger"
                    size="small"
                    @click="deleteConversation(row.id)"
                  >
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>

          <!-- 系统设置 -->
          <div v-if="activeMenu === 'settings'">
            <h3>系统设置</h3>
            <el-form
              :model="settingsForm"
              label-width="120px"
              style="max-width: 600px"
            >
              <el-form-item label="网站名称">
                <el-input v-model="settingsForm.website_name" />
              </el-form-item>

              <el-form-item label="系统提示词">
                <el-input
                  v-model="settingsForm.system_prompt"
                  type="textarea"
                  :rows="4"
                />
              </el-form-item>

              <el-divider />

              <el-form-item label="LLM 提供商">
                <el-select v-model="settingsForm.llm_provider">
                  <el-option label="DeepSeek" value="deepseek" />
                  <el-option label="Qwen" value="qwen" />
                  <el-option label="OpenAI" value="openai" />
                </el-select>
              </el-form-item>

              <el-form-item label="API Key">
                <el-input v-model="settingsForm.llm_api_key" type="password" />
              </el-form-item>

              <el-form-item label="模型 ID">
                <el-input v-model="settingsForm.llm_model_id" />
              </el-form-item>

              <el-form-item>
                <el-button
                  type="primary"
                  @click="testConnection"
                  :loading="testing"
                >
                  测试连接
                </el-button>
                <el-button
                  type="success"
                  @click="saveSettings"
                  :loading="saving"
                >
                  保存设置
                </el-button>
              </el-form-item>

              <el-alert
                title="注意：修改模型配置后，所有历史对话将被禁用"
                type="warning"
                :closable="false"
              />
            </el-form>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { User, ChatDotRound, Setting } from "@element-plus/icons-vue";
import { adminAPI } from "../api/admin";
import BackendStatus from "../components/BackendStatus.vue";

const activeMenu = ref("users");
const users = ref<any[]>([]);
const conversations = ref<any[]>([]);
const testing = ref(false);
const saving = ref(false);

const settingsForm = reactive({
  website_name: "",
  website_logo: "",
  system_prompt: "",
  llm_provider: "deepseek",
  llm_api_key: "",
  llm_model_id: "deepseek-chat",
});

const handleMenuSelect = (index: string) => {
  activeMenu.value = index;
  if (index === "users") {
    loadUsers();
  } else if (index === "conversations") {
    loadConversations();
  } else if (index === "settings") {
    loadSettings();
  }
};

const loadUsers = async () => {
  try {
    const res = await adminAPI.getUsers();
    users.value = res.data;
  } catch (error) {
    console.error("加载用户列表失败:", error);
  }
};

const banUser = async (userId: number) => {
  try {
    await ElMessageBox.confirm("确定要封禁此用户吗？", "提示", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });

    await adminAPI.updateUser(userId, { is_banned: true });
    ElMessage.success("封禁成功");
    loadUsers();
  } catch (error) {
    if (error !== "cancel") {
      console.error("封禁用户失败:", error);
    }
  }
};

const unbanUser = async (userId: number) => {
  try {
    await adminAPI.updateUser(userId, { is_banned: false });
    ElMessage.success("解封成功");
    loadUsers();
  } catch (error) {
    console.error("解封用户失败:", error);
  }
};

const deleteUser = async (userId: number) => {
  try {
    await ElMessageBox.confirm("确定要删除此用户吗？此操作不可恢复！", "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "error",
    });

    await adminAPI.deleteUser(userId);
    ElMessage.success("删除成功");
    loadUsers();
  } catch (error) {
    if (error !== "cancel") {
      console.error("删除用户失败:", error);
    }
  }
};

const loadConversations = async () => {
  try {
    const res = await adminAPI.getAllConversations();
    conversations.value = res.data;
  } catch (error) {
    console.error("加载对话列表失败:", error);
  }
};

const deleteConversation = async (conversationId: number) => {
  try {
    await ElMessageBox.confirm("确定要删除此对话吗？", "提示", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });

    await adminAPI.deleteConversation(conversationId);
    ElMessage.success("删除成功");
    loadConversations();
  } catch (error) {
    if (error !== "cancel") {
      console.error("删除对话失败:", error);
    }
  }
};

const loadSettings = async () => {
  try {
    const res = await adminAPI.getSettings();
    Object.assign(settingsForm, res.data);
  } catch (error) {
    console.error("加载设置失败:", error);
  }
};

const testConnection = async () => {
  testing.value = true;
  try {
    await adminAPI.testConnection({
      llm_provider: settingsForm.llm_provider,
      llm_api_key: settingsForm.llm_api_key,
      llm_model_id: settingsForm.llm_model_id,
    });
    ElMessage.success("连接测试成功");
  } catch (error) {
    console.error("连接测试失败:", error);
  } finally {
    testing.value = false;
  }
};

const saveSettings = async () => {
  saving.value = true;
  try {
    await adminAPI.updateSettings(settingsForm);
    ElMessage.success("保存成功");
  } catch (error) {
    console.error("保存设置失败:", error);
  } finally {
    saving.value = false;
  }
};

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString("zh-CN");
};

onMounted(() => {
  loadUsers();
});
</script>

<style scoped>
.admin-container {
  height: 100vh;
  overflow: hidden;
}

.el-header {
  background: var(--color-bgPrimary);
  border-bottom: 1px solid var(--color-borderPrimary);
  display: flex;
  align-items: center;
}

.header-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h2 {
  margin: 0;
  color: var(--color-primary);
  font-size: var(--font-size-2xl);
  font-weight: 600;
}

.el-aside {
  background: var(--color-bgPrimary);
  border-right: 1px solid var(--color-borderPrimary);
  overflow-y: auto;
}

.el-main {
  background: var(--color-bgSecondary);
  overflow-y: auto;
}

h3 {
  margin-top: 0;
  margin-bottom: var(--spacing-lg);
  color: var(--color-textPrimary);
  font-size: var(--font-size-xl);
  font-weight: 600;
}

:deep(.el-button) {
  font-weight: 500;
  transition: all var(--transition-base);
}

:deep(.el-table) {
  font-size: var(--font-size-sm);
}

:deep(.el-menu-item) {
  transition: all var(--transition-base);
}
</style>
