/**
 * 中医慢性病问诊数据配置
 * 基于《问诊档案设计方案.md》
 */

// 疾病类型定义
export interface Disease {
  id: string;
  name: string;
  nameEn: string;
  tcmAliases: string[];  // 中医别名
  syndromes: Syndrome[];  // 证型列表
}

// 证型定义
export interface Syndrome {
  id: string;
  name: string;
  nameEn: string;
  tcmSymptoms: string[];  // 典型中医症状
  westernSymptoms?: string[];  // 典型西医症状/指标
}

// 症状定义
export interface Symptom {
  id: string;
  name: string;
  nameEn: string;
  type: 'tcm' | 'western';  // 中医症状或西医症状
}

/**
 * 慢性病数据库
 */
export const DISEASES: Disease[] = [
  {
    id: 'hypertension',
    name: '高血压',
    nameEn: 'Hypertension',
    tcmAliases: ['眩晕', '头痛', '肝风'],
    syndromes: [
      {
        id: 'hypertension_liver_yang',
        name: '肝阳上亢型',
        nameEn: 'Liver Yang Hyperactivity',
        tcmSymptoms: ['头目胀痛', '面红目赤', '口苦', '急躁易怒'],
        westernSymptoms: ['血压升高（收缩压/舒张压超过正常值）', '头痛', '头晕'],
      },
      {
        id: 'hypertension_phlegm_dampness',
        name: '痰湿中阻型',
        nameEn: 'Phlegm-Dampness Obstruction',
        tcmSymptoms: ['头晕头重（如布裹头）', '胸闷恶心', '食少多寐'],
        westernSymptoms: ['血压升高', '头晕', '胸闷'],
      },
    ],
  },
  {
    id: 'diabetes_type2',
    name: '2型糖尿病',
    nameEn: 'Type 2 Diabetes',
    tcmAliases: ['消渴'],
    syndromes: [
      {
        id: 'diabetes_lung_heat',
        name: '肺热津伤型（上消）',
        nameEn: 'Lung Heat with Fluid Damage',
        tcmSymptoms: ['烦渴多饮', '口干舌燥', '小便频数'],
        westernSymptoms: ['血糖升高（空腹/餐后）', '多饮', '多食', '多尿', '体重下降'],
      },
      {
        id: 'diabetes_stomach_heat',
        name: '胃热炽盛型（中消）',
        nameEn: 'Stomach Heat Exuberance',
        tcmSymptoms: ['多食易饥', '口渴', '形体消瘦', '大便干燥'],
        westernSymptoms: ['血糖升高', '多食', '体重下降'],
      },
      {
        id: 'diabetes_kidney_yin',
        name: '肾阴亏虚型（下消）',
        nameEn: 'Kidney Yin Deficiency',
        tcmSymptoms: ['尿频量多', '浑浊如膏', '腰膝酸软'],
        westernSymptoms: ['血糖升高', '多尿', '腰痛'],
      },
    ],
  },
  {
    id: 'coronary_disease',
    name: '冠心病',
    nameEn: 'Coronary Heart Disease',
    tcmAliases: ['胸痹', '心痛'],
    syndromes: [
      {
        id: 'coronary_blood_stasis',
        name: '心血瘀阻型',
        nameEn: 'Heart Blood Stasis',
        tcmSymptoms: ['心胸刺痛', '痛处固定', '入夜更甚', '舌质紫暗'],
        westernSymptoms: ['心绞痛（胸骨后压榨性疼痛，可放射）', '心电图异常'],
      },
      {
        id: 'coronary_phlegm_turbidity',
        name: '痰浊闭阻型',
        nameEn: 'Phlegm Turbidity Obstruction',
        tcmSymptoms: ['胸闷如窒而痛', '痰多气短', '肢体沉重'],
        westernSymptoms: ['胸痛', '胸闷', '气短'],
      },
    ],
  },
  {
    id: 'copd',
    name: '慢性阻塞性肺疾病',
    nameEn: 'COPD',
    tcmAliases: ['肺胀', '喘证'],
    syndromes: [
      {
        id: 'copd_phlegm_heat',
        name: '痰热郁肺型',
        nameEn: 'Phlegm-Heat Accumulation',
        tcmSymptoms: ['咳嗽气急', '痰黄粘稠', '胸膈烦闷', '身热口渴'],
        westernSymptoms: ['持续性呼吸困难', '咳嗽', '咳痰', '肺功能检查异常'],
      },
      {
        id: 'copd_lung_kidney',
        name: '肺肾气虚型',
        nameEn: 'Lung-Kidney Qi Deficiency',
        tcmSymptoms: ['呼吸浅短难续', '声低气怯', '甚则张口抬肩'],
        westernSymptoms: ['呼吸困难', '活动后加重'],
      },
    ],
  },
  {
    id: 'chronic_gastritis',
    name: '慢性胃炎/消化性溃疡',
    nameEn: 'Chronic Gastritis/Peptic Ulcer',
    tcmAliases: ['胃脘痛', '痞满'],
    syndromes: [
      {
        id: 'gastritis_liver_qi',
        name: '肝气犯胃型',
        nameEn: 'Liver Qi Invading Stomach',
        tcmSymptoms: ['胃脘胀痛', '痛连两胁', '嗳气频繁', '情志不舒时加重'],
        westernSymptoms: ['上腹部疼痛', '饱胀', '反酸', '嗳气', '胃镜检查可见炎症或溃疡'],
      },
      {
        id: 'gastritis_spleen_cold',
        name: '脾胃虚寒型',
        nameEn: 'Spleen-Stomach Cold Deficiency',
        tcmSymptoms: ['胃痛隐隐', '喜温喜按', '空腹痛甚', '食后缓解'],
        westernSymptoms: ['上腹部隐痛', '空腹时加重', '进食后缓解'],
      },
    ],
  },
  {
    id: 'rheumatoid_arthritis',
    name: '类风湿性关节炎',
    nameEn: 'Rheumatoid Arthritis',
    tcmAliases: ['痹证（尪痹）'],
    syndromes: [
      {
        id: 'arthritis_cold_dampness',
        name: '寒湿痹阻型',
        nameEn: 'Cold-Dampness Obstruction',
        tcmSymptoms: ['关节冷痛', '痛处固定', '得温则减', '遇寒痛增'],
        westernSymptoms: ['对称性小关节肿痛（如手、腕）', '晨僵', '类风湿因子阳性'],
      },
      {
        id: 'arthritis_liver_kidney',
        name: '肝肾亏虚型',
        nameEn: 'Liver-Kidney Deficiency',
        tcmSymptoms: ['关节畸形', '屈伸不利', '腰膝酸软'],
        westernSymptoms: ['关节变形', '活动受限', 'X光检查异常'],
      },
    ],
  },
  {
    id: 'chronic_kidney_disease',
    name: '慢性肾病',
    nameEn: 'Chronic Kidney Disease',
    tcmAliases: ['水肿', '虚劳'],
    syndromes: [
      {
        id: 'kidney_spleen_qi',
        name: '脾肾气虚型',
        nameEn: 'Spleen-Kidney Qi Deficiency',
        tcmSymptoms: ['面色无华', '腰膝酸软', '神疲乏力', '尿中泡沫增多'],
        westernSymptoms: ['蛋白尿', '血肌酐升高', '水肿', '高血压'],
      },
      {
        id: 'kidney_dampness_turbidity',
        name: '湿浊内蕴型',
        nameEn: 'Dampness-Turbidity Retention',
        tcmSymptoms: ['恶心呕吐', '口中粘腻', '食欲不振', '皮肤瘙痒'],
        westernSymptoms: ['恶心', '呕吐', '食欲下降', '皮肤瘙痒'],
      },
    ],
  },
  {
    id: 'stroke_sequelae',
    name: '脑血管病后遗症',
    nameEn: 'Stroke Sequelae',
    tcmAliases: ['中风'],
    syndromes: [
      {
        id: 'stroke_qi_blood',
        name: '气虚血瘀型',
        nameEn: 'Qi Deficiency with Blood Stasis',
        tcmSymptoms: ['半身不遂', '口眼歪斜', '言语不利', '面色苍白', '气短乏力'],
        westernSymptoms: ['肢体偏瘫', '感觉障碍', '言语不清等神经功能缺损'],
      },
      {
        id: 'stroke_liver_yang',
        name: '肝阳上亢型',
        nameEn: 'Liver Yang Hyperactivity',
        tcmSymptoms: ['半身不遂', '眩晕头痛', '面红耳赤'],
        westernSymptoms: ['肢体偏瘫', '头痛', '头晕'],
      },
    ],
  },
];

/**
 * 所有症状列表（用于症状选择器）
 */
export const ALL_SYMPTOMS: Symptom[] = [
  // 从所有疾病中提取症状
  ...DISEASES.flatMap((disease) =>
    disease.syndromes.flatMap((syndrome) => [
      ...syndrome.tcmSymptoms.map((symptom, index) => ({
        id: `${syndrome.id}_tcm_${index}`,
        name: symptom,
        nameEn: symptom, // 待补充英文翻译
        type: 'tcm' as const,
      })),
      ...(syndrome.westernSymptoms || []).map((symptom, index) => ({
        id: `${syndrome.id}_western_${index}`,
        name: symptom,
        nameEn: symptom, // 待补充英文翻译
        type: 'western' as const,
      })),
    ])
  ),
];

/**
 * 根据疾病ID获取对应的症状列表
 */
export const getSymptomsByDiseases = (diseaseIds: string[]): Symptom[] => {
  const symptoms: Symptom[] = [];
  const seenSymptoms = new Set<string>();

  diseaseIds.forEach((diseaseId) => {
    const disease = DISEASES.find((d) => d.id === diseaseId);
    if (!disease) return;

    disease.syndromes.forEach((syndrome) => {
      syndrome.tcmSymptoms.forEach((symptom, index) => {
        if (!seenSymptoms.has(symptom)) {
          symptoms.push({
            id: `${syndrome.id}_tcm_${index}`,
            name: symptom,
            nameEn: symptom,
            type: 'tcm',
          });
          seenSymptoms.add(symptom);
        }
      });

      (syndrome.westernSymptoms || []).forEach((symptom, index) => {
        if (!seenSymptoms.has(symptom)) {
          symptoms.push({
            id: `${syndrome.id}_western_${index}`,
            name: symptom,
            nameEn: symptom,
            type: 'western',
          });
          seenSymptoms.add(symptom);
        }
      });
    });
  });

  return symptoms;
};

/**
 * 根据疾病和症状推断可能的中医证型
 * 使用关键词匹配算法
 */
export const inferTcmSyndrome = (
  diseaseIds: string[],
  symptomNames: string[]
): string | null => {
  if (diseaseIds.length === 0 || symptomNames.length === 0) {
    return null;
  }

  let bestMatch: { syndrome: Syndrome; disease: Disease; score: number } | null = null;

  diseaseIds.forEach((diseaseId) => {
    const disease = DISEASES.find((d) => d.id === diseaseId);
    if (!disease) return;

    disease.syndromes.forEach((syndrome) => {
      // 计算匹配分数
      let score = 0;

      // 检查中医症状匹配
      syndrome.tcmSymptoms.forEach((tcmSymptom) => {
        if (symptomNames.some((s) => s.includes(tcmSymptom) || tcmSymptom.includes(s))) {
          score += 2; // 中医症状权重更高
        }
      });

      // 检查西医症状匹配
      (syndrome.westernSymptoms || []).forEach((westernSymptom) => {
        if (symptomNames.some((s) => s.includes(westernSymptom) || westernSymptom.includes(s))) {
          score += 1;
        }
      });

      if (score > 0 && (!bestMatch || score > bestMatch.score)) {
        bestMatch = { syndrome, disease, score };
      }
    });
  });

  if (bestMatch && bestMatch.score >= 2) {
    return `${bestMatch.disease.name} - ${bestMatch.syndrome.name}`;
  }

  return null;
};

/**
 * 获取疾病的中医别名
 */
export const getTcmAliases = (diseaseId: string): string[] => {
  const disease = DISEASES.find((d) => d.id === diseaseId);
  return disease?.tcmAliases || [];
};

/**
 * 格式化疾病和症状信息为诊断描述
 */
export const formatDiagnosisDescription = (
  diseases: string[],
  symptoms: string[],
  syndrome: string | null
): string => {
  const diseaseNames = diseases
    .map((id) => DISEASES.find((d) => d.id === id)?.name)
    .filter(Boolean)
    .join('、');

  let description = `患者主诉疾病史：${diseaseNames || '未填写'}。\n`;
  description += `近期症状：${symptoms.join('、') || '未填写'}。\n`;

  if (syndrome) {
    description += `初步分析：可能为${syndrome}。`;
  }

  return description;
};
