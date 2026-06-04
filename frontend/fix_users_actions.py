import re

with open(r'src\pages\admin\UsersPage.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the actions column render
old = "{ key: 'actions', label: 'Actions', render: (r) => ("
new = """{ key: 'actions', label: 'Actions', render: (r) => {
    if (r.is_active) {
      return <div style={{ display: 'flex', gap: 8 }}><Button size="sm" variant="danger" onClick={() => { if (confirm('Deactivate?')) deleteMutation.mutate(r.id); }}>Deactivate</Button></div>;
    } else {
      return <div style={{ display: 'flex', gap: 8 }}><Button size="sm" variant="primary" onClick={() => activateMutation.mutate(r.id)}>Activate</Button></div>;
    }
  }},
  { key: 'dummy', label: '', render: (r) => ("""

content = content.replace(old, new)

with open(r'src\pages\admin\UsersPage.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
