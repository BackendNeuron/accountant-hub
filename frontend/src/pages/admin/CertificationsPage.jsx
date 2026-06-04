import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { adminService } from '../../services/adminService';
import { DataTable } from './DataTable';
import { Badge } from '../../components/ui/Badge';
import { Modal } from '../../components/ui/Modal';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import './AdminPage.css';

export default function CertificationsPage() {
  const [page, setPage] = useState(1);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState({ name: '', issuing_body: '', region: '' });
  const queryClient = useQueryClient();

  const { data } = useQuery({ queryKey: ['admin', 'certifications', page], queryFn: () => adminService.list('certifications', { page }) });

  const createMutation = useMutation({
    mutationFn: (body) => adminService.create('certifications', body),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['admin', 'certifications'] }); setModalOpen(false); }
  });

  const [deleteError, setDeleteError] = useState('');

  const deleteMutation = useMutation({
    mutationFn: (id) => adminService.remove('certifications', id),
    onError: (err) => { setDeleteError(err.response?.data?.detail || 'Failed to delete'); },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin', 'certifications'] })
  });

  const columns = [
    { key: 'name', label: 'Name' },
    { key: 'issuing_body', label: 'Issuing Body', render: (r) => r.issuing_body || '—' },
    { key: 'region', label: 'Region', render: (r) => r.region || '—' },
    { key: 'is_active', label: 'Active', render: (r) => r.is_active ? '✅' : '❌' },
    { key: 'actions', label: 'Actions', render: (r) => (
      <Button size="sm" variant="danger" onClick={() => { if (confirm('Delete?')) deleteMutation.mutate(r.id); }}>Delete</Button>
    )},
  ];

    const links = [
    { to: '/admin', label: 'Dashboard' },
    { to: '/admin/users', label: 'Users' },
    { to: '/admin/jobs', label: 'Jobs' },
    { to: '/admin/bids', label: 'Bids' },
    { to: '/admin/categories', label: 'Categories' },
    { to: '/admin/certifications', label: 'Certifications' },
    { to: '/admin/software-skills', label: 'Software Skills' },
    { to: '/admin/countries', label: 'Countries' },
    { to: '/admin/documents', label: 'Documents' },
    { to: '/admin/content', label: 'Content' },
    { to: '/admin/audit-logs', label: 'Audit Logs' },
  ];

  return (
    <div className="admin-page">
            <aside className="admin-sidebar">
        <Link to="/admin" className="admin-logo">Admin Panel</Link>
        <nav>
          {links.map((link) => (
            <Link key={link.to} to={link.to}>{link.label}</Link>
          ))}
        </nav>
      </aside>
      <main className="admin-main">
        <div className="admin-navbar-row">
          <h1>Certifications</h1>
          <Button variant="primary" onClick={() => { setForm({ name: '', issuing_body: '', region: '' }); setModalOpen(true); }}>Add Certification</Button>
        </div>
        {deleteError && <div style={{ background: 'var(--color-danger-light)', color: 'var(--color-danger)', padding: '10px 14px', borderRadius: 'var(--radius-md)', marginBottom: 16, fontSize: 13 }}>{deleteError}</div>}
        <DataTable columns={columns} data={data?.data} totalPages={data?.meta?.last_page} page={page} onPageChange={setPage} />

        <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title="Add Certification">
          <Input label="Name" value={form.name} onChange={(e) => setForm({...form, name: e.target.value})} />
          <Input label="Issuing Body" value={form.issuing_body} onChange={(e) => setForm({...form, issuing_body: e.target.value})} />
          <Input label="Region" value={form.region} onChange={(e) => setForm({...form, region: e.target.value})} />
          <Button variant="primary" onClick={() => createMutation.mutate(form)} loading={createMutation.isPending}>Create</Button>
        </Modal>
      </main>
    </div>
  );
}
