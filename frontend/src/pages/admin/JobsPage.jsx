import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { adminService } from '../../services/adminService';
import { DataTable } from './DataTable';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import './AdminPage.css';
import { formatCurrency } from '../../utils/formatCurrency';
import { formatDeadline } from '../../utils/formatDate';

export default function JobsPage() {
  const [page, setPage] = useState(1);
  const { data } = useQuery({ queryKey: ['admin', 'jobs', page], queryFn: () => adminService.list('jobs', { page }) });
  const queryClient = useQueryClient();

  const [deleteError, setDeleteError] = useState('');

  const deleteMutation = useMutation({
    mutationFn: (id) => adminService.remove('jobs', id),
    onError: (err) => { setDeleteError(err.response?.data?.detail || 'Failed to delete'); },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin', 'jobs'] })
  });

  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'title', label: 'Title' },
    { key: 'client_id', label: 'Client ID' },
    { key: 'budget_min', label: 'Budget', render: (r) => formatCurrency(r.budget_min, r.currency) + ' - ' + formatCurrency(r.budget_max, r.currency) },
    { key: 'status', label: 'Status', render: (r) => <Badge variant={r.status === 'open' ? 'success' : 'danger'}>{r.status}</Badge> },
    { key: 'bids_count', label: 'Bids' },
    { key: 'deadline', label: 'Deadline', render: (r) => formatDeadline(r.deadline) },
    { key: 'actions', label: 'Actions', render: (r) => (
      <Button size="sm" variant="danger" onClick={() => { if (confirm('Delete job?')) deleteMutation.mutate(r.id); }}>Delete</Button>
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
        <h1>Jobs</h1>
        {deleteError && <div style={{ background: 'var(--color-danger-light)', color: 'var(--color-danger)', padding: '10px 14px', borderRadius: 'var(--radius-md)', marginBottom: 16, fontSize: 13 }}>{deleteError}</div>}
        <DataTable columns={columns} data={data?.data} totalPages={data?.meta?.last_page} page={page} onPageChange={setPage} />
      </main>
    </div>
  );
}
