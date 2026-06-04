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
import { Textarea } from '../../components/ui/Textarea';

export default function ContentPage() {
  const [page, setPage] = useState(1);
  const [modalOpen, setModalOpen] = useState(false);
  const [editContent, setEditContent] = useState(null);
  const [form, setForm] = useState({ title: '', body: '' });
  const queryClient = useQueryClient();

  const { data } = useQuery({ queryKey: ['admin', 'content', page], queryFn: () => adminService.list('content', { page }) });

  const updateMutation = useMutation({
    mutationFn: ({ id, body }) => adminService.update('content', id, body),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['admin', 'content'] }); setModalOpen(false); }
  });

  const openEdit = (row) => {
    setEditContent(row);
    setForm({ title: row.title || '', body: row.body || '' });
    setModalOpen(true);
  };

  const columns = [
    { key: 'key', label: 'Key' },
    { key: 'title', label: 'Title' },
    { key: 'version', label: 'Version' },
    { key: 'is_active', label: 'Active', render: (r) => r.is_active ? '✅' : '❌' },
    { key: 'actions', label: 'Actions', render: (r) => (
      <Button size="sm" variant="primary" onClick={() => openEdit(r)}>Edit</Button>
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
        <h1>Content</h1>
        <DataTable columns={columns} data={data?.data} totalPages={data?.meta?.last_page} page={page} onPageChange={setPage} />

        <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title="Edit Content">
          <Input label="Title" value={form.title} onChange={(e) => setForm({...form, title: e.target.value})} />
          <Textarea label="Body" value={form.body} onChange={(e) => setForm({...form, body: e.target.value})} rows={8} />
          <Button variant="primary" onClick={() => updateMutation.mutate({ id: editContent?.id, body: form })} loading={updateMutation.isPending}>Update</Button>
        </Modal>
      </main>
    </div>
  );
}
