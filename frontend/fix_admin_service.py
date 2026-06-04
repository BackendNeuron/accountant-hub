with open(r'src\services\adminService.js', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(r"activate: async (id) => { const { data } = await api.patch('/admin/users/' + id + '/activate'); return data; },\n\n  removeRestrictions: async", r"activate: async (id) => { const { data } = await api.patch('/admin/users/' + id + '/activate'); return data; },

  removeRestrictions: async")

with open(r'src\services\adminService.js', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
