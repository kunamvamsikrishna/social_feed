import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          });

          const { access, refresh } = response.data;
          localStorage.setItem('access_token', access);
          if (refresh) {
            localStorage.setItem('refresh_token', refresh);
          }

          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (userData) => api.post('/auth/register/', userData),
  login: (credentials) => api.post('/auth/login/', credentials),
  logout: (refreshToken) => api.post('/auth/logout/', { refresh: refreshToken }),
  getProfile: () => api.get('/auth/profile/'),
  updateProfile: (data) => api.patch('/auth/profile/', data),
};

// Communities API
export const communitiesAPI = {
  getAll: (page = 1) => api.get(`/communities/?page=${page}`),
  getById: (id) => api.get(`/communities/${id}/`),
  create: (data) => api.post('/communities/', data),
  update: (id, data) => api.patch(`/communities/${id}/`, data),
  delete: (id) => api.delete(`/communities/${id}/`),
  join: (id) => api.post(`/communities/${id}/join/`),
  leave: (id) => api.post(`/communities/${id}/leave/`),
  getMembers: (id) => api.get(`/communities/${id}/members/`),
};

// Posts API
export const postsAPI = {
  getAll: (page = 1, communityId = null) => {
    const url = communityId 
      ? `/posts/?community=${communityId}&page=${page}`
      : `/posts/?page=${page}`;
    return api.get(url);
  },
  getCommunityFeed: (communityId, page = 1) => 
    api.get(`/posts/community/${communityId}/?page=${page}`),
  getById: (id) => api.get(`/posts/${id}/`),
  create: (data) => api.post('/posts/', data),
  update: (id, data) => api.patch(`/posts/${id}/`, data),
  delete: (id) => api.delete(`/posts/${id}/`),
  toggleLike: (id) => api.post(`/posts/${id}/like/`),
  getLikes: (id) => api.get(`/posts/${id}/likes/`),
};

export default api;
