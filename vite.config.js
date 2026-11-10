import { defineConfig } from 'vite';
import { fileURLToPath } from 'node:url';

export default defineConfig({
  base: './',
  build: { target: 'es2022', rolldownOptions: { input: {
    main: fileURLToPath(new URL('./index.html', import.meta.url)),
    fit: fileURLToPath(new URL('./fit-check.html', import.meta.url)),
  } } },
});
