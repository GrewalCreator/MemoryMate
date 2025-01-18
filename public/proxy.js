import { createProxyMiddleware } from 'http-proxy-middleware';

export default function(app) {
  app.use(
    '/api', // Match this prefix to your endpoint
    createProxyMiddleware({
      target: 'http://127.0.0.1:5000', // Flask backend URL
      changeOrigin: true,
    })
  );
};
