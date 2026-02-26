import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: process.env.NODE_ENV === 'production' ? '/static/' : '/',
  build: {
    manifest: true,
    outDir: 'dist',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        about: 'src/about.jsx',
        contact: 'src/contact.jsx',
        index: 'src/index.jsx',
        cart: 'src/cart.jsx',
        product_list: 'src/product_list.jsx',
        product_detail: 'src/product_detail.jsx',
        sign_in: 'src/sign_in.jsx',
        sign_up: 'src/sign_up.jsx',
      },
    },
  },
  server: {
    origin: 'http://localhost:5173',
  },
})
