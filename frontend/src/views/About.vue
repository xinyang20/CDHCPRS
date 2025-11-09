<template>
  <div class="about-container">
    <header class="header">
      <div class="header-content">
        <h1 class="logo">{{ websiteName }}</h1>
        <nav class="nav">
          <LargeFontModeSwitcher />
          <LanguageSwitcher />
          <el-button @click="$router.push('/')">{{
            t("common.actions.back")
          }}</el-button>
          <el-button type="primary" @click="$router.push('/login')">{{
            t("home.nav.login")
          }}</el-button>
        </nav>
      </div>
    </header>

    <main class="main-content">
      <section class="intro-section">
        <div class="intro-content">
          <el-icon :size="80" color="var(--color-primary)">
            <Promotion />
          </el-icon>
          <h1>{{ websiteName }}</h1>
          <p class="version">{{ t("about.version") }} {{ version }}</p>
          <p class="description">{{ t("about.intro") }}</p>
        </div>
      </section>

      <section class="info-section">
        <el-row :gutter="24">
          <el-col :xs="24" :sm="12" :md="8">
            <el-card class="info-card">
              <template #header>
                <div class="card-header">
                  <el-icon :size="24"><InfoFilled /></el-icon>
                  <span>{{ t("admin.settings.basic") }}</span>
                </div>
              </template>
              <p>{{ t("about.systemIntro") }}</p>
            </el-card>
          </el-col>

          <el-col :xs="24" :sm="12" :md="8">
            <el-card class="info-card">
              <template #header>
                <div class="card-header">
                  <el-icon :size="24"><Star /></el-icon>
                  <span>{{ t("home.features.title") }}</span>
                </div>
              </template>
              <ul>
                <li>{{ t("about.featureList.auth") }}</li>
                <li>{{ t("about.featureList.chat") }}</li>
                <li>{{ t("about.featureList.plan") }}</li>
                <li>{{ t("about.featureList.security") }}</li>
              </ul>
            </el-card>
          </el-col>

          <el-col :xs="24" :sm="12" :md="8">
            <el-card class="info-card">
              <template #header>
                <div class="card-header">
                  <el-icon :size="24"><Tools /></el-icon>
                  <span>Tech Stack</span>
                </div>
              </template>
              <ul>
                <li>Frontend: Vue 3 + TypeScript</li>
                <li>Backend: FastAPI + Python</li>
                <li>AI: OpenAI-compatible LLMs</li>
                <li>Database: SQLite</li>
              </ul>
            </el-card>
          </el-col>
        </el-row>
      </section>

      <section class="features-section">
        <h2>{{ t("home.features.title") }}</h2>
        <el-timeline>
          <el-timeline-item
            v-for="feature in featureTimeline"
            :key="feature.title"
            :icon="feature.icon"
            :color="feature.color"
          >
            <h3>{{ t(feature.title) }}</h3>
            <p>{{ t(feature.description) }}</p>
          </el-timeline-item>
        </el-timeline>
      </section>

      <section class="disclaimer-section">
        <el-alert
          :title="t('about.disclaimer')"
          type="warning"
          :closable="false"
        />
      </section>
    </main>

    <footer class="footer">
      <div class="footer-content">
        <p>&copy; 2024 {{ websiteName }}. {{ t("home.footer.terms") }}</p>
      </div>
    </footer>

    <BackendStatus />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";
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
import LanguageSwitcher from "../components/LanguageSwitcher.vue";
import LargeFontModeSwitcher from "../components/LargeFontModeSwitcher.vue";

const { t } = useI18n();

const websiteName = ref(t("common.appName"));
const version = ref("1.0.0");

const featureTimeline = [
  {
    title: "about.featureList.auth",
    description: "about.featureList.auth",
    icon: User,
    color: "#409eff",
  },
  {
    title: "about.featureList.chat",
    description: "about.featureList.chat",
    icon: ChatDotRound,
    color: "#67c23a",
  },
  {
    title: "about.featureList.plan",
    description: "about.featureList.plan",
    icon: Star,
    color: "#e6a23c",
  },
  {
    title: "about.featureList.security",
    description: "about.featureList.security",
    icon: Lock,
    color: "#909399",
  },
  {
    title: "admin.menu.settings",
    description: "admin.settings.title",
    icon: Setting,
    color: "#f56c6c",
  },
];

onMounted(async () => {
  try {
    const res = await api.get("/api/public/settings");
    websiteName.value = res.data.website_name || t("common.appName");
  } catch (error) {
    console.error("Failed to fetch site settings:", error);
  }
});
</script>

<style scoped>
.about-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-bgSecondary);
  overflow: hidden;
}

.header {
  flex-shrink: 0;
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

.main-content {
  flex: 1;
  max-width: 1280px;
  width: 100%;
  margin: 0 auto;
  padding: var(--spacing-4xl) var(--spacing-xl);
  overflow-y: auto;
  overflow-x: hidden;
}

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

.info-card p,
.info-card ul {
  color: var(--color-textSecondary);
  line-height: 1.8;
  margin: 0;
  padding-left: var(--spacing-base);
}

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

.disclaimer-section {
  margin: var(--spacing-4xl) 0;
}

.footer {
  flex-shrink: 0;
  background: var(--color-textPrimary);
  color: var(--color-white);
  padding: var(--spacing-2xl) var(--spacing-xl);
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

@media (max-width: 768px) {
  .intro-content h1 {
    font-size: var(--font-size-2xl);
  }

  .features-section {
    padding: var(--spacing-xl);
  }
}
</style>
