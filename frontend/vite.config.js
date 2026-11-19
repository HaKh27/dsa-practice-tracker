import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/get-problems': 'http://127.0.0.1:5000',
      '/add-problem': 'http://127.0.0.1:5000',
      '/delete-problem': 'http://127.0.0.1:5000',
      '/edit-topic': 'http://127.0.0.1:5000',
      '/search-by-name': 'http://127.0.0.1:5000',
      '/search-by-topic': 'http://127.0.0.1:5000',
      '/update-field': 'http://127.0.0.1:5000',
      '/filter-difficulty': 'http://127.0.0.1:5000',
      '/filter-problems': 'http://127.0.0.1:5000',
      '/distinct-topic': 'http://127.0.0.1:5000',
      '/reviewed': 'http://127.0.0.1:5000',
    },
  },
})
