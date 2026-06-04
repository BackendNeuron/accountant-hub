
import api from './api';

export const authService = {
  async login(email, password) {
    const { data } = await api.post('/auth/login', { email, password });
    return data;
  },

  async register(userData) {
    const { data } = await api.post('/auth/register', userData);
    return data;
  },

  async getMe() {
    const token = sessionStorage.getItem('ah_token');
    if (!token) return null;
    const { data } = await api.get('/my-profile');
    return data.data;
  },
};
