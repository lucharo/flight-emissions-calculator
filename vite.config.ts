import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
  resolve: {
    alias: {
      $lib: path.resolve('./src/lib')
    }
  },
  optimizeDeps: {
    include: [
      'leaflet',
      '@internationalized/date',
      'class-variance-authority',
      'clsx',
      'cmdk-sv',
      'tailwind-merge',
      'tailwind-variants'
    ]
  },
  build: {
    rollupOptions: {
      input: path.resolve(__dirname, 'index.html')
    }
  }
})
