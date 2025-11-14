<template>
  <div v-if="questions.length > 0" class="suggested-questions">
    <div class="questions-title">{{ $t('suggestedQuestions.title', '猜你想问') }}</div>
    <div class="questions-list">
      <div
        v-for="(question, index) in questions"
        :key="index"
        class="question-card"
        @click="handleQuestionClick(question)"
      >
        <span class="question-text">{{ question }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

interface Props {
  questions: string[]
}

const props = defineProps<Props>()
const emit = defineEmits<{
  selectQuestion: [question: string]
}>()

const handleQuestionClick = (question: string) => {
  emit('selectQuestion', question)
}
</script>

<style scoped>
.suggested-questions {
  margin: 12px 0;
  padding: 0;
}

.questions-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
  font-weight: 500;
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.question-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
}

.question-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.35);
}

.question-card:active {
  transform: translateY(0);
}

.question-text {
  color: #ffffff;
  font-size: 14px;
  line-height: 1.5;
  display: block;
}

/* 大字模式适配 */
@media (min-width: 768px) {
  .question-card {
    padding: 14px 18px;
  }

  .question-text {
    font-size: 15px;
  }
}
</style>
