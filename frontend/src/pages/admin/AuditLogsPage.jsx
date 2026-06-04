import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { adminService } from '../../services/adminService';
import { DataTable } from './DataTable';
import { Card } from '../../components/ui/Card';
import { formatFullDate } from '../../utils/formatDate';
import './AdminPage.css';

export default function AuditLogsPage() {
  const [page, setPage] = useState(1);
  const [filters, setFilters] = useState({});

  const { data } = useQuery({
    queryKey: ['admin', 'audit-logs', page, filters],
    queryFn: () => adminService.getAuditLogs({ ...filters, page }),
  });

  const columns = [
    { key: 'action', label: 'Action' },
    { key: 'user_email', label: 'User' },
    { key: 'action_category', label: 'Category' },
    { key: 'entity_type', label: 'Entity' },
    { key: 'entity_id', label: 'Entity ID' },
    { key: 'description', label: 'Description', render: (r) => (r.description || '').substring(0, 80) || '-' },
    { key: 'created_at', label: 'Date', render: (r) => formatFullDate(r.created_at) },
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
        <h1>Audit Logs</h1>
        <div className="audit-filters">
          <select onChange={(e) => { setFilters({...filters, action_category: e.target.value}); setPage(1); }}>
            <option value="">All Categories</option>
            <option value="authentication">Authentication</option>
            <option value="profile">Profile</option>
            <option value="job">Job</option>
            <option value="bid">Bid</option>
            <option value="nda">NDA</option>
            <option value="document">Document</option>
            <option value="admin">Admin</option>
            <option value="content">Content</option>
          </select>
          <select onChange={(e) => { setFilters({...filters, user_role: e.target.value}); setPage(1); }}>
            <option value="">All Roles</option>
            <option value="admin">Admin</option>
            <option value="client">Client</option>
            <option value="accountant">Accountant</option>
          </select>
        </div>
        {data?.data && data.data.length > 0 ? (
          <DataTable columns={columns} data={data.data} totalPages={data.meta?.last_page || 1} page={page} onPageChange={setPage} />
        ) : (
          <Card padding="lg"><p>No audit logs found. Audit logging may be disabled or no actions have been recorded yet.</p></Card>
        )}
      </main>
    </div>
  );
}
