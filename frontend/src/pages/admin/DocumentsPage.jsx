import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { adminService } from '../../services/adminService';
import { DataTable } from './DataTable';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import './AdminPage.css';
import { formatFullDate } from '../../utils/formatDate';

export default function DocumentsPage() {
  const [page, setPage] = useState(1);
  const { data } = useQuery({ queryKey: ['admin', 'documents', page], queryFn: () => adminService.list('documents', { page }) });
  const queryClient = useQueryClient();

  const verifyMutation = useMutation({
    mutationFn: (id) => adminService.verifyDocument(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin', 'documents'] })
  });

  const [deleteError, setDeleteError] = useState('');

  const deleteMutation = useMutation({
    mutationFn: (id) => adminService.remove('documents', id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin', 'documents'] })
  });

  const columns = [
    { key: 'document_type', label: 'Type' },
    { key: 'file_name', label: 'File Name' },
    { key: 'is_verified', label: 'Verified', render: (r) => r.is_verified ? '✅' : '❌' },
    { key: 'uploaded_at', label: 'Uploaded', render: (r) => formatFullDate(r.uploaded_at) },
    { key: 'actions', label: 'Actions', render: (r) => (
      <div style={{ display: 'flex', gap: 8 }}>
        {!r.is_verified && <Button size="sm" variant="primary" onClick={() => verifyMutation.mutate(r.id)}>Verify</Button>}
        <Button size="sm" variant="danger" onClick={() => { if (confirm('Delete?')) deleteMutation.mutate(r.id); }}>Delete</Button>
      </div>
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
        <h1>Documents</h1>
        {deleteError && <div style={{ background: 'var(--color-danger-light)', color: 'var(--color-danger)', padding: '10px 14px', borderRadius: 'var(--radius-md)', marginBottom: 16, fontSize: 13 }}>{deleteError}</div>}
        <DataTable columns={columns} data={data?.data} totalPages={data?.meta?.last_page} page={page} onPageChange={setPage} />
      </main>
    </div>
  );
}
