<template>
  <div class="home-container">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="header-content">
        <h1 class="logo">{{ websiteName }}</h1>
        <nav class="nav">
          <el-button text @click="scrollToSection('features')">功能特性</el-button>
          <el-button text @click="scrollToSection('about')">关于系统</el-button>
          <el-button @click="$router.push('/login')">登录</el-button>
          <el-button type="primary" @click="$router.push('/register')">注册</el-button>
        </nav>
      </div>
    </header>

    <!-- 主要内容区 -->
    <main class="main-content">
      <!-- 英雄区域 -->
      <section class="hero-section">
        <div class="hero-content">
          <h1 class="hero-title">慢性病诊疗方案推荐系统</h1>
          <p class="hero-subtitle">
            基于大语言模型的智能医疗辅助系统，为慢性病患者提供专业的诊疗建议
          </p>
          <div class="hero-actions">
            <el-button type="primary" size="large" @click="$router.push('/register')">
              <el-icon><UserFilled /></el-icon>
              立即开始
            </el-button>
            <el-button size="large" @click="$router.push('/login')">
              <el-icon><Right /></el-icon>
              已有账号
            </el-button>
          </div>
        </div>
      </section>

      <!-- 功能特性区域 -->
      <section id="features" class="features-section">
        <h2 class="section-title">核心功能</h2>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon :size="48"><ChatDotRound /></el-icon>
            </div>
            <h3>智能对话</h3>
            <p>基于大语言模型的智能对话系统，提供专业的医疗咨询服务</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <el-icon :size="48"><Document /></el-icon>
            </div>
            <h3>方案推荐</h3>
            <p>根据患者症状和病史，智能推荐个性化的诊疗方案</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <el-icon :size="48"><DataAnalysis /></el-icon>
            </div>
            <h3>数据分析</h3>
            <p>全面分析患者健康数据，提供科学的健康管理建议</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <el-icon :size="48"><Lock /></el-icon>
            </div>
            <h3>隐私保护</h3>
            <p>严格的数据加密和隐私保护机制，确保患者信息安全</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <el-icon :size="48"><Clock /></el-icon>
            </div>
            <h3>24/7 服务</h3>
            <p>全天候在线服务，随时随地获取专业的医疗咨询</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <el-icon :size="48"><Star /></el-icon>
            </div>
            <h3>专业可靠</h3>
            <p>基于权威医学知识库，提供准确可靠的医疗建议</p>
          </div>
        </div>
      </section>

      <!-- 关于系统区域 -->
      <section id="about" class="about-section">
        <h2 class="section-title">关于系统</h2>
        <div class="about-content">
          <div class="about-text">
            <h3>专业的慢性病管理平台</h3>
            <p>
              本系统采用先进的大语言模型技术，结合专业的医学知识库，
              为慢性病患者提供智能化的诊疗方案推荐服务。
            </p>
            <p>
              我们致力于通过人工智能技术，帮助患者更好地理解和管理自己的健康状况，
              提供个性化的健康建议，改善生活质量。
            </p>
            <el-button type="primary" @click="$router.push('/about')">
              了解更多
              <el-icon><Right /></el-icon>
            </el-button>
          </div>
          <div class="about-image">
            <el-icon :size="200" color="var(--color-primary)">
              <Promotion />
            </el-icon>
          </div>
        </div>
      </section>
    </main>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="footer-content">
        <p>&copy; 2024 慢性病诊疗方案推荐系统. All rights reserved.</p>
        <div class="footer-links">
          <el-button text @click="$router.push('/about')">关于我们</el-button>
          <el-button text>隐私政策</el-button>
          <el-button text>使用条款</el-button>
        </div>
      </div>
    </footer>

    <!-- 后端状态指示器 -->
    <BackendStatus />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import {
  UserFilled,
  Right,
  ChatDotRound,
  Document,
  DataAnalysis,
  Lock,
  Clock,
  Star,
  Promotion,
} from "@element-plus/icons-vue";
import api from "../api";
import BackendStatus from "../components/BackendStatus.vue";

const websiteName = ref("慢性病诊疗方案推荐系统");

const scrollToSection = (sectionId: string) => {
  const element = document.getElementById(sectionId);
  if (element) {
    element.scrollIntoView({ behavior: "smooth" });
  }
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
.home-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-bgPrimary);
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
}

/* 英雄区域 */
.hero-section {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primaryLight) 100%);
  padding: var(--spacing-5xl) var(--spacing-xl);
  text-align: center;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: var(--font-size-4xl);
  font-weight: 700;
  color: var(--color-white);
  margin: 0 0 var(--spacing-lg) 0;
}

.hero-subtitle {
  font-size: var(--font-size-xl);
  color: var(--color-white);
  margin: 0 0 var(--spacing-3xl) 0;
  opacity: 0.95;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: var(--spacing-base);
  justify-content: center;
}

/* 功能特性区域 */
.features-section {
  padding: var(--spacing-5xl) var(--spacing-xl);
  background: var(--color-bgSecondary);
}

.section-title {
  text-align: center;
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: var(--color-textPrimary);
  margin: 0 0 var(--spacing-4xl) 0;
}

.features-grid {
  max-width: 1280px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-2xl);
}

.feature-card {
  background: var(--color-bgPrimary);
  padding: var(--spacing-2xl);
  border-radius: var(--border-radius-lg);
  text-align: center;
  transition: all var(--transition-base);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  color: var(--color-primary);
  margin-bottom: var(--spacing-base);
}

.feature-card h3 {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--color-textPrimary);
  margin: 0 0 var(--spacing-md) 0;
}

.feature-card p {
  font-size: var(--font-size-base);
  color: var(--color-textSecondary);
  line-height: 1.6;
  margin: 0;
}

/* 关于系统区域 */
.about-section {
  padding: var(--spacing-5xl) var(--spacing-xl);
  background: var(--color-bgPrimary);
}

.about-content {
  max-width: 1280px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-4xl);
  align-items: center;
}

.about-text h3 {
  font-size: var(--font-size-2xl);
  font-weight: 600;
  color: var(--color-textPrimary);
  margin: 0 0 var(--spacing-lg) 0;
}

.about-text p {
  font-size: var(--font-size-base);
  color: var(--color-textSecondary);
  line-height: 1.8;
  margin: 0 0 var(--spacing-base) 0;
}

.about-text .el-button {
  margin-top: var(--spacing-xl);
}

.about-image {
  display: flex;
  justify-content: center;
  align-items: center;
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
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-content p {
  margin: 0;
  opacity: 0.8;
}

.footer-links {
  display: flex;
  gap: var(--spacing-base);
}

.footer-links .el-button {
  color: var(--color-white);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-title {
    font-size: var(--font-size-3xl);
  }

  .hero-subtitle {
    font-size: var(--font-size-lg);
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .about-content {
    grid-template-columns: 1fr;
  }

  .about-image {
    order: -1;
  }

  .footer-content {
    flex-direction: column;
    gap: var(--spacing-base);
    text-align: center;
  }

  .nav {
    flex-wrap: wrap;
  }
}
</style>

