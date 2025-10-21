import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // 从项目根目录加载环境变量
  const env = loadEnv(mode, '..', '')

  return {
    plugins: [vue()],

    // 从根目录读取 .env 文件
    envDir: '..',

    // 开发服务器配置
    server: {
      port: parseInt(env.FRONTEND_PORT || '5173'),
      host: true,
      open: false,
    },
  }
})
