<template>
  <div class="about-container">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="header-content">
        <h1 class="logo">{{ websiteName }}</h1>
        <nav class="nav">
          <el-button @click="$router.push('/')">返回首页</el-button>
          <el-button type="primary" @click="$router.push('/login')"
            >登录</el-button
          >
        </nav>
      </div>
    </header>

    <!-- 主要内容 -->
    <main class="main-content">
      <!-- 系统介绍 -->
      <section class="intro-section">
        <div class="intro-content">
          <el-icon :size="80" color="var(--color-primary)">
            <Promotion />
          </el-icon>
          <h1>{{ websiteName }}</h1>
          <p class="version">版本 {{ version }}</p>
          <p class="description">基于大语言模型的智能慢性病诊疗方案推荐系统</p>
        </div>
      </section>

      <!-- 系统信息 -->
      <section class="info-section">
        <el-row :gutter="24">
          <el-col :xs="24" :sm="12" :md="8">
            <el-card class="info-card">
              <template #header>
                <div class="card-header">
                  <el-icon :size="24"><InfoFilled /></el-icon>
                  <span>系统简介</span>
                </div>
              </template>
              <p>
                本系统采用先进的大语言模型技术，结合专业的医学知识库，
                为慢性病患者提供智能化的诊疗方案推荐服务。
              </p>
            </el-card>
          </el-col>

          <el-col :xs="24" :sm="12" :md="8">
            <el-card class="info-card">
              <template #header>
                <div class="card-header">
                  <el-icon :size="24"><Star /></el-icon>
                  <span>核心特性</span>
                </div>
              </template>
              <ul>
                <li>智能对话交互</li>
                <li>个性化方案推荐</li>
                <li>数据安全保护</li>
                <li>24/7 在线服务</li>
              </ul>
            </el-card>
          </el-col>

          <el-col :xs="24" :sm="12" :md="8">
            <el-card class="info-card">
              <template #header>
                <div class="card-header">
                  <el-icon :size="24"><Tools /></el-icon>
                  <span>技术栈</span>
                </div>
              </template>
              <ul>
                <li>前端: Vue 3 + TypeScript</li>
                <li>后端: FastAPI + Python</li>
                <li>AI: 大语言模型</li>
                <li>数据库: SQLite</li>
              </ul>
            </el-card>
          </el-col>
        </el-row>
      </section>

      <!-- 功能模块 -->
      <section class="features-section">
        <h2>主要功能模块</h2>
        <el-timeline>
          <el-timeline-item
            v-for="(feature, index) in features"
            :key="index"
            :icon="feature.icon"
            :color="feature.color"
          >
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
          </el-timeline-item>
        </el-timeline>
      </section>

      <!-- 联系信息 -->
      <!-- <section class="contact-section">
        <h2>联系我们</h2>
        <el-descriptions :column="1" border>
          <el-descriptions-item label="项目地址">
            <el-link href="https://github.com/xinyang20/CDHCPRS" target="_blank" type="primary">
              GitHub Repository
            </el-link>
          </el-descriptions-item>
          <el-descriptions-item label="开发者">
            Xinyang Gao
          </el-descriptions-item>
          <el-descriptions-item label="许可证">
            MIT License
          </el-descriptions-item>
          <el-descriptions-item label="最后更新">
            {{ lastUpdate }}
          </el-descriptions-item>
        </el-descriptions>
      </section> -->

      <!-- 免责声明 -->
      <section class="disclaimer-section">
        <el-alert title="免责声明" type="warning" :closable="false">
          <p>
            本系统提供的诊疗建议仅供参考，不能替代专业医生的诊断和治疗。
            如有健康问题，请及时就医并遵循医生的专业建议。
          </p>
        </el-alert>
      </section>
    </main>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="footer-content">
        <p>&copy; 2024 慢性病诊疗方案推荐系统. All rights reserved.</p>
      </div>
    </footer>

    <!-- 后端状态指示器 -->
    <BackendStatus />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import {
  Promotion,
  InfoFilled,
  Star,
  Tools,
  ChatDotRound,
  User,
  Setting,
  Lock,
} from "@element-plus/icons-vue";
import api from "../api";
import BackendStatus from "../components/BackendStatus.vue";

const websiteName = ref("慢性病诊疗方案推荐系统");
const version = ref("1.0.0");
const lastUpdate = ref(new Date().toLocaleDateString("zh-CN"));

const features = [
  {
    title: "用户认证系统",
    description: "安全的用户注册、登录和权限管理功能",
    icon: User,
    color: "#409eff",
  },
  {
    title: "智能对话系统",
    description: "基于大语言模型的智能对话，提供专业的医疗咨询",
    icon: ChatDotRound,
    color: "#67c23a",
  },
  {
    title: "方案推荐引擎",
    description: "根据患者情况智能推荐个性化的诊疗方案",
    icon: Star,
    color: "#e6a23c",
  },
  {
    title: "管理后台",
    description: "完善的系统管理功能，包括用户管理、对话管理和系统设置",
    icon: Setting,
    color: "#f56c6c",
  },
  {
    title: "数据安全",
    description: "严格的数据加密和隐私保护机制",
    icon: Lock,
    color: "#909399",
  },
];

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
.about-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-bgSecondary);
}

/* 顶部导航栏 */
.header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--color-bgPrimary);
  border-bottom: 1px solid var(--color-borderPrimary);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.header-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: var(--spacing-base) var(--spacing-xl);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--color-primary);
  margin: 0;
}

.nav {
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
}

/* 主要内容 */
.main-content {
  flex: 1;
  max-width: 1280px;
  width: 100%;
  margin: 0 auto;
  padding: var(--spacing-4xl) var(--spacing-xl);
}

/* 系统介绍 */
.intro-section {
  text-align: center;
  padding: var(--spacing-4xl) 0;
}

.intro-content h1 {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: var(--color-textPrimary);
  margin: var(--spacing-lg) 0 var(--spacing-md) 0;
}

.version {
  font-size: var(--font-size-base);
  color: var(--color-textTertiary);
  margin: 0 0 var(--spacing-base) 0;
}

.description {
  font-size: var(--font-size-lg);
  color: var(--color-textSecondary);
  margin: 0;
}

/* 系统信息 */
.info-section {
  margin: var(--spacing-4xl) 0;
}

.info-card {
  height: 100%;
  transition: all var(--transition-base);
}

.info-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-weight: 600;
  color: var(--color-textPrimary);
}

.info-card p {
  color: var(--color-textSecondary);
  line-height: 1.8;
  margin: 0;
}

.info-card ul {
  margin: 0;
  padding-left: var(--spacing-lg);
  color: var(--color-textSecondary);
}

.info-card li {
  margin-bottom: var(--spacing-sm);
  line-height: 1.6;
}

/* 功能模块 */
.features-section {
  margin: var(--spacing-4xl) 0;
  background: var(--color-bgPrimary);
  padding: var(--spacing-3xl);
  border-radius: var(--border-radius-lg);
}

.features-section h2 {
  font-size: var(--font-size-2xl);
  font-weight: 600;
  color: var(--color-textPrimary);
  margin: 0 0 var(--spacing-2xl) 0;
}

.features-section h3 {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-textPrimary);
  margin: 0 0 var(--spacing-sm) 0;
}

.features-section p {
  color: var(--color-textSecondary);
  line-height: 1.6;
  margin: 0;
}

/* 联系信息 */
.contact-section {
  margin: var(--spacing-4xl) 0;
}

.contact-section h2 {
  font-size: var(--font-size-2xl);
  font-weight: 600;
  color: var(--color-textPrimary);
  margin: 0 0 var(--spacing-xl) 0;
}

/* 免责声明 */
.disclaimer-section {
  margin: var(--spacing-4xl) 0;
}

.disclaimer-section p {
  margin: 0;
  line-height: 1.8;
}

/* 页脚 */
.footer {
  background: var(--color-textPrimary);
  color: var(--color-white);
  padding: var(--spacing-2xl) var(--spacing-xl);
  margin-top: auto;
}

.footer-content {
  max-width: 1280px;
  margin: 0 auto;
  text-align: center;
}

.footer-content p {
  margin: 0;
  opacity: 0.8;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .intro-content h1 {
    font-size: var(--font-size-2xl);
  }

  .features-section {
    padding: var(--spacing-xl);
  }
}
</style>
