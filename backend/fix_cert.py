with open('app/api/v1/admin/certifications.py', 'r') as f:
    content = f.read()

old = '    await db.delete(cert)\n    await db.flush()\n    return {\"message\": \"Certification deleted\"}'
new = '    try:\n        await db.delete(cert)\n        await db.flush()\n    except Exception:\n        raise HTTPException(400, \"Cannot delete this certification because it is assigned to accountants.\")\n    return {\"message\": \"Certification deleted\"}'

content = content.replace(old, new)

with open('app/api/v1/admin/certifications.py', 'w') as f:
    f.write(content)
print('Done')
