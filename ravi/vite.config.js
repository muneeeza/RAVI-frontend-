import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/ocr': 'http://localhost:8000',
      '/tts': 'http://localhost:8000',
    },
  },
})