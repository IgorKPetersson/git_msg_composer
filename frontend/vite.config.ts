import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// WHY Vite? Much faster than Create React App, modern tooling
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,  // Frontend runs on port 3000
    proxy: {
      // WHY proxy? Allows easy API calls to backend without CORS issues during dev
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
