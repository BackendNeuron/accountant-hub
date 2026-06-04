import re

# Fix adminService.js
with open(r'src\services\adminService.js', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(r",\n\n  removeRestrictions", r",

  removeRestrictions")

with open(r'src\services\adminService.js', 'w', encoding='utf-8') as f:
    f.write(content)

# Fix UsersPage.jsx
with open(r'src\pages\admin\UsersPage.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(r'});\n\n  const deleteMutation', r'});

  const deleteMutation')

with open(r'src\pages\admin\UsersPage.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed both files')
