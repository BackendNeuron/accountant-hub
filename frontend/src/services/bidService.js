
import api from './api';

export const bidService = {
  async submitBid(jobId, bidData) {
    const { data } = await api.post(`/jobs/${jobId}/bids`, bidData);
    return data;
  },

  async getMyBids(page = 1) {
    const { data } = await api.get('/my-bids', { params: { page } });
    return data;
  },

  async acceptNda(jobId) {
    const { data } = await api.post(`/jobs/${jobId}/accept-nda`, { agree: true });
    return data;
  },

  async getMatchScore(jobId) {
    const { data } = await api.get(`/jobs/${jobId}/match-score`);
    return data.data;
  },
};
