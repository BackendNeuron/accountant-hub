
import api from './api';

export const adminService = {
  getStats: async () => {
    const { data } = await api.get('/admin/dashboard/stats');
    return data.data;
  },

  // Generic CRUD helpers
  list: async (resource, params = {}) => {
    const { data } = await api.get(`/admin/${resource}`, { params });
    return data;
  },

  get: async (resource, id) => {
    const { data } = await api.get(`/admin/${resource}/${id}`);
    return data.data;
  },

  create: async (resource, body) => {
    const { data } = await api.post(`/admin/${resource}`, body);
    return data;
  },

  update: async (resource, id, body) => {
    const { data } = await api.put(`/admin/${resource}/${id}`, body);
    return data;
  },

  remove: async (resource, id) => {
    const { data } = await api.delete(`/admin/${resource}/${id}`);
    return data;
  },

  // Audit log specific
  getAuditLogs: async (params = {}) => {
    const { data } = await api.get('/admin/audit-logs', { params });
    return data;
  },

  getAuditLog: async (id) => {
    const { data } = await api.get(`/admin/audit-logs/${id}`);
    return data.data;
  },

  getAuditFilters: async () => {
    const { data } = await api.get('/admin/audit-logs/meta/filters');
    return data.data;
  },

  // Audit toggle
  getAuditToggle: async () => {
    const { data } = await api.get('/admin/me/audit-toggle');
    return data;
  },

  toggleAudit: async (enabled) => {
    const { data } = await api.patch('/admin/me/audit-toggle', { audit_enabled: enabled });
    return data;
  },

  // Restrictions
  getRestrictions: async (userId) => {
    const { data } = await api.get(`/admin/users/${userId}/restrictions`);
    return data;
  },

  setRestrictions: async (userId, restrictions) => {
    const { data } = await api.patch(`/admin/users/${userId}/restrictions`, restrictions);
    return data;
  },

  activate: async (id) => { const { data } = await api.patch('/admin/users/' + id + '/activate'); return data; },

    verifyDocument: async (id) => { const { data } = await api.patch('/admin/documents/' + id + '/verify'); return data; },

  removeRestrictions: async (userId) => {
    const { data } = await api.delete(`/admin/users/${userId}/restrictions`);
    return data;
  },
};
