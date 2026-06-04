import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { adminService } from '../../services/adminService';
import { jobService } from '../../services/jobService';
import { DataTable } from './DataTable';
import { Badge } from '../../components/ui/Badge';
import { Modal } from '../../components/ui/Modal';
import { Input } from '../../components/ui/Input';
import { Select } from '../../components/ui/Select';
import { Button } from '../../components/ui/Button';
import './AdminPage.css';

export default function UsersPage() {
  const [page, setPage] = useState(1);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState({ name: '', email: '', phone: '', password: '', role: 'accountant', country_code: '', phone_digits_count: 0 });
  const [error, setError] = useState('');
  const [phoneError, setPhoneError] = useState('');
  const queryClient = useQueryClient();

  const { data } = useQuery({ queryKey: ['admin', 'users', page], queryFn: () => adminService.list('users', { page }) });
  const { data: rawCountries } = useQuery({ queryKey: ['countries'], queryFn: jobService.getCountries });

  const countries = Array.isArray(rawCountries) ? rawCountries : [];
  const countryOptions = countries.map(c => ({ value: c.country_iso_code2, label: c.country_name_en + ' (' + c.phone_code + ')' }));

  const createMutation = useMutation({
    mutationFn: (body) => adminService.create('users', body),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['admin', 'users'] }); setModalOpen(false); setError(''); },
    onError: (err) => { setError(err.response?.data?.detail || 'Failed to create user'); }
  });

  const activateMutation = useMutation({
    mutationFn: (id) => adminService.activate(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin', 'users'] })
  });

  const deleteMutation = useMutation({
    mutationFn: (id) => adminService.remove('users', id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin', 'users'] })
  });

  const handleCountryChange = (code) => {
    const country = countries.find(c => c.country_iso_code2 === code);
    setForm({ ...form, country_code: code, phone_digits_count: country?.phone_digits_count || 0 });
    setPhoneError('');
  };

  const validatePhone = (phone) => {
    if (form.phone_digits_count) {
      const digits = phone.replace(/\D/g, '');
      if (digits.length !== form.phone_digits_count) {
        setPhoneError('Phone must be exactly ' + form.phone_digits_count + ' digits');
        return false;
      }
    }
    setPhoneError('');
    return true;
  };

  const openCreate = () => { 
    setForm({ name: '', email: '', phone: '', password: '', role: 'accountant', country_code: '', phone_digits_count: 0 }); 
    setError(''); 
    setPhoneError(''); 
    setModalOpen(true); 
  };

  const handleSubmit = () => {
    setError('');
    if (!form.name || !form.email || !form.phone || !form.password) {
      setError('All fields are required');
      return;
    }
    if (!validatePhone(form.phone)) return;
    createMutation.mutate(form);
  };

  const columns = [
    { key: 'name', label: 'Name' },
    { key: 'email', label: 'Email' },
    { key: 'role', label: 'Role', render: (r) => <Badge variant={r.role === 'admin' ? 'primary' : r.role === 'client' ? 'warning' : 'success'}>{r.role}</Badge> },
    { key: 'is_active', label: 'Active', render: (r) => r.is_active ? 'Yes' : 'No' },
    { key: 'actions', label: 'Actions', render: (r) => {
      if (r.is_active) {
        return <Button size="sm" variant="danger" onClick={() => { if (confirm('Deactivate?')) deleteMutation.mutate(r.id); }}>Deactivate</Button>;
      } else {
        return <Button size="sm" variant="primary" onClick={() => activateMutation.mutate(r.id)}>Activate</Button>;
      }
    }},
  ];

  const links = [
    { to: '/admin', label: 'Dashboard' }, { to: '/admin/users', label: 'Users' }, { to: '/admin/jobs', label: 'Jobs' },
    { to: '/admin/bids', label: 'Bids' }, { to: '/admin/categories', label: 'Categories' }, { to: '/admin/certifications', label: 'Certifications' },
    { to: '/admin/software-skills', label: 'Software Skills' }, { to: '/admin/countries', label: 'Countries' },
    { to: '/admin/documents', label: 'Documents' }, { to: '/admin/content', label: 'Content' }, { to: '/admin/audit-logs', label: 'Audit Logs' },
  ];

  return (
    <div className="admin-page">
      <aside className="admin-sidebar">
        <Link to="/admin" className="admin-logo">Admin Panel</Link>
        <nav>{links.map(link => <Link key={link.to} to={link.to}>{link.label}</Link>)}</nav>
      </aside>
      <main className="admin-main">
        <div className="admin-navbar-row"><h1>Users</h1><Button variant="primary" onClick={openCreate}>Add User</Button></div>
        <DataTable columns={columns} data={data?.data} totalPages={data?.meta?.last_page} page={page} onPageChange={setPage} />

        <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title="Add User">
          {error && <div style={{ background: 'var(--color-danger-light)', color: 'var(--color-danger)', padding: '10px 14px', borderRadius: 'var(--radius-md)', marginBottom: 16, fontSize: 13 }}>{error}</div>}
          
          <Input label="Name" value={form.name} onChange={e => setForm({...form, name: e.target.value})} />
          <Input label="Email" type="email" value={form.email} onChange={e => setForm({...form, email: e.target.value})} />
          
          <Select label="Country" options={countryOptions} value={form.country_code} onChange={e => handleCountryChange(e.target.value)} placeholder="Select country..." />
          <Input label="Phone" value={form.phone} onChange={e => { setForm({...form, phone: e.target.value}); validatePhone(e.target.value); }} error={phoneError} hint={form.phone_digits_count ? 'Expected ' + form.phone_digits_count + ' digits' : ''} />
          
          <Input label="Password" type="password" value={form.password} onChange={e => setForm({...form, password: e.target.value})} />
          
          <select value={form.role} onChange={e => setForm({...form, role: e.target.value})} className="input-field" style={{ marginBottom: 16, width: '100%' }}>
            <option value="accountant">Accountant</option>
            <option value="client">Client</option>
            <option value="admin">Admin</option>
          </select>
          
          <Button variant="primary" onClick={handleSubmit} loading={createMutation.isPending}>Create</Button>
        </Modal>
      </main>
    </div>
  );
}