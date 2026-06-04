import { Link, useLocation } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { adminService } from '../../services/adminService';
import { Card } from '../../components/ui/Card';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './AdminPage.css';

const COLORS = ['#019A51', '#017A41', '#4ADE80', '#86EFAC', '#BBF7D0', '#F59E0B', '#EF4444', '#3B82F6', '#8B5CF6', '#EC4899'];

export default function AdminDashboard() {
  const location = useLocation();
  const queryClient = useQueryClient();
  
  const { data: statsData } = useQuery({ queryKey: ['admin', 'stats'], queryFn: adminService.getStats });
  const { data: toggleData } = useQuery({ queryKey: ['admin', 'audit-toggle'], queryFn: adminService.getAuditToggle });
  
  const toggleMutation = useMutation({
    mutationFn: (enabled) => adminService.toggleAudit(enabled),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin', 'audit-toggle'] }),
  });

  const stats = statsData || {};
  const auditEnabled = toggleData?.audit_enabled ?? true;

  const links = [
    { to: '/admin/users', label: 'Users' }, { to: '/admin/jobs', label: 'Jobs' },
    { to: '/admin/bids', label: 'Bids' }, { to: '/admin/categories', label: 'Categories' },
    { to: '/admin/certifications', label: 'Certifications' }, { to: '/admin/software-skills', label: 'Software Skills' },
    { to: '/admin/countries', label: 'Countries' }, { to: '/admin/documents', label: 'Documents' },
    { to: '/admin/content', label: 'Content' }, { to: '/admin/audit-logs', label: 'Audit Logs' },
  ];

  const usersByRole = stats.users_by_role || {};
  const jobsByStatus = stats.jobs_by_status || {};
  const bidsByStatus = stats.bids_by_status || {};
  const jobsTimeSeries = (stats.jobs_time_series || []).slice().reverse();
  const bidsTimeSeries = (stats.bids_time_series || []).slice().reverse();
  const usersTimeSeries = (stats.users_time_series || []).slice().reverse();
  const topAccountants = stats.top_accountants || [];
  const jobsByCategory = stats.jobs_by_category || [];

  return (
    <div className="admin-page">
      <aside className="admin-sidebar">
        <Link to="/admin" className="admin-logo">Admin Panel</Link>
        <nav>
          {links.map((link) => (
            <Link key={link.to} to={link.to} className={location.pathname === link.to ? 'active' : ''}>{link.label}</Link>
          ))}
        </nav>
      </aside>
      <main className="admin-main" style={{ background: 'var(--color-bg-page)', minHeight: '100vh' }}>
        <div className="admin-navbar-row">
          <h1>Dashboard</h1>
          <div className="audit-toggle">
            <span>Audit Logging:</span>
            <button className={'audit-toggle-switch' + (auditEnabled ? ' on' : '')} onClick={() => toggleMutation.mutate(!auditEnabled)} />
            <span>{auditEnabled ? 'ON' : 'OFF'}</span>
          </div>
        </div>

        <div className="stats-grid">
          <Card padding="lg"><h3>{stats.total_users || 0}</h3><p>Total Users</p></Card>
          <Card padding="lg"><h3>{stats.total_jobs || 0}</h3><p>Total Jobs</p></Card>
          <Card padding="lg"><h3>{stats.total_bids || 0}</h3><p>Total Bids</p></Card>
          <Card padding="lg"><h3>{usersByRole.accountant || 0}</h3><p>Accountants</p></Card>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24, marginTop: 24 }}>
          <Card padding="lg">
            <h2 style={{ marginBottom: 16, fontSize: 16 }}>Jobs Posted Over Time</h2>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={jobsTimeSeries}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
                <XAxis dataKey="date" tick={{ fontSize: 11, fill: 'var(--color-text-muted)' }} />
                <YAxis tick={{ fontSize: 11, fill: 'var(--color-text-muted)' }} />
                <Tooltip contentStyle={{ background: 'var(--color-bg-surface)', border: '1px solid var(--color-border)', borderRadius: 8 }} />
                <Line type="monotone" dataKey="count" stroke="#019A51" strokeWidth={2} dot={{ fill: '#019A51' }} animationDuration={1000} />
              </LineChart>
            </ResponsiveContainer>
          </Card>

          <Card padding="lg">
            <h2 style={{ marginBottom: 16, fontSize: 16 }}>Bids Submitted Over Time</h2>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={bidsTimeSeries}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
                <XAxis dataKey="date" tick={{ fontSize: 11, fill: 'var(--color-text-muted)' }} />
                <YAxis tick={{ fontSize: 11, fill: 'var(--color-text-muted)' }} />
                <Tooltip contentStyle={{ background: 'var(--color-bg-surface)', border: '1px solid var(--color-border)', borderRadius: 8 }} />
                <Bar dataKey="count" fill="#019A51" radius={[4, 4, 0, 0]} animationDuration={1000} />
              </BarChart>
            </ResponsiveContainer>
          </Card>

          <Card padding="lg">
            <h2 style={{ marginBottom: 16, fontSize: 16 }}>Jobs by Category</h2>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie data={jobsByCategory} dataKey="count" nameKey="name" cx="50%" cy="50%" outerRadius={90} label={({ name, percent }) => name + ' ' + (percent * 100).toFixed(0) + '%'} animationDuration={1000}>
                  {jobsByCategory.map((entry, index) => <Cell key={index} fill={COLORS[index % COLORS.length]} />)}
                </Pie>
                <Tooltip contentStyle={{ background: 'var(--color-bg-surface)', border: '1px solid var(--color-border)', borderRadius: 8 }} />
              </PieChart>
            </ResponsiveContainer>
          </Card>

          <Card padding="lg">
            <h2 style={{ marginBottom: 16, fontSize: 16 }}>Top Accountants by Bids</h2>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={topAccountants} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
                <XAxis type="number" tick={{ fontSize: 11, fill: 'var(--color-text-muted)' }} />
                <YAxis type="category" dataKey="name" width={100} tick={{ fontSize: 11, fill: 'var(--color-text-muted)' }} />
                <Tooltip contentStyle={{ background: 'var(--color-bg-surface)', border: '1px solid var(--color-border)', borderRadius: 8 }} />
                <Bar dataKey="bids" fill="#017A41" radius={[0, 4, 4, 0]} animationDuration={1000} />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24, marginTop: 24, marginBottom: 24 }}>
          <Card padding="lg">
            <h2 style={{ marginBottom: 16, fontSize: 16 }}>Users by Role</h2>
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie data={[{ name: 'Admins', value: usersByRole.admin || 0 }, { name: 'Clients', value: usersByRole.client || 0 }, { name: 'Accountants', value: usersByRole.accountant || 0 }]} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={70} label={({ name, value }) => name + ': ' + value} animationDuration={1000}>
                  <Cell fill="#F59E0B" /><Cell fill="#3B82F6" /><Cell fill="#019A51" />
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Card>

          <Card padding="lg">
            <h2 style={{ marginBottom: 16, fontSize: 16 }}>Bids by Status</h2>
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie data={[{ name: 'Pending', value: bidsByStatus.pending || 0 }, { name: 'Accepted', value: bidsByStatus.accepted || 0 }, { name: 'Rejected', value: bidsByStatus.rejected || 0 }]} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={70} label={({ name, value }) => name + ': ' + value} animationDuration={1000}>
                  <Cell fill="#F59E0B" /><Cell fill="#019A51" /><Cell fill="#EF4444" />
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Card>
        </div>
      </main>
    </div>
  );
}
