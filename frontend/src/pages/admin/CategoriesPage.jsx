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

export default function CategoriesPage() {
  const [page, setPage] = useState(1);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState({ name: '', slug: '', parent_id: '', description: '', sort_order: 0 });
  const queryClient = useQueryClient();

  const { data } = useQuery({ queryKey: ['admin', 'categories', page], queryFn: () => adminService.list('categories', { page }) });

  const createMutation = useMutation({
    mutationFn: (body) => adminService.create('categories', body),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['admin', 'categories'] }); setModalOpen(false); }
  });

  const [deleteError, setDeleteError] = useState('');

  const deleteMutation = useMutation({
      mutationFn: (id) => adminService.remove('categories', id),
      onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['admin', 'categories'] }); setDeleteError(''); },
      onError: (err) => { setDeleteError(err.response?.data?.detail || 'Failed to delete'); }
    });

  const columns = [
    { key: 'name', label: 'Name' },
    { key: 'slug', label: 'Slug' },
    { key: 'parent_id', label: 'Parent ID', render: (r) => r.parent_id || '—' },
    { key: 'sort_order', label: 'Sort Order' },
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
          <h1>Categories</h1>
          <Button variant="primary" onClick={() => { setForm({ name: '', slug: '', parent_id: '', description: '', sort_order: 0 }); setModalOpen(true); }}>Add Category</Button>
        </div>
        {deleteError && <div style={{ background: 'var(--color-danger-light)', color: 'var(--color-danger)', padding: '10px 14px', borderRadius: 'var(--radius-md)', marginBottom: 16, fontSize: 13 }}>{deleteError}</div>}
        <DataTable columns={columns} data={data?.data} totalPages={data?.meta?.last_page} page={page} onPageChange={setPage} />

        <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title="Add Category">
          <Input label="Name" value={form.name} onChange={(e) => setForm({...form, name: e.target.value})} />
          <Input label="Slug" value={form.slug} onChange={(e) => setForm({...form, slug: e.target.value})} />
          <Input label="Parent ID (optional)" value={form.parent_id} onChange={(e) => setForm({...form, parent_id: e.target.value})} />
          <Input label="Sort Order" type="number" value={form.sort_order} onChange={(e) => setForm({...form, sort_order: parseInt(e.target.value) || 0})} />
          <Button variant="primary" onClick={() => createMutation.mutate(form)} loading={createMutation.isPending}>Create</Button>
        </Modal>
      </main>
    </div>
  );
}
