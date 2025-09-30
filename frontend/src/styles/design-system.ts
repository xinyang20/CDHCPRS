/**
 * 统一设计系统配置
 * 定义全局的颜色、字体、间距、圆角等设计规范
 */

export const designSystem = {
  // 颜色系统
  colors: {
    // 主色调
    primary: '#f0a04b',
    primaryLight: '#f5d0a9',
    primaryDark: '#d88a35',
    
    // 辅助色
    success: '#67c23a',
    warning: '#e6a23c',
    danger: '#f56c6c',
    info: '#909399',
    
    // 背景色
    bgPrimary: '#ffffff',
    bgSecondary: '#f5f5f5',
    bgTertiary: '#fafafa',
    
    // 文字颜色
    textPrimary: '#333333',
    textSecondary: '#666666',
    textTertiary: '#999999',
    textDisabled: '#c0c4cc',
    
    // 边框颜色
    borderPrimary: '#e0e0e0',
    borderSecondary: '#dcdfe6',
    borderLight: '#f0f0f0',
    
    // 特殊颜色
    white: '#ffffff',
    black: '#000000',
    overlay: 'rgba(0, 0, 0, 0.5)',
  },
  
  // 字体系统
  typography: {
    // 字体家族
    fontFamily: {
      base: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif',
      mono: '"Courier New", Courier, monospace',
    },
    
    // 字体大小
    fontSize: {
      xs: '12px',
      sm: '14px',
      base: '16px',
      lg: '18px',
      xl: '20px',
      '2xl': '24px',
      '3xl': '30px',
      '4xl': '36px',
    },
    
    // 字重
    fontWeight: {
      light: 300,
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
    
    // 行高
    lineHeight: {
      tight: 1.2,
      normal: 1.5,
      relaxed: 1.75,
      loose: 2,
    },
  },
  
  // 间距系统
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '12px',
    base: '16px',
    lg: '20px',
    xl: '24px',
    '2xl': '32px',
    '3xl': '40px',
    '4xl': '48px',
    '5xl': '64px',
  },
  
  // 圆角系统
  borderRadius: {
    none: '0',
    sm: '4px',
    base: '8px',
    md: '12px',
    lg: '16px',
    xl: '20px',
    full: '9999px',
  },
  
  // 阴影系统
  shadows: {
    none: 'none',
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    base: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
  },
  
  // 过渡动画
  transitions: {
    fast: '150ms ease-in-out',
    base: '250ms ease-in-out',
    slow: '350ms ease-in-out',
  },
  
  // 断点系统（响应式）
  breakpoints: {
    xs: '480px',
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  },
  
  // Z-index 层级
  zIndex: {
    dropdown: 1000,
    sticky: 1020,
    fixed: 1030,
    modalBackdrop: 1040,
    modal: 1050,
    popover: 1060,
    tooltip: 1070,
  },
}

// 导出 CSS 变量字符串（用于全局样式）
export const generateCSSVariables = () => {
  const vars: string[] = []
  
  // 颜色变量
  Object.entries(designSystem.colors).forEach(([key, value]) => {
    vars.push(`--color-${key}: ${value};`)
  })
  
  // 字体大小变量
  Object.entries(designSystem.typography.fontSize).forEach(([key, value]) => {
    vars.push(`--font-size-${key}: ${value};`)
  })
  
  // 间距变量
  Object.entries(designSystem.spacing).forEach(([key, value]) => {
    vars.push(`--spacing-${key}: ${value};`)
  })
  
  // 圆角变量
  Object.entries(designSystem.borderRadius).forEach(([key, value]) => {
    vars.push(`--border-radius-${key}: ${value};`)
  })
  
  return vars.join('\n  ')
}

export default designSystem

