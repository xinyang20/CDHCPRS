<template>
  <el-card class="user-info-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <span class="card-title">{{ t('chat.infoDialogTitle') }}</span>
        <el-text size="small" type="info">{{ t('chat.patientProfileHint') }}</el-text>
      </div>
    </template>

    <el-form :model="formData" label-width="80px" class="user-info-form">
      <el-form-item :label="t('chat.age')">
        <el-input-number
          v-model="formData.age"
          :min="1"
          :max="150"
          :placeholder="t('chat.agePlaceholder')"
          style="width: 100%"
        />
      </el-form-item>

      <el-form-item :label="t('chat.gender')">
        <el-radio-group v-model="formData.gender">
          <el-radio value="male">{{ t('chat.genderMale') }}</el-radio>
          <el-radio value="female">{{ t('chat.genderFemale') }}</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item :label="t('chat.mainSymptom')">
        <el-input
          v-model="formData.mainSymptom"
          type="textarea"
          :rows="3"
          :placeholder="t('chat.mainSymptomPlaceholder')"
        />
      </el-form-item>

      <el-form-item :label="t('chat.medicalHistory')">
        <el-input
          v-model="formData.medicalHistory"
          type="textarea"
          :rows="3"
          :placeholder="t('chat.medicalHistoryPlaceholder')"
        />
      </el-form-item>

      <el-form-item :label="t('chat.allergies')">
        <el-input
          v-model="formData.allergies"
          :placeholder="t('chat.allergiesPlaceholder')"
        />
      </el-form-item>

      <div class="form-actions">
        <el-button @click="handleSkip" v-if="!hasData">{{ t('chat.skipForm') }}</el-button>
        <el-button type="primary" @click="handleSubmit">
          {{ hasData ? t('chat.updateInfo') : t('chat.submitInfo') }}
        </el-button>
      </div>
    </el-form>
  </el-card>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'
import { useI18n } from 'vue-i18n'

export interface UserInfo {
  age?: number
  gender?: 'male' | 'female' | ''
  mainSymptom?: string
  medicalHistory?: string
  allergies?: string
}

const props = defineProps<{
  initialData?: UserInfo
}>()

const emit = defineEmits<{
  submit: [data: UserInfo]
  skip: []
}>()

const { t } = useI18n()

const formData = reactive<UserInfo>({
  age: props.initialData?.age,
  gender: props.initialData?.gender || '',
  mainSymptom: props.initialData?.mainSymptom || '',
  medicalHistory: props.initialData?.medicalHistory || '',
  allergies: props.initialData?.allergies || '',
})

const hasData = computed(() => {
  return !!(formData.age || formData.gender || formData.mainSymptom || formData.medicalHistory || formData.allergies)
})

const handleSubmit = () => {
  emit('submit', { ...formData })
}

const handleSkip = () => {
  emit('skip')
}

// 对外暴露获取数据的方法
defineExpose({
  getData: () => ({ ...formData }),
  hasData,
})
</script>

<style scoped>
.user-info-card {
  border-radius: var(--border-radius-lg);
  margin-bottom: var(--spacing-lg);
}

.card-header {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-textPrimary);
}

.user-info-form {
  margin-top: var(--spacing-md);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-lg);
}
</style>
