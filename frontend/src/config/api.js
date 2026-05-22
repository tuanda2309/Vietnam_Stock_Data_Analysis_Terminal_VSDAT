const rawApiUrl = import.meta.env?.VITE_API_URL || 'http://127.0.0.1:5000';

// Render Blueprint đôi khi truyền host chưa có protocol, ví dụ: vsdat-backend.onrender.com
// Local thì dùng http://127.0.0.1:5000.
const withProtocol = rawApiUrl.startsWith('http://') || rawApiUrl.startsWith('https://')
  ? rawApiUrl
  : `https://${rawApiUrl}`;

export const API_BASE_URL = withProtocol.replace(/\/$/, '');
