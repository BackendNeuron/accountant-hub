import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { adminService } from '../../services/adminService';
import { DataTable } from './DataTable';
import { Badge } from '../../components/ui/Badge';
import { formatCurrency } from '../../utils/formatCurrency';
import { formatFullDate } from '../../utils/formatDate';
import './AdminPage.css';

export default function BidsPage() {
  const [page, setPage] = useState(1);
  const { data } = useQuery({ queryKey: ['admin', 'bids', page], queryFn: () => adminService.list('bids', { page }) });

  const columns = [
    { key: 'id', label: 'Bid ID' },
    { key: 'job_id', label: 'Job ID' },
    { key: 'accountant_id', label: 'Accountant ID' },
    { key: 'price', label: 'Price', render: (r) => formatCurrency(r.price, r.currency) },
    { key: 'pricing_model', label: 'Type' },
    { key: 'status', label: 'Status', render: (r) => <Badge variant={r.status === 'accepted' ? 'success' : r.status === 'rejected' ? 'danger' : 'warning'}>{r.status}</Badge> },
    { key: 'created_at', label: 'Submitted', render: (r) => formatFullDate(r.created_at) },
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
        <h1>Bids</h1>
        <DataTable columns={columns} data={data?.data} totalPages={data?.meta?.last_page} page={page} onPageChange={setPage} />
      </main>
    </div>
  );
}