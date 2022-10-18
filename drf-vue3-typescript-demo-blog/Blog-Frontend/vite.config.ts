import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'


export default defineConfig({
    plugins: [
        vue(),
    ],


    base: '/',

    server: {
        host: "localhost",
        port: 3000,
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:8000/',
                changeOrigin: true,
                ws: false,
                rewrite: (pathStr) => pathStr.replace('/api', ''),
                timeout: 5000,
            },
            '/upload': {
                target: 'http://127.0.0.1:8000/',
                changeOrigin: true,
                ws: false,
                rewrite: (pathStr) => pathStr.replace('/api', ''),
                timeout: 5000,
            },
        },
    }
});
