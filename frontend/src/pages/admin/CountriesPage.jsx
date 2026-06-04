import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { adminService } from '../../services/adminService';
import { DataTable } from './DataTable';
import { Badge } from '../../components/ui/Badge';
import './AdminPage.css';

export default function CountriesPage() {
  const [page, setPage] = useState(1);
  const [deleteError, setDeleteError] = useState('');
  const { data } = useQuery({ queryKey: ['admin', 'countries', page], queryFn: () => adminService.list('countries', { page }) });

  const columns = [
    { key: 'country_name_en', label: 'Country' },
    { key: 'country_iso_code2', label: 'Code' },
    { key: 'currency_iso_code', label: 'Currency' },
    { key: 'phone_code', label: 'Phone Code' },
    { key: 'is_active', label: 'Active', render: (r) => r.is_active ? '✅' : '❌' },
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
        <h1>Countries</h1>
        {deleteError && <div style={{ background: 'var(--color-danger-light)', color: 'var(--color-danger)', padding: '10px 14px', borderRadius: 'var(--radius-md)', marginBottom: 16, fontSize: 13 }}>{deleteError}</div>}
        <DataTable columns={columns} data={data?.data} totalPages={data?.meta?.last_page} page={page} onPageChange={setPage} />
      </main>
    </div>
  );
}
