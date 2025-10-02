<template>
  <div class="markdown-body" v-html="renderedContent"></div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUpdated, ref } from 'vue'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

const props = defineProps<{
  content: string
}>()

const markdown: MarkdownIt = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  highlight(str: string, lang: string) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        const highlighted = hljs.highlight(str, {
          language: lang,
          ignoreIllegals: true,
        }).value
        return `<pre class="hljs"><code>${highlighted}</code></pre>`
      } catch (error) {
        console.error('Failed to highlight code block:', error)
      }
    }
    return `<pre class="hljs"><code>${markdown.utils.escapeHtml(str)}</code></pre>`
  },
})

// 处理思考过程的标记
const processThinkingContent = (content: string): string => {
  // 匹配 <think>...</think> 或类似的思考标记
  const thinkingRegex = /<think>([\s\S]*?)<\/think>/gi

  let processedContent = content.replace(thinkingRegex, (match, thinkContent) => {
    const thinkId = `think-${Math.random().toString(36).substr(2, 9)}`
    return `
      <details class="thinking-block" data-think-id="${thinkId}">
        <summary class="thinking-summary">
          <span class="thinking-icon">💭</span>
          <span class="thinking-label">思考过程</span>
          <span class="toggle-hint">(点击展开/折叠)</span>
        </summary>
        <div class="thinking-content">${markdown.render(thinkContent)}</div>
      </details>
    `
  })

  // 如果没有显式标记，检测是否有"思考"、"分析"等关键词开头的段落
  if (!thinkingRegex.test(content)) {
    const lines = processedContent.split('\n')
    let inThinking = false
    let thinkingLines: string[] = []
    const resultLines: string[] = []

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim()

      if (line.match(/^(思考|分析|推理|让我想想|让我分析|考虑到)[:：]/i)) {
        inThinking = true
        thinkingLines = [line]
      } else if (inThinking && (line.match(/^(结论|建议|答案|回答|总结)[:：]/i) || i === lines.length - 1)) {
        // 结束思考块
        if (thinkingLines.length > 0) {
          const thinkId = `think-auto-${Math.random().toString(36).substr(2, 9)}`
          resultLines.push(`
            <details class="thinking-block auto-detected" data-think-id="${thinkId}">
              <summary class="thinking-summary">
                <span class="thinking-icon">💭</span>
                <span class="thinking-label">思考过程</span>
                <span class="toggle-hint">(点击展开/折叠)</span>
              </summary>
              <div class="thinking-content">${markdown.render(thinkingLines.join('\n'))}</div>
            </details>
          `)
        }
        inThinking = false
        thinkingLines = []
        resultLines.push(line)
      } else if (inThinking) {
        thinkingLines.push(line)
      } else {
        resultLines.push(line)
      }
    }

    if (resultLines.some(l => l.includes('thinking-block'))) {
      processedContent = resultLines.join('\n')
    }
  }

  return processedContent
}

const renderedContent = computed(() => {
  const processed = processThinkingContent(props.content)
  return markdown.render(processed)
})

// 自动折叠已完成的思考过程
const autoCollapseThinking = () => {
  const thinkingBlocks = document.querySelectorAll('.thinking-block')
  thinkingBlocks.forEach((block) => {
    const details = block as HTMLDetailsElement
    // 默认展开，流式响应结束后自动折叠
    if (!details.hasAttribute('data-user-interacted')) {
      details.open = true
    }
  })
}

onMounted(() => {
  autoCollapseThinking()
})

onUpdated(() => {
  autoCollapseThinking()
})
</script>

<style scoped>
.markdown-body {
  font-size: 14px;
  line-height: 1.6;
  word-wrap: break-word;
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3),
.markdown-body :deep(h4),
.markdown-body :deep(h5),
.markdown-body :deep(h6) {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
}

.markdown-body :deep(h1) {
  font-size: 2em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 0.3em;
}

.markdown-body :deep(h2) {
  font-size: 1.5em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 0.3em;
}

.markdown-body :deep(p) {
  margin-top: 0;
  margin-bottom: 16px;
}

.markdown-body :deep(code) {
  padding: 0.2em 0.4em;
  margin: 0;
  font-size: 85%;
  background-color: rgba(27, 31, 35, 0.05);
  border-radius: 3px;
}

.markdown-body :deep(pre) {
  padding: 16px;
  overflow: auto;
  font-size: 85%;
  line-height: 1.45;
  background-color: #f6f8fa;
  border-radius: 6px;
  margin-bottom: 16px;
}

.markdown-body :deep(pre code) {
  display: inline;
  padding: 0;
  margin: 0;
  overflow: visible;
  line-height: inherit;
  word-wrap: normal;
  background-color: transparent;
  border: 0;
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  padding-left: 2em;
  margin-top: 0;
  margin-bottom: 16px;
}

.markdown-body :deep(li) {
  margin-top: 0.25em;
}

.markdown-body :deep(blockquote) {
  padding: 0 1em;
  color: #6a737d;
  border-left: 0.25em solid #dfe2e5;
  margin: 0 0 16px 0;
}

.markdown-body :deep(table) {
  border-spacing: 0;
  border-collapse: collapse;
  margin-bottom: 16px;
}

.markdown-body :deep(table th),
.markdown-body :deep(table td) {
  padding: 6px 13px;
  border: 1px solid #dfe2e5;
}

.markdown-body :deep(table tr) {
  background-color: #fff;
  border-top: 1px solid #c6cbd1;
}

.markdown-body :deep(table tr:nth-child(2n)) {
  background-color: #f6f8fa;
}

/* 思考过程折叠块样式 */
.markdown-body :deep(.thinking-block) {
  margin: 16px 0;
  border: 1px solid #e1e4e8;
  border-radius: 6px;
  background: #f8f9fa;
  overflow: hidden;
  transition: all 0.3s ease;
}

.markdown-body :deep(.thinking-block:hover) {
  border-color: #d0d7de;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.markdown-body :deep(.thinking-summary) {
  cursor: pointer;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  color: #57606a;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  user-select: none;
  transition: background 0.2s ease;
}

.markdown-body :deep(.thinking-summary:hover) {
  background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
}

.markdown-body :deep(.thinking-icon) {
  font-size: 18px;
}

.markdown-body :deep(.thinking-label) {
  font-size: 14px;
  color: #24292f;
}

.markdown-body :deep(.toggle-hint) {
  margin-left: auto;
  font-size: 12px;
  color: #6e7781;
  font-weight: 400;
}

.markdown-body :deep(.thinking-content) {
  padding: 16px;
  background: #ffffff;
  border-top: 1px solid #e1e4e8;
  animation: fadeIn 0.3s ease;
}

.markdown-body :deep(.thinking-block[open]) .thinking-summary {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  color: #1565c0;
}

.markdown-body :deep(.thinking-block[open]) .thinking-label {
  color: #0d47a1;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
