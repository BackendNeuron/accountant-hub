
import api from './api';

export const jobService = {
  async getJobs(params = {}) {
    const { data } = await api.get('/jobs', { params });
    return data;
  },

  async getJob(id) {
    const { data } = await api.get(`/jobs/${id}`);
    return data;
  },

  async getCategories() {
    const { data } = await api.get('/categories');
    return data.data;
  },

  async getCertifications() {
    const { data } = await api.get('/certifications');
    return data.data;
  },

  async getCountries() {
    const { data } = await api.get('/countries');
    return data.data;
  },

  async getContent(key) {
    const { data } = await api.get(`/content/${key}`);
    return data.data;
  },
};
