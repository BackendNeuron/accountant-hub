import os
path = r'C:\Mohamed\Accountant_Hub\frontend\src\App.jsx'
with open(path, 'r') as f:
    content = f.read()

content = content.replace(
    "import ClientJobDetailPage from './pages/client/ClientJobDetailPage';",
    "import ClientJobDetailPage from './pages/client/ClientJobDetailPage';\nimport AccountantProfileView from './pages/client/AccountantProfileView';"
)

content = content.replace(
    '<Route path="client/jobs/:id" element={<ClientJobDetailPage />} />',
    '<Route path="client/jobs/:id" element={<ClientJobDetailPage />} />\n              <Route path="accountant/:id" element={<AccountantProfileView />} />'
)

with open(path, 'w') as f:
    f.write(content)
print('Done')
