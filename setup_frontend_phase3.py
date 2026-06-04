"""
Fix all Admin Frontend Pages
Run: python fix_admin_pages.py
"""
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend", "src", "pages", "admin")

SIDEBAR_LINKS = """  const links = [
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
  ];"""

SIDEBAR_JSX = """      <aside className="admin-sidebar">
        <Link to="/admin" className="admin-logo">Admin Panel</Link>
        <nav>
          {links.map((link) => (
            <Link key={link.to} to={link.to}>{link.label}</Link>
          ))}
        </nav>
      </aside>"""

IMPORTS_BASE = """import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { adminService } from '../../services/adminService';
import { DataTable } from './DataTable';
import { Badge } from '../../components/ui/Badge';
import './AdminPage.css';"""

IMPORTS_WITH_MODAL = """import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { adminService } from '../../services/adminService';
import { DataTable } from './DataTable';
import { Badge } from '../../components/ui/Badge';
import { Modal } from '../../components/ui/Modal';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import './AdminPage.css';"""

FILES = {}

# =============================================
# USERS PAGE
# =============================================
FILES["UsersPage.jsx"] = f'''{IMPORTS_WITH_MODAL}

export default function UsersPage() {{
  const [page, setPage] = useState(1);
  const [modalOpen, setModalOpen] = useState(false);
  const [editUser, setEditUser] = useState(null);
  const [form, setForm] = useState({{ name: '', email: '', phone: '', password: '', role: 'accountant' }});
  const queryClient = useQueryClient();

  const {{ data }} = useQuery({{ queryKey: ['admin', 'users', page], queryFn: () => adminService.list('users', {{ page }}) }});

  const createMutation = useMutation({{
    mutationFn: (body) => adminService.create('users', body),
    onSuccess: () => {{ queryClient.invalidateQueries({{ queryKey: ['admin', 'users'] }}); setModalOpen(false); }}
  }});

  const deleteMutation = useMutation({{
    mutationFn: (id) => adminService.remove('users', id),
    onSuccess: () => queryClient.invalidateQueries({{ queryKey: ['admin', 'users'] }})
  }});

  const openCreate = () => {{ setEditUser(null); setForm({{ name: '', email: '', phone: '', password: '', role: 'accountant' }}); setModalOpen(true); }};

  const handleSubmit = () => {{
    if (editUser) {{
      // update logic
    }} else {{
      createMutation.mutate(form);
    }}
  }};

  const columns = [
    {{ key: 'name', label: 'Name' }},
    {{ key: 'email', label: 'Email' }},
    {{ key: 'role', label: 'Role', render: (r) => <Badge variant={{r.role === 'admin' ? 'primary' : r.role === 'client' ? 'warning' : 'success'}}>{{r.role}}</Badge> }},
    {{ key: 'is_active', label: 'Active', render: (r) => r.is_active ? '✅' : '❌' }},
    {{ key: 'actions', label: 'Actions', render: (r) => (
      <div style={{{{ display: 'flex', gap: 8 }}}}>
        <Button size="sm" variant="ghost" onClick={{() => deleteMutation.mutate(r.id)}}>Delete</Button>
      </div>
    )}},
  ];

  {SIDEBAR_LINKS}

  return (
    <div className="admin-page">
      {SIDEBAR_JSX}
      <main className="admin-main">
        <div className="admin-navbar-row">
          <h1>Users</h1>
          <Button variant="primary" onClick={{openCreate}}>Add User</Button>
        </div>
        <DataTable columns={{columns}} data={{data?.data}} totalPages={{data?.meta?.last_page}} page={{page}} onPageChange={{setPage}} />

        <Modal isOpen={{modalOpen}} onClose={{() => setModalOpen(false)}} title={{editUser ? 'Edit User' : 'Add User'}}>
          <Input label="Name" value={{form.name}} onChange={{(e) => setForm({{...form, name: e.target.value}})}} />
          <Input label="Email" value={{form.email}} onChange={{(e) => setForm({{...form, email: e.target.value}})}} />
          <Input label="Phone" value={{form.phone}} onChange={{(e) => setForm({{...form, phone: e.target.value}})}} />
          {{!editUser && <Input label="Password" type="password" value={{form.password}} onChange={{(e) => setForm({{...form, password: e.target.value}})}} />}}
          <select value={{form.role}} onChange={{(e) => setForm({{...form, role: e.target.value}})}} className="input-field" style={{{{ marginBottom: 16, width: '100%' }}}}>
            <option value="accountant">Accountant</option>
            <option value="client">Client</option>
            <option value="admin">Admin</option>
          </select>
          <Button variant="primary" onClick={{handleSubmit}} loading={{createMutation.isPending}}>{{editUser ? 'Update' : 'Create'}}</Button>
        </Modal>
      </main>
    </div>
  );
}}
'''

# =============================================
# JOBS PAGE
# =============================================
FILES["JobsPage.jsx"] = f'''{IMPORTS_BASE}
import {{ formatCurrency }} from '../../utils/formatCurrency';
import {{ formatDeadline }} from '../../utils/formatDate';

export default function JobsPage() {{
  const [page, setPage] = useState(1);
  const {{ data }} = useQuery({{ queryKey: ['admin', 'jobs', page], queryFn: () => adminService.list('jobs', {{ page }}) }});
  const queryClient = useQueryClient();

  const deleteMutation = useMutation({{
    mutationFn: (id) => adminService.remove('jobs', id),
    onSuccess: () => queryClient.invalidateQueries({{ queryKey: ['admin', 'jobs'] }})
  }});

  const columns = [
    {{ key: 'id', label: 'ID' }},
    {{ key: 'title', label: 'Title' }},
    {{ key: 'client_id', label: 'Client ID' }},
    {{ key: 'budget_min', label: 'Budget', render: (r) => formatCurrency(r.budget_min, r.currency) + ' - ' + formatCurrency(r.budget_max, r.currency) }},
    {{ key: 'status', label: 'Status', render: (r) => <Badge variant={{r.status === 'open' ? 'success' : 'danger'}}>{{r.status}}</Badge> }},
    {{ key: 'bids_count', label: 'Bids' }},
    {{ key: 'deadline', label: 'Deadline', render: (r) => formatDeadline(r.deadline) }},
    {{ key: 'actions', label: 'Actions', render: (r) => (
      <Button size="sm" variant="danger" onClick={{() => {{ if (confirm('Delete job?')) deleteMutation.mutate(r.id); }}}}>Delete</Button>
    )}},
  ];

  {SIDEBAR_LINKS}

  return (
    <div className="admin-page">
      {SIDEBAR_JSX}
      <main className="admin-main">
        <h1>Jobs</h1>
        <DataTable columns={{columns}} data={{data?.data}} totalPages={{data?.meta?.last_page}} page={{page}} onPageChange={{setPage}} />
      </main>
    </div>
  );
}}
'''

# =============================================
# CATEGORIES PAGE
# =============================================
FILES["CategoriesPage.jsx"] = f'''{IMPORTS_WITH_MODAL}

export default function CategoriesPage() {{
  const [page, setPage] = useState(1);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState({{ name: '', slug: '', parent_id: '', description: '', sort_order: 0 }});
  const queryClient = useQueryClient();

  const {{ data }} = useQuery({{ queryKey: ['admin', 'categories', page], queryFn: () => adminService.list('categories', {{ page }}) }});

  const createMutation = useMutation({{
    mutationFn: (body) => adminService.create('categories', body),
    onSuccess: () => {{ queryClient.invalidateQueries({{ queryKey: ['admin', 'categories'] }}); setModalOpen(false); }}
  }});

  const deleteMutation = useMutation({{
    mutationFn: (id) => adminService.remove('categories', id),
    onSuccess: () => queryClient.invalidateQueries({{ queryKey: ['admin', 'categories'] }})
  }});

  const columns = [
    {{ key: 'name', label: 'Name' }},
    {{ key: 'slug', label: 'Slug' }},
    {{ key: 'parent_id', label: 'Parent ID', render: (r) => r.parent_id || '—' }},
    {{ key: 'sort_order', label: 'Sort Order' }},
    {{ key: 'is_active', label: 'Active', render: (r) => r.is_active ? '✅' : '❌' }},
    {{ key: 'actions', label: 'Actions', render: (r) => (
      <Button size="sm" variant="danger" onClick={{() => {{ if (confirm('Delete?')) deleteMutation.mutate(r.id); }}}}>Delete</Button>
    )}},
  ];

  {SIDEBAR_LINKS}

  return (
    <div className="admin-page">
      {SIDEBAR_JSX}
      <main className="admin-main">
        <div className="admin-navbar-row">
          <h1>Categories</h1>
          <Button variant="primary" onClick={{() => {{ setForm({{ name: '', slug: '', parent_id: '', description: '', sort_order: 0 }}); setModalOpen(true); }}}}>Add Category</Button>
        </div>
        <DataTable columns={{columns}} data={{data?.data}} totalPages={{data?.meta?.last_page}} page={{page}} onPageChange={{setPage}} />

        <Modal isOpen={{modalOpen}} onClose={{() => setModalOpen(false)}} title="Add Category">
          <Input label="Name" value={{form.name}} onChange={{(e) => setForm({{...form, name: e.target.value}})}} />
          <Input label="Slug" value={{form.slug}} onChange={{(e) => setForm({{...form, slug: e.target.value}})}} />
          <Input label="Parent ID (optional)" value={{form.parent_id}} onChange={{(e) => setForm({{...form, parent_id: e.target.value}})}} />
          <Input label="Sort Order" type="number" value={{form.sort_order}} onChange={{(e) => setForm({{...form, sort_order: parseInt(e.target.value) || 0}})}} />
          <Button variant="primary" onClick={{() => createMutation.mutate(form)}} loading={{createMutation.isPending}}>Create</Button>
        </Modal>
      </main>
    </div>
  );
}}
'''

# =============================================
# CERTIFICATIONS PAGE
# =============================================
FILES["CertificationsPage.jsx"] = f'''{IMPORTS_WITH_MODAL}

export default function CertificationsPage() {{
  const [page, setPage] = useState(1);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState({{ name: '', issuing_body: '', region: '' }});
  const queryClient = useQueryClient();

  const {{ data }} = useQuery({{ queryKey: ['admin', 'certifications', page], queryFn: () => adminService.list('certifications', {{ page }}) }});

  const createMutation = useMutation({{
    mutationFn: (body) => adminService.create('certifications', body),
    onSuccess: () => {{ queryClient.invalidateQueries({{ queryKey: ['admin', 'certifications'] }}); setModalOpen(false); }}
  }});

  const deleteMutation = useMutation({{
    mutationFn: (id) => adminService.remove('certifications', id),
    onSuccess: () => queryClient.invalidateQueries({{ queryKey: ['admin', 'certifications'] }})
  }});

  const columns = [
    {{ key: 'name', label: 'Name' }},
    {{ key: 'issuing_body', label: 'Issuing Body', render: (r) => r.issuing_body || '—' }},
    {{ key: 'region', label: 'Region', render: (r) => r.region || '—' }},
    {{ key: 'is_active', label: 'Active', render: (r) => r.is_active ? '✅' : '❌' }},
    {{ key: 'actions', label: 'Actions', render: (r) => (
      <Button size="sm" variant="danger" onClick={{() => {{ if (confirm('Delete?')) deleteMutation.mutate(r.id); }}}}>Delete</Button>
    )}},
  ];

  {SIDEBAR_LINKS}

  return (
    <div className="admin-page">
      {SIDEBAR_JSX}
      <main className="admin-main">
        <div className="admin-navbar-row">
          <h1>Certifications</h1>
          <Button variant="primary" onClick={{() => {{ setForm({{ name: '', issuing_body: '', region: '' }}); setModalOpen(true); }}}}>Add Certification</Button>
        </div>
        <DataTable columns={{columns}} data={{data?.data}} totalPages={{data?.meta?.last_page}} page={{page}} onPageChange={{setPage}} />

        <Modal isOpen={{modalOpen}} onClose={{() => setModalOpen(false)}} title="Add Certification">
          <Input label="Name" value={{form.name}} onChange={{(e) => setForm({{...form, name: e.target.value}})}} />
          <Input label="Issuing Body" value={{form.issuing_body}} onChange={{(e) => setForm({{...form, issuing_body: e.target.value}})}} />
          <Input label="Region" value={{form.region}} onChange={{(e) => setForm({{...form, region: e.target.value}})}} />
          <Button variant="primary" onClick={{() => createMutation.mutate(form)}} loading={{createMutation.isPending}}>Create</Button>
        </Modal>
      </main>
    </div>
  );
}}
'''

# =============================================
# SOFTWARE SKILLS PAGE
# =============================================
FILES["SoftwareSkillsPage.jsx"] = f'''{IMPORTS_WITH_MODAL}

export default function SoftwareSkillsPage() {{
  const [page, setPage] = useState(1);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState({{ name: '' }});
  const queryClient = useQueryClient();

  const {{ data }} = useQuery({{ queryKey: ['admin', 'software-skills', page], queryFn: () => adminService.list('software-skills', {{ page }}) }});

  const createMutation = useMutation({{
    mutationFn: (body) => adminService.create('software-skills', body),
    onSuccess: () => {{ queryClient.invalidateQueries({{ queryKey: ['admin', 'software-skills'] }}); setModalOpen(false); }}
  }});

  const deleteMutation = useMutation({{
    mutationFn: (id) => adminService.remove('software-skills', id),
    onSuccess: () => queryClient.invalidateQueries({{ queryKey: ['admin', 'software-skills'] }})
  }});

  const columns = [
    {{ key: 'name', label: 'Name' }},
    {{ key: 'is_active', label: 'Active', render: (r) => r.is_active ? '✅' : '❌' }},
    {{ key: 'actions', label: 'Actions', render: (r) => (
      <Button size="sm" variant="danger" onClick={{() => {{ if (confirm('Delete?')) deleteMutation.mutate(r.id); }}}}>Delete</Button>
    )}},
  ];

  {SIDEBAR_LINKS}

  return (
    <div className="admin-page">
      {SIDEBAR_JSX}
      <main className="admin-main">
        <div className="admin-navbar-row">
          <h1>Software Skills</h1>
          <Button variant="primary" onClick={{() => {{ setForm({{ name: '' }}); setModalOpen(true); }}}}>Add Skill</Button>
        </div>
        <DataTable columns={{columns}} data={{data?.data}} totalPages={{data?.meta?.last_page}} page={{page}} onPageChange={{setPage}} />

        <Modal isOpen={{modalOpen}} onClose={{() => setModalOpen(false)}} title="Add Software Skill">
          <Input label="Name" value={{form.name}} onChange={{(e) => setForm({{...form, name: e.target.value}})}} />
          <Button variant="primary" onClick={{() => createMutation.mutate(form)}} loading={{createMutation.isPending}}>Create</Button>
        </Modal>
      </main>
    </div>
  );
}}
'''

# =============================================
# COUNTRIES PAGE
# =============================================
FILES["CountriesPage.jsx"] = f'''{IMPORTS_BASE}

export default function CountriesPage() {{
  const [page, setPage] = useState(1);
  const {{ data }} = useQuery({{ queryKey: ['admin', 'countries', page], queryFn: () => adminService.list('countries', {{ page }}) }});

  const columns = [
    {{ key: 'country_name_en', label: 'Country' }},
    {{ key: 'country_iso_code2', label: 'Code' }},
    {{ key: 'currency_iso_code', label: 'Currency' }},
    {{ key: 'phone_code', label: 'Phone Code' }},
    {{ key: 'is_active', label: 'Active', render: (r) => r.is_active ? '✅' : '❌' }},
  ];

  {SIDEBAR_LINKS}

  return (
    <div className="admin-page">
      {SIDEBAR_JSX}
      <main className="admin-main">
        <h1>Countries</h1>
        <DataTable columns={{columns}} data={{data?.data}} totalPages={{data?.meta?.last_page}} page={{page}} onPageChange={{setPage}} />
      </main>
    </div>
  );
}}
'''

# =============================================
# DOCUMENTS PAGE
# =============================================
FILES["DocumentsPage.jsx"] = f'''{IMPORTS_BASE}
import {{ formatFullDate }} from '../../utils/formatDate';

export default function DocumentsPage() {{
  const [page, setPage] = useState(1);
  const {{ data }} = useQuery({{ queryKey: ['admin', 'documents', page], queryFn: () => adminService.list('documents', {{ page }}) }});
  const queryClient = useQueryClient();

  const verifyMutation = useMutation({{
    mutationFn: (id) => adminService.update('documents', id, {{}}),
    onSuccess: () => queryClient.invalidateQueries({{ queryKey: ['admin', 'documents'] }})
  }});

  const deleteMutation = useMutation({{
    mutationFn: (id) => adminService.remove('documents', id),
    onSuccess: () => queryClient.invalidateQueries({{ queryKey: ['admin', 'documents'] }})
  }});

  const columns = [
    {{ key: 'document_type', label: 'Type' }},
    {{ key: 'file_name', label: 'File Name' }},
    {{ key: 'is_verified', label: 'Verified', render: (r) => r.is_verified ? '✅' : '❌' }},
    {{ key: 'uploaded_at', label: 'Uploaded', render: (r) => formatFullDate(r.uploaded_at) }},
    {{ key: 'actions', label: 'Actions', render: (r) => (
      <div style={{{{ display: 'flex', gap: 8 }}}}>
        {{!r.is_verified && <Button size="sm" variant="primary" onClick={{() => verifyMutation.mutate(r.id)}}>Verify</Button>}}
        <Button size="sm" variant="danger" onClick={{() => {{ if (confirm('Delete?')) deleteMutation.mutate(r.id); }}}}>Delete</Button>
      </div>
    )}},
  ];

  {SIDEBAR_LINKS}

  return (
    <div className="admin-page">
      {SIDEBAR_JSX}
      <main className="admin-main">
        <h1>Documents</h1>
        <DataTable columns={{columns}} data={{data?.data}} totalPages={{data?.meta?.last_page}} page={{page}} onPageChange={{setPage}} />
      </main>
    </div>
  );
}}
'''

# =============================================
# CONTENT PAGE
# =============================================
FILES["ContentPage.jsx"] = f'''{IMPORTS_WITH_MODAL}
import {{ Textarea }} from '../../components/ui/Textarea';

export default function ContentPage() {{
  const [page, setPage] = useState(1);
  const [modalOpen, setModalOpen] = useState(false);
  const [editContent, setEditContent] = useState(null);
  const [form, setForm] = useState({{ title: '', body: '' }});
  const queryClient = useQueryClient();

  const {{ data }} = useQuery({{ queryKey: ['admin', 'content', page], queryFn: () => adminService.list('content', {{ page }}) }});

  const updateMutation = useMutation({{
    mutationFn: ({{ id, body }}) => adminService.update('content', id, body),
    onSuccess: () => {{ queryClient.invalidateQueries({{ queryKey: ['admin', 'content'] }}); setModalOpen(false); }}
  }});

  const openEdit = (row) => {{
    setEditContent(row);
    setForm({{ title: row.title || '', body: row.body || '' }});
    setModalOpen(true);
  }};

  const columns = [
    {{ key: 'key', label: 'Key' }},
    {{ key: 'title', label: 'Title' }},
    {{ key: 'version', label: 'Version' }},
    {{ key: 'is_active', label: 'Active', render: (r) => r.is_active ? '✅' : '❌' }},
    {{ key: 'actions', label: 'Actions', render: (r) => (
      <Button size="sm" variant="primary" onClick={{() => openEdit(r)}}>Edit</Button>
    )}},
  ];

  {SIDEBAR_LINKS}

  return (
    <div className="admin-page">
      {SIDEBAR_JSX}
      <main className="admin-main">
        <h1>Content</h1>
        <DataTable columns={{columns}} data={{data?.data}} totalPages={{data?.meta?.last_page}} page={{page}} onPageChange={{setPage}} />

        <Modal isOpen={{modalOpen}} onClose={{() => setModalOpen(false)}} title="Edit Content">
          <Input label="Title" value={{form.title}} onChange={{(e) => setForm({{...form, title: e.target.value}})}} />
          <Textarea label="Body" value={{form.body}} onChange={{(e) => setForm({{...form, body: e.target.value}})}} rows={{8}} />
          <Button variant="primary" onClick={{() => updateMutation.mutate({{ id: editContent?.id, body: form }})}} loading={{updateMutation.isPending}}>Update</Button>
        </Modal>
      </main>
    </div>
  );
}}
'''

# =============================================
# ADMIN DASHBOARD (UPDATED WITH MORE STATS)
# =============================================
FILES["AdminDashboard.jsx"] = f'''import {{ Link, useLocation }} from 'react-router-dom';
import {{ useQuery, useMutation, useQueryClient }} from '@tanstack/react-query';
import {{ adminService }} from '../../services/adminService';
import {{ Card }} from '../../components/ui/Card';
import './AdminPage.css';

export default function AdminDashboard() {{
  const location = useLocation();
  const queryClient = useQueryClient();
  
  const {{ data: statsData }} = useQuery({{ queryKey: ['admin', 'stats'], queryFn: adminService.getStats }});
  const {{ data: toggleData }} = useQuery({{ queryKey: ['admin', 'audit-toggle'], queryFn: adminService.getAuditToggle }});
  
  const toggleMutation = useMutation({{
    mutationFn: (enabled) => adminService.toggleAudit(enabled),
    onSuccess: () => queryClient.invalidateQueries({{ queryKey: ['admin', 'audit-toggle'] }}),
  }});

  const stats = statsData || {{}};
  const auditEnabled = toggleData?.audit_enabled ?? true;

  const links = [
    {{ to: '/admin/users', label: 'Users' }},
    {{ to: '/admin/jobs', label: 'Jobs' }},
    {{ to: '/admin/bids', label: 'Bids' }},
    {{ to: '/admin/categories', label: 'Categories' }},
    {{ to: '/admin/certifications', label: 'Certifications' }},
    {{ to: '/admin/software-skills', label: 'Software Skills' }},
    {{ to: '/admin/countries', label: 'Countries' }},
    {{ to: '/admin/documents', label: 'Documents' }},
    {{ to: '/admin/content', label: 'Content' }},
    {{ to: '/admin/audit-logs', label: 'Audit Logs' }},
  ];

  const usersByRole = stats.users_by_role || {{}};
  const jobsByStatus = stats.jobs_by_status || {{}};
  const bidsByStatus = stats.bids_by_status || {{}};

  return (
    <div className="admin-page">
      <aside className="admin-sidebar">
        <Link to="/admin" className="admin-logo">Admin Panel</Link>
        <nav>
          {{links.map((link) => (
            <Link key={{link.to}} to={{link.to}} className={{location.pathname === link.to ? 'active' : ''}}>{{link.label}}</Link>
          ))}}
        </nav>
      </aside>
      <main className="admin-main">
        <div className="admin-navbar-row">
          <h1>Dashboard</h1>
          <div className="audit-toggle">
            <span>Audit Logging:</span>
            <button 
              className={{'audit-toggle-switch' + (auditEnabled ? ' on' : '')}}
              onClick={{() => toggleMutation.mutate(!auditEnabled)}}
            />
            <span>{{auditEnabled ? 'ON' : 'OFF'}}</span>
          </div>
        </div>

        <h2 style={{{{ marginBottom: 16, marginTop: 8 }}}}>Overview</h2>
        <div className="stats-grid">
          <Card padding="lg"><h3>{{stats.total_users || 0}}</h3><p>Total Users</p></Card>
          <Card padding="lg"><h3>{{stats.total_jobs || 0}}</h3><p>Total Jobs</p></Card>
          <Card padding="lg"><h3>{{stats.total_bids || 0}}</h3><p>Total Bids</p></Card>
        </div>

        <h2 style={{{{ marginBottom: 16, marginTop: 32 }}}}>Users by Role</h2>
        <div className="stats-grid">
          <Card padding="lg"><h3>{{usersByRole.admin || 0}}</h3><p>Admins</p></Card>
          <Card padding="lg"><h3>{{usersByRole.client || 0}}</h3><p>Clients</p></Card>
          <Card padding="lg"><h3>{{usersByRole.accountant || 0}}</h3><p>Accountants</p></Card>
        </div>

        <h2 style={{{{ marginBottom: 16, marginTop: 32 }}}}>Jobs by Status</h2>
        <div className="stats-grid">
          <Card padding="lg"><h3>{{jobsByStatus.open || 0}}</h3><p>Open</p></Card>
          <Card padding="lg"><h3>{{jobsByStatus.closed || 0}}</h3><p>Closed</p></Card>
        </div>

        <h2 style={{{{ marginBottom: 16, marginTop: 32 }}}}>Bids by Status</h2>
        <div className="stats-grid">
          <Card padding="lg"><h3>{{bidsByStatus.pending || 0}}</h3><p>Pending</p></Card>
          <Card padding="lg"><h3>{{bidsByStatus.accepted || 0}}</h3><p>Accepted</p></Card>
          <Card padding="lg"><h3>{{bidsByStatus.rejected || 0}}</h3><p>Rejected</p></Card>
        </div>
      </main>
    </div>
  );
}}
'''


# =============================================
# WRITE ALL FILES
# =============================================
if __name__ == "__main__":
    os.makedirs(BASE, exist_ok=True)
    for filename, content in FILES.items():
        filepath = os.path.join(BASE, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created: {filename}")
    print(f"\n🎉 {len(FILES)} admin pages fixed!")
    print("Restart frontend: cd frontend && npm run dev")