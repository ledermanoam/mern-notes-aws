import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    include: ['../Tests/frontend/**/*.test.{js,jsx}'],
    globals: false,
  },
});
