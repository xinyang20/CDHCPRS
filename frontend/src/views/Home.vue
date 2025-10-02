<template>
  <div class="home-container">
    <header class="header">
      <div class="header-content">
        <h1 class="logo">{{ websiteName }}</h1>
        <nav class="nav">
          <el-button text @click="scrollToSection('features')">{{ t('home.nav.features') }}</el-button>
          <el-button text @click="scrollToSection('about')">{{ t('home.nav.about') }}</el-button>
          <el-button @click="$router.push('/login')">{{ t('home.nav.login') }}</el-button>
          <el-button type="primary" @click="$router.push('/register')">{{ t('home.nav.register') }}</el-button>
        </nav>
      </div>
    </header>

    <main class="main-content">
      <section class="hero-section">
        <div class="hero-content">
          <h1 class="hero-title">{{ t('home.hero.title') }}</h1>
          <p class="hero-subtitle">{{ t('home.hero.subtitle') }}</p>
          <div class="hero-actions">
            <el-button type="primary" size="large" @click="$router.push('/register')">
              <el-icon><UserFilled /></el-icon>
              {{ t('home.hero.cta') }}
            </el-button>
            <el-button size="large" @click="$router.push('/login')">
              <el-icon><Right /></el-icon>
              {{ t('home.hero.ctaExisting') }}
            </el-button>
          </div>
        </div>
      </section>

      <section id="features" class="features-section">
        <h2 class="section-title">{{ t('home.features.title') }}</h2>
        <div class="features-grid">
          <div
            v-for="feature in featureCards"
            :key="feature.titleKey"
            class="feature-card"
          >
            <div class="feature-icon">
              <el-icon :size="48"><component :is="feature.icon" /></el-icon>
            </div>
            <h3>{{ t(feature.titleKey) }}</h3>
            <p>{{ t(feature.descriptionKey) }}</p>
          </div>
        </div>
      </section>

      <section id="about" class="about-section">
        <h2 class="section-title">{{ t('home.about.title') }}</h2>
        <div class="about-content">
          <div class="about-text">
            <h3>{{ t('home.about.heading') }}</h3>
            <p>{{ t('home.about.description1') }}</p>
            <p>{{ t('home.about.description2') }}</p>
            <el-button type="primary" @click="$router.push('/about')">
              {{ t('home.about.more') }}
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

    <footer class="footer">
      <div class="footer-content">
        <p>&copy; 2024 {{ websiteName }}. {{ t('home.footer.terms') }}</p>
        <div class="footer-links">
          <el-button text @click="$router.push('/about')">{{ t('home.footer.privacy') }}</el-button>
          <el-button text>{{ t('home.footer.terms') }}</el-button>
        </div>
      </div>
    </footer>

    <BackendStatus />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useI18n } from "vue-i18n";
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

const { t } = useI18n();

const websiteName = ref(t("common.appName"));

const featureCards = [
  { icon: ChatDotRound, titleKey: "home.features.cards.chat.title", descriptionKey: "home.features.cards.chat.description" },
  { icon: Document, titleKey: "home.features.cards.plan.title", descriptionKey: "home.features.cards.plan.description" },
  { icon: DataAnalysis, titleKey: "home.features.cards.analysis.title", descriptionKey: "home.features.cards.analysis.description" },
  { icon: Lock, titleKey: "home.features.cards.privacy.title", descriptionKey: "home.features.cards.privacy.description" },
  { icon: Clock, titleKey: "home.features.cards.service.title", descriptionKey: "home.features.cards.service.description" },
  { icon: Star, titleKey: "home.features.cards.reliable.title", descriptionKey: "home.features.cards.reliable.description" }
];

const scrollToSection = (sectionId: string) => {
  const element = document.getElementById(sectionId);
  if (element) {
    element.scrollIntoView({ behavior: "smooth" });
  }
};

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
.home-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-bgPrimary);
}

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

.main-content {
  flex: 1;
}

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

.footer {
  background: var(--color-textPrimary);
  color: var(--color-white);
  padding: var(--spacing-2xl) var(--spacing-xl);
  margin-top: auto;
}

.footer-content {
  max-width: 1280px;
  margin: 0
  auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-content p {
  margin: 0;
  font-size: var(--font-size-sm);
}

.footer-links {
  display: flex;
  gap: var(--spacing-sm);
}

.footer-links :deep(.el-button) {
  color: var(--color-white);
}

@media (max-width: 960px) {
  .about-content {
    grid-template-columns: 1fr;
  }

  .hero-actions {
    flex-direction: column;
  }

  .footer-content {
    flex-direction: column;
    gap: var(--spacing-base);
    text-align: center;
  }
}
</style>
