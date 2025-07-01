import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path' // Import path module

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'), // Setup path alias for @/*
    },
  },
  server: {
    // Configuration for the dev server
    port: 3000, // Optional: specify port
    proxy: {
      // Proxy API requests to the backend to avoid CORS issues during development
      '/api': { // Assuming your FastAPI backend is served at / (or you mount it at /api)
                // If FastAPI serves at root (e.g. /entities), then proxy path might need to be /entities etc.
                // For now, let's assume FastAPI endpoints are not prefixed with /api
                // and we will call them directly, handling CORS on the backend if needed for dev.
                // Or, if FastAPI is at http://localhost:8000, then:
        target: 'http://localhost:8000', // Your FastAPI backend URL
        changeOrigin: true,
        // rewrite: (path) => path.replace(/^\/api/, '') // Remove /api prefix if backend doesn't expect it
      }
    }
  }
})
