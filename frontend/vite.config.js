// frontend/vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: './', // ensures assets load correctly for SPA routes
  build: {
    outDir: 'dist',  // output folder for production build
    emptyOutDir: true, // clear the folder before building
  },
  server: {
    port: 5173,       // optional, default dev server port
    open: true,
  },
});
