const DEFAULT_LOCAL_API_URL = 'http://127.0.0.1:5000';

const rawApiUrl = import.meta.env?.VITE_API_URL || DEFAULT_LOCAL_API_URL;

const apiUrlWithProtocol = rawApiUrl.startsWith('http://') || rawApiUrl.startsWith('https://')
  ? rawApiUrl
  : `https://${rawApiUrl}`;

export const API_BASE_URL = apiUrlWithProtocol.replace(/\/$/, '');
