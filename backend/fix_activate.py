with open('app/api/v1/admin/users.py', 'r') as f:
    content = f.read()

activate_endpoint = '''

@router.patch("/{user_id}/activate")
async def activate_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    user.is_active = True
    user.updated_by = current_user.id
    await db.flush()
    return {"message": "User activated"}
'''

content = content.rstrip() + activate_endpoint + '\n'
with open('app/api/v1/admin/users.py', 'w') as f:
    f.write(content)
print('Done')
