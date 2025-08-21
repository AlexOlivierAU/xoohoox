export const config = {
  API_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  NODE_ENV: import.meta.env.VITE_NODE_ENV || 'development',
  ANALYTICS_ID: import.meta.env.VITE_ANALYTICS_ID,
  SENTRY_DSN: import.meta.env.VITE_SENTRY_DSN,
};

export default config; 