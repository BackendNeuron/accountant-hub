
import api from './api';

export const profileService = {
  async getProfile() {
    const { data } = await api.get('/my-profile');
    return data.data;
  },

  async updateProfile(profileData) {
    const { data } = await api.put('/my-profile', profileData);
    return data;
  },

  async updateCertifications(data) {
    const { data: res } = await api.put('/my-profile/certifications', data);
    return res;
  },

  async updateSoftwareSkills(data) {
    const { data: res } = await api.put('/my-profile/software-skills', data);
    return res;
  },  

  async uploadDocument(formData) {
    const { data } = await api.post('/my-profile/documents', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return data;
  },

  async getDocuments() {
    const { data } = await api.get('/my-profile/documents');
    return data.data;
  },

  async deleteDocument(id) {
    const { data } = await api.delete(`/my-profile/documents/${id}`);
    return data;
  },
};

export const clientService = {
  async getMyJobs(page = 1) {
    const { data } = await api.get('/my-jobs', { params: { page } });
    return data;
  },

  async createJob(jobData) {
    const { data } = await api.post('/my-jobs', jobData);
    return data;
  },

  async updateJob(id, jobData) {
    const { data } = await api.put(`/my-jobs/${id}`, jobData);
    return data;
  },

  async updateJobStatus(id, status, closedReason = null) {
    const { data } = await api.patch(`/my-jobs/${id}/status`, { status, closed_reason: closedReason });
    return data;
  },

  async getJobBids(jobId) {
    const { data } = await api.get(`/my-jobs/${jobId}/bids`);
    return data.data;
  },

  async acceptBid(jobId, bidId) {
    const { data } = await api.patch(`/my-jobs/${jobId}/bids/${bidId}/accept`);
    return data;
  },

  async rejectBid(jobId, bidId) {
    const { data } = await api.patch(`/my-jobs/${jobId}/bids/${bidId}/reject`);
    return data;
  },
};
