with open('app/api/v1/router.py', 'r') as f:
    content = f.read()

content = content.replace(
    'from app.api.v1 import nda, match, documents, client_jobs',
    'from app.api.v1 import nda, match, documents, client_jobs, accountants'
)

content = content.replace(
    'api_v1_router.include_router(client_jobs.router, prefix="/my-jobs", tags=["My Jobs"])',
    'api_v1_router.include_router(client_jobs.router, prefix="/my-jobs", tags=["My Jobs"])\napi_v1_router.include_router(accountants.router, prefix="/accountants", tags=["Accountants"])'
)

with open('app/api/v1/router.py', 'w') as f:
    f.write(content)
print('Done')
