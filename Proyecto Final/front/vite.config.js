import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// El proxy hace que /api/... llegue a Django sin configurar CORS en el backend
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:8000',
    },
  },
})
